"""Import race results from UltraSignup.

Dry-run by default: it fetches and prints exactly what it *would* create or
update, and writes nothing. Pass --commit to actually save.

UltraSignup structure this relies on:
  * Each distance of an event has its own numeric event id ("did"). The distances
    of one event are consecutive dids (e.g. the Hawk = 52373/52374/52375/52376).
  * ``results_event.aspx?did=<did>`` lists the ordered distance names for that event.
  * ``service/events.svc/results/<did>/1/json`` returns that distance's finishers.
  * Per-finisher ``status``: 1 = finished, 2 = DNS, 3 = DNF.

A race's stored ``ultrasignup_id`` is treated as one of the event's distance dids;
the sibling distances are discovered from the consecutive run around it.

Examples:
  manage.py import_ultrasignup_results --race 146            # dry-run one race
  manage.py import_ultrasignup_results --race 146 --commit   # write it
  manage.py import_ultrasignup_results --all-importable      # dry-run every past race w/o results
"""

import re
import time

import djclick as click
import requests

from races.models import Race, Racer, RaceType, Result

UA = "Mozilla/5.0 (compatible; TrailHawksResultsImporter/1.0)"
RESULTS_API = "https://ultrasignup.com/service/events.svc/results/{did}/1/json"
EVENT_PAGE = "https://ultrasignup.com/results_event.aspx?did={did}"


def _get(url):
    resp = requests.get(url, headers={"User-Agent": UA, "Accept": "application/json"}, timeout=30)
    resp.raise_for_status()
    return resp


def fetch_results(did):
    try:
        return _get(RESULTS_API.format(did=did)).json()
    except (ValueError, requests.RequestException):
        return []


def discover_distances(did):
    """Return ordered [(distance_name, did), ...] for the event `did` belongs to."""
    try:
        html = _get(EVENT_PAGE.format(did=did)).text
    except requests.RequestException:
        return [(None, did)]

    names_match = re.search(r'distances">([^<]+)<', html)
    names = [n.strip() for n in names_match.group(1).split(",")] if names_match else []

    # dids that appear as result tabs on this page
    tab_dids = {int(x) for x in re.findall(r"results_event\.aspx\?did=(\d+)", html)}
    # the event's distances are the consecutive run of tab dids containing `did`
    run = [did]
    d = did - 1
    while d in tab_dids:
        run.insert(0, d)
        d -= 1
    d = did + 1
    while d in tab_dids:
        run.append(d)
        d += 1

    if names and len(names) == len(run):
        return list(zip(names, run))
    # fall back: pair as far as they line up, label the rest by did
    pairs = []
    for i, dd in enumerate(run):
        pairs.append((names[i] if i < len(names) else None, dd))
    return pairs


def _clean_time(formattime):
    if not formattime or len(formattime) in (1, 2):
        return ""
    if len(formattime) == 7:  # e.g. 9:59:59 -> 09:59:59
        return f"0{formattime}"
    return formattime


def _bib(raw):
    raw = str(raw or "").strip()
    return int(raw) if raw.isdigit() else None


def import_race(race, commit, echo):
    if not (race.ultrasignup_id and str(race.ultrasignup_id).isdigit()):
        echo(f"  skip: no numeric ultrasignup_id ({race.ultrasignup_id!r})")
        return {"skipped": 1}

    did = int(race.ultrasignup_id)
    distances = discover_distances(did)
    stats = {"created": 0, "updated": 0, "racers_created": 0, "distances": 0, "finishers": 0}

    for name, dist_did in distances:
        rows = fetch_results(dist_did)
        if not rows:
            continue
        stats["distances"] += 1
        stats["finishers"] += len(rows)
        label = name or f"did {dist_did}"
        echo(f"  distance {label!r} (did={dist_did}): {len(rows)} finishers")

        race_type = None
        if name:
            if commit:
                race_type, _ = RaceType.objects.get_or_create(name=name)
            else:
                race_type = RaceType.objects.filter(name=name).first()

        for item in rows:
            first, last = item.get("firstname", ""), item.get("lastname", "")
            racer = Racer.objects.filter(first_name=first, last_name=last).first()
            if racer is None:
                stats["racers_created"] += 1
                if commit:
                    racer, _ = Racer.objects.get_or_create(
                        first_name=first,
                        last_name=last,
                        defaults={
                            "city": item.get("city") or "",
                            "state": item.get("state") or "",
                            "country": "USA",
                            "gender": "Man" if item.get("gender") == "M" else "Woman",
                        },
                    )

            defaults = {
                "bib_number": _bib(item.get("bib")),
                "time": _clean_time(item.get("formattime")),
                "place": str(item.get("place")) if item.get("place") is not None else "",
                "dns": item.get("status") == 2,
                "dnf": item.get("status") == 3,
                "import_data": item,
            }

            exists = (
                Result.objects.filter(race=race, race_type=race_type, racer=racer).exists()
                if (commit and racer)
                else False
            )
            if commit and racer:
                Result.objects.update_or_create(
                    race=race, race_type=race_type, racer=racer, defaults=defaults
                )
            stats["updated" if exists else "created"] += 1

    return stats


@click.command()
@click.option("--race", "race_ids", multiple=True, type=int, help="Race pk (repeatable).")
@click.option("--all-importable", is_flag=True, help="Every past race with an ultrasignup_id and no results.")
@click.option("--commit", is_flag=True, help="Actually write (default is a dry run).")
@click.option("--limit", type=int, default=0, help="Cap number of races processed.")
def command(race_ids, all_importable, commit, limit):
    if all_importable:
        from django.utils import timezone

        qs = (
            Race.objects.exclude(ultrasignup_id="")
            .exclude(ultrasignup_id=None)
            .filter(start_datetime__lt=timezone.now())
            .order_by("-start_datetime")
        )
        races = [r for r in qs if not r.result_set.exists()]
    elif race_ids:
        races = list(Race.objects.filter(pk__in=race_ids))
    else:
        raise click.ClickException("Pass --race <pk> (repeatable) or --all-importable")

    if limit:
        races = races[:limit]

    mode = click.style("COMMIT", fg="red", bold=True) if commit else click.style("DRY RUN", fg="green", bold=True)
    click.echo(f"[{mode}] {len(races)} race(s)\n")

    totals = {"created": 0, "updated": 0, "racers_created": 0}
    for race in races:
        click.echo(click.style(f"[{race.pk}] {race.title} {race.start_datetime:%Y-%m-%d}", bold=True))
        s = import_race(race, commit, click.echo)
        for k in totals:
            totals[k] += s.get(k, 0)
        click.echo(
            f"  => results {'created' if commit else 'to create'}: {s.get('created', 0)}, "
            f"updated: {s.get('updated', 0)}, racers new: {s.get('racers_created', 0)}\n"
        )
        time.sleep(0.5)

    verb = "wrote" if commit else "would create"
    click.echo(
        click.style(
            f"TOTAL: {verb} {totals['created']} results "
            f"({totals['updated']} updated), {totals['racers_created']} new racers.",
            bold=True,
        )
    )
    if not commit:
        click.echo("Re-run with --commit to save.")
