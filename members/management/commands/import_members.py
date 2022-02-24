import csv
import logging

import djclick as click

from dateutil.parser import parse

from members.models import Member

logger = logging.getLogger(__name__)


@click.command()
@click.argument("filename")
@click.option("--update", default=False)
def command(filename, update):
    if not filename:
        raise Exception("You forgot the CSV silly")

    with open(filename) as f:
        result_data = list(csv.DictReader(f))
        for result in result_data:
            member, created = Member.objects.update_or_create(
                email=result["Email"],
                defaults={
                    "first_name": result["First Name"],
                    "last_name": result["Last Name"],
                    # "hawk_name": result[""],
                    "phone": result["Phone"],
                    "address": result["Address"],
                    # "address2": result[""],
                    "city": result["City"],
                    "state": result["State"],
                    "zip": result["Zip"],
                    "date_paid": parse(result["Registration Date"].split(" ")[0]),
                    "gender": result["Identified Gender"],
                    # "notes": result[""],
                }
            )
            if created:
                click.echo(f"{member} was imported")
                member.member_since = parse(result["Registration Date"].split(" ")[0])
                member.notes = f"{result['Price Option']}"
                member.save()

            else:
                click.echo(f"{member} was updated")
