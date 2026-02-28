import json

import djclick as click

from dateutil.parser import parse
from num2words import num2words
from rich import print
from slugify import slugify
from titlecase import titlecase

from scrapers.scrape_ultrasignup import RaceListFromDjango
from races.models import Race, Racer, RaceType, Result


@click.command()
@click.option("--create/--no-create", default=False)
@click.option("--update/--no-update", default=False)
def command(create, update):
    missing = []

    race_list = RaceListFromDjango()
    for data in race_list.do_scrape():
        print(json.dumps(data, indent=2))

        date = parse(data["date"].split("@")[0])
        did = data["did"]
        distance = data["distance"]
        formattime = data["formattime"]
        gender = data["gender"]
        gender_place = data["gender_place"]
        place = data["place"]

        place_data = []

        if gender_place in [1, 2, 3]:
            if gender.upper() in ["F", "W"]:
                if place in [1, 2, 3]:
                    place_data.append(titlecase(f"{num2words(place, ordinal=True)} Place Overall."))
                place_data.append(titlecase(f"{num2words(gender_place, ordinal=True)} Place Womens."))
            elif gender.upper() in ["M"]:
                place_data.append(titlecase(f"{num2words(gender_place, ordinal=True)} Place Mens."))
            else:
                place_data.append(titlecase(f"{num2words(gender_place, ordinal=True)} Place Overall."))

        if len(place_data):
            place_data = " ".join(place_data)
        else:
            place_data = ""

        try:
            title = f"{data['title']} {date.strftime('%Y')}"
            race_defaults = {
                "slug": slugify(title),
                "start_datetime": date,
                "title": title,
            }
            if create:
                race, _ = Race.objects.get_or_create(
                    ultrasignup_id=did,
                    defaults=race_defaults,
                )
            elif update:
                race, _ = Race.objects.update_or_create(
                    ultrasignup_id=did,
                    defaults=race_defaults,
                )
            else:
                race = Race.objects.get(ultrasignup_id=did)

            # TODO: Fix slugs
            race_type, _ = RaceType.objects.get_or_create(name=distance)
            # race_type, _ = RaceType.objects.get_or_create(
            #     slug=slugify(distance), defaults={"name": distance}
            # )

            racer, _ = Racer.objects.update_or_create(
                first_name=data["firstname"],
                last_name=data["lastname"],
                defaults={
                    "city": data["city"],
                    "country": "USA",
                    "gender": "Man" if data["gender"] == "M" else "Woman",
                    "state": data["state"],
                },
            )

            if len(formattime) in [1, 2]:
                formattime = ""
            elif len(formattime) == 7:
                formattime = f"0{formattime}"

            try:
                result, _ = Result.objects.update_or_create(
                    race=race,
                    racer=racer,
                    race_type=race_type,
                    defaults={
                        "bib_number": data["bib"] or None,
                        "dnf": data["status"] == 3,
                        "dns": data["status"] == 2,
                        "import_data": data,
                        "place": place_data,
                        # "race_type": race_type,
                        "time": formattime,
                    },
                )
            except Result.MultipleObjectsReturned as e:
                click.secho(f"{e}", bold=True, fg="red")
                click.echo(f"race: {race}")
                click.echo(f"race_type: {race_type}")
                click.echo(f"racer: {racer}")

        except (Race.DoesNotExist, Race.MultipleObjectsReturned) as e:
            ultrasignup_url = f"https://ultrasignup.com/results_event.aspx?did={did}"
            click.secho(
                f"{e}:{ultrasignup_url}",
                bold=True,
                fg="red",
            )
            if ultrasignup_url not in missing:
                missing.append(ultrasignup_url)

        print()
