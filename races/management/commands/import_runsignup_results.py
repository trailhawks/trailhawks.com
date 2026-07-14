"""Import race results from RunSignup.

Dry-run by default: fetches and prints what it *would* create/update, writing
nothing. Pass --commit to save.

RunSignup structure this relies on:
  * One RunSignup ``race_id`` holds every year as a separate ``event``; each event
    is a (distance, date) pair whose ``name`` is the distance (e.g. "5K", "10K").
  * ``rest/race/<race_id>?format=json`` lists the events (with start_time).
  * ``rest/race/<race_id>/results/get-results?event_id=<id>`` returns finishers,
    paginated, grouped in result sets.

For a given race record we take its stored RunSignup URL, resolve the numeric
race_id, then import every event whose start year matches the race's year — one
RaceType per event/distance.

Examples:
  manage.py import_runsignup_results --race 135            # dry-run one race
  manage.py import_runsignup_results --race 135 --commit   # write it
  manage.py import_runsignup_results --all-runsignup       # dry-run every past RunSignup race w/o results
"""

import re

import djclick as click
import requests

from races.models import Race, Racer, RaceType, Result

UA = "Mozilla/5.0 (compatible; TrailHawksResultsImporter/1.0)"
REST = "https://runsignup.com/rest/race/{race_id}"
PER_PAGE = 250


def _get_json(url, params):
    params = {**params, "format": "json"}
    resp = requests.get(url, params=params, headers={"User-Agent": UA}, timeout=30)
    resp.raise_for_status()
    return resp.json()


def resolve_race_id(reg_url):
    """Numeric RunSignup race_id from a race's registration URL."""
    m = re.search(r"[?&]raceId=(\d+)", reg_url)
    if m:
        return int(m.group(1))
    resp = requests.get(reg_url, headers={"User-Agent": UA}, timeout=30)
    resp.raise_for_status()
    m = re.search(r'raceId["\' :=]+(\d+)', resp.text)
    return int(m.group(1)) if m else None


def select_year_events(events, year):
    """Pure: [(event_id, distance_name), ...] for events starting in `year`.

    RunSignup start_time looks like "7/20/2024 07:00"; the year is the token
    after the second slash.
    """
    out = []
    for e in events:
        m = re.search(r"/(\d{4})\b", e.get("start_time", ""))
        if m and int(m.group(1)) == year:
            out.append((e.get("event_id"), (e.get("name") or "").strip()))
    return out


def events_for_year(race_id, year):
    """[(event_id, distance_name), ...] for events starting in `year`."""
    data = _get_json(REST.format(race_id=race_id), {})
    race = data.get("race", data)
    return select_year_events(race.get("events", []), year)


def fetch_finishers(race_id, event_id):
    """All finisher rows for an event, across result sets and pages."""
    rows = []
    page = 1
    while True:
        data = _get_json(
            f"{REST.format(race_id=race_id)}/results/get-results",
            {"event_id": event_id, "results_per_page": PER_PAGE, "page": page},
        )
        sets = data.get("individual_results_sets") or []
        page_rows = [r for s in sets for r in s.get("results", [])]
        rows.extend(page_rows)
        if len(page_rows) < PER_PAGE:
            break
        page += 1
    return rows


def _bib(raw):
    raw = str(raw or "").strip()
    return int(raw) if raw.isdigit() else None


def _gender(raw):
    if raw == "M":
        return "Man"
    if raw == "F":
        return "Woman"
    return ""


def import_race(race, commit, echo):
    if "runsignup" not in (race.reg_url or ""):
        echo("  skip: no RunSignup URL")
        return {"skipped": 1}

    race_id = resolve_race_id(race.reg_url)
    if not race_id:
        echo(f"  skip: could not resolve race_id from {race.reg_url}")
        return {"skipped": 1}

    year = race.start_datetime.year
    events = events_for_year(race_id, year)
    if not events:
        echo(f"  no RunSignup events found for {year} (race_id={race_id})")
        return {}

    stats = {"created": 0, "updated": 0, "racers_created": 0}
    for event_id, distance in events:
        rows = fetch_finishers(race_id, event_id)
        if not rows:
            continue
        label = distance or f"event {event_id}"
        echo(f"  distance {label!r} (event={event_id}): {len(rows)} finishers")

        race_type = None
        if distance:
            race_type = (
                RaceType.objects.get_or_create(name=distance)[0]
                if commit
                else RaceType.objects.filter(name=distance).first()
            )

        for item in rows:
            first, last = (item.get("first_name") or "").strip(), (item.get("last_name") or "").strip()
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
                            "gender": _gender(item.get("gender")),
                        },
                    )

            defaults = {
                "bib_number": _bib(item.get("bib")),
                "time": (item.get("chip_time") or item.get("clock_time") or "").strip(),
                "place": str(item["place"]) if item.get("place") is not None else "",
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
@click.option("--all-runsignup", is_flag=True, help="Every past RunSignup race with no results.")
@click.option("--commit", is_flag=True, help="Actually write (default is a dry run).")
@click.option("--limit", type=int, default=0)
def command(race_ids, all_runsignup, commit, limit):
    if all_runsignup:
        from django.utils import timezone

        qs = Race.objects.filter(reg_url__contains="runsignup", start_datetime__lt=timezone.now()).order_by(
            "-start_datetime"
        )
        races = [r for r in qs if not r.result_set.exists()]
    elif race_ids:
        races = list(Race.objects.filter(pk__in=race_ids))
    else:
        raise click.ClickException("Pass --race <pk> (repeatable) or --all-runsignup")

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
