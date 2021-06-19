import djclick as click
import json

from dateutil.parser import parse
from pathlib import Path

# from slugify import slugify

from races.models import Race, Racer, RaceType, Result


@click.command()
@click.argument("folder")
def command(folder):
    missing = []
    filenames = Path(folder).glob("*.json")
    for filename in filenames:
        data = json.loads(filename.read_text())

        did = data["did"]
        distance = data["distance"]
        formattime = data["formattime"]
        start_datetime = parse(data["date"].split("@")[0])
        title = data["title"]
        ultrasignup_id = data["ultrasignup_id"]

        # click.echo(
        #     [
        #         title,
        #         start_datetime.year,
        #         ultrasignup_id,
        #         did,
        #         distance,
        #         data["firstname"],
        #         data["lastname"],
        #         data["formattime"],
        #     ]
        # )

        try:
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
                    "gender": Racer.MALE if data["gender"] == "M" else Racer.FEMALE,
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
                    race_type=race_type,
                    racer=racer,
                    defaults={
                        "bib_number": data["bib"] or None,
                        "dnf": data["status"] == 3,
                        "dns": data["status"] == 2,
                        "time": formattime,
                    },
                )
            except Result.MultipleObjectsReturned as e:
                click.secho(f"{e}", bold=True, fg="red")

        except (Race.DoesNotExist, Race.MultipleObjectsReturned) as e:
            ultrasignup_url = f"https://ultrasignup.com/results_event.aspx?did={did}"
            click.secho(
                f"{e}:{ultrasignup_url}",
                bold=True,
                fg="red",
            )
            if ultrasignup_url not in missing:
                missing.append(ultrasignup_url)

    for filename in missing:
        click.echo(f"{filename}")
