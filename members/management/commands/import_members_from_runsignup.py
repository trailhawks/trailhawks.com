import djclick as click
import requests
from dateutil.parser import parse
from django.conf import settings

from members.models import Member


@click.command()
def command():
    response = requests.get(
        settings.RUNSIGNUP_URL + "/members",
        {
            "rsu_api_key": settings.RUNSIGNUP_KEY,
            "format": "json",
            "results_per_page": "2500",
        },
        headers={"X-RSU-API-SECRET": settings.RUNSIGNUP_SECRET},
    )

    club_members = response.json()["club_members"]
    for club_member in club_members:
        user = club_member["user"]
        address = user["address"]
        try:
            member, created = Member.objects.update_or_create(
                email=user["email"],
                defaults={
                    "first_name": user["first_name"],
                    "last_name": user["last_name"],
                    "phone": user.get("phone", None),
                    "address": address["street"],
                    "city": address["city"],
                    "state": address["state"],
                    "zip": address["zipcode"],
                    "date_paid": parse(club_member["registration_date"]),
                    "gender": user.get("gender", None),
                },
            )
            if created:
                print(
                    "[yellow]{} {}[/yellow] was imported".format(
                        user["first_name"], user["last_name"]
                    )
                )
                # member.member_since = parse(result["Registration Date"].split(" ")[0])
                # member.notes = f"{result['Price Option']}"
                # member.save()

        except Exception as e:
            print(f"[red]{e=}[/red]")
            print(f"{club_member=}")
