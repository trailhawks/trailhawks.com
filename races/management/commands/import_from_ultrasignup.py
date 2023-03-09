import json
from pathlib import Path

import djclick as click
import requests

from races.models import Race, Racer, Result


@click.command()
# @click.argument("result_id")
# @click.option("race_slug", "--slug", "--race-slug")
# @click.option("race_type_name", "--race-type")
@click.option("race_id", "--race", "--race-id", "--race-pk")
def command(race_id):
    headers = {"Content-type": "application/json"}

    races = Race.objects.all().exclude(ultrasignup_id=None)
    for race in races:
        print(f"{race.pk}=={race.ultrasignup_id}")
        url = f"https://ultrasignup.com/service/events.svc/results/{race.ultrasignup_id}/1/json"

        if not Path("_results").exists():
            Path("_results").mkdir()

        filename = Path("_results", f"{race.ultrasignup_id}.json")

        if filename.exists():
            input_buffer = json.loads(filename.read_text())
        else:
            request = requests.get(url, headers=headers)
            input_buffer = request.json()
            filename.write_text(json.dumps(input_buffer, indent=2))

        if len(input_buffer) > 0:
            # try:
            #     if race_id:
            #         race = Race.objects.get(pk=race_id)
            #     elif race_slug:
            #         race = Race.objects.get(slug=race_slug)
            #     else:
            #         raise Exception("We need a Race <pk> or <slug>")
            # except Race.DoesNotExist:
            #     raise Exception(f"Race <pk:{race_id}> or <slug:{race_slug}> not found")

            # race_type, _ = RaceType.objects.get_or_create(name=race_type_name)

            for item in input_buffer:
                racer, _ = Racer.objects.update_or_create(
                    first_name=item["firstname"],
                    last_name=item["lastname"],
                    defaults={
                        "city": item["city"],
                        "country": "USA",
                        "gender": Racer.MALE if item["gender"] == "M" else Racer.FEMALE,
                        "state": item["state"],
                    },
                )

                formattime = item["formattime"]

                if len(formattime) in [1, 2]:
                    formattime = ""

                elif len(formattime) == 7:
                    formattime = f"0{formattime}"

                result, _ = Result.objects.update_or_create(
                    race=race,
                    # race_type=race_type,
                    racer=racer,
                    defaults={
                        "bib_number": item["bib"] or None,
                        "dnf": item["status"] == 3,
                        "dns": item["status"] == 2,
                        "time": formattime,
                    },
                )
