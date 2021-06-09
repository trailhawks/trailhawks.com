import csv
import djclick as click
import logging

from races.models import Race, RaceType, Racer, Result


logger = logging.getLogger(__name__)


@click.command()
@click.option("--race")
@click.option("csv_filename", "--csv")
@click.option("--update", default=False)
def command(race, csv_filename, update):
    logger.info(race)

    if not csv_filename:
        raise Exception("You forgot the CSV silly")

    if not race:
        raise Exception("You forgot to add the Race silly")

    try:
        race = Race.objects.get(pk=int(race))
    except ValueError:
        race = Race.objects.get(slug=race)

    with open(csv_filename, "r") as f:
        result_data = list(csv.DictReader(f))

    for row in result_data:
        defaults = {}
        race_type = None
        bib_number = row["bib"]
        time = row["time"]
        place = row["comments"]
        first_name = row["first_name"]
        last_name = row["last_name"]
        distance = row["distance"]

        if row["gender"].strip() in ["m", "M"]:
            gender = 1
        else:
            gender = 2

        racer, _ = Racer.objects.get_or_create(
            first_name=first_name, last_name=last_name, gender=gender
        )

        if len(distance):
            race_type, _ = RaceType.objects.get_or_create(name=distance)

        if "CR" in place:
            defaults["course_record"] = True

        if "DNF" in time:
            defaults["dnf"] = True

        if "DNS" in time:
            defaults["dns"] = True

        logger.info("Found Racer: {0}".format(racer))

        # might update_or_create...
        result, _ = Result.objects.get_or_create(
            race=race,
            racer=racer,
            time=time,
            bib_number=bib_number,
            place=place,
            defaults=defaults,
        )

        if race_type:
            result.race_type = race_type
            result.save()

        logger.info("Result for {0} for race: {1}".format(racer, race))
        logger.info(result)

    logger.info("results loaded")
