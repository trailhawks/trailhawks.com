import djclick as click
import json
import requests

from pathlib import Path
from races.models import Race, RaceType, Racer, Result


@click.command()
@click.argument("result_id")
@click.option("race_id", "--race", "--race-id", "--race-pk")
@click.option("race_slug", "--slug", "--race-slug")
@click.option("race_type_name", "--race-type")
def command(result_id, race_id, race_slug, race_type_name):
    headers = {"Content-type": "application/json"}
    url = f"https://ultrasignup.com/service/events.svc/results/{result_id}/1/json"

    if not Path("results").exists():
        Path("results").mkdir()

    filename = Path("results", f"{result_id}.json")

    if filename.exists():
        input_buffer = json.loads(filename.read_text())
    else:
        request = requests.get(url, headers=headers)
        input_buffer = request.json()
        filename.write_text(json.dumps(input_buffer, indent=2))

    try:
        if race_id:
            race = Race.objects.get(pk=race_id)
        elif race_slug:
            race = Race.objects.get(slug=race_slug)
        else:
            raise Exception("We need a Race <pk> or <slug>")
    except Race.DoesNotExist:
        raise Exception(f"Race <pk:{race_id}> or <slug:{race_slug}> not found")

    race_type, _ = RaceType.objects.get_or_create(name=race_type_name)

    for item in input_buffer:
        # TODO: try to track by member too...
        racer, _ = Racer.objects.update_or_create(
            first_name=item["firstname"],
            last_name=item["lastname"],
            defaults={
                "gender": Racer.MALE if item["gender"] == "M" else Racer.FEMALE,
                "city": item["city"],
                "state": item["state"],
                "country": "USA",
            },
        )

        formattime = item["formattime"]

        if len(formattime) in [1, 2]:
            formattime = ""

        elif len(formattime) == 7:
            formattime = f"0{formattime}"

        result, _ = Result.objects.update_or_create(
            race=race,
            race_type=race_type,
            racer=racer,
            defaults={
                "bib_number": item["bib"] or None,
                "time": formattime,
                "dnf": item["status"] == 3,
                "dns": item["status"] == 2,
            },
        )
