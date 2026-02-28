import os

import djclick as click
import json
import requests

from bs4 import BeautifulSoup
from django.db.utils import IntegrityError
from django.utils.text import slugify
from pathlib import Path
from playwright.sync_api import sync_playwright
from rich import print
from urllib.parse import parse_qs
from urllib.parse import urlparse

from events.models import Event
from races.models import Race


os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = "true"

RACES = [
    "100642",
    "10136",
    "101450",
    "102084",
    "10470",
    "11877",
    "11986",
    "12054",
    "14150",
    "14555",
    "14595",
    "14596",
    "14609",
    "15764",
    "16492",
    "17970",
    "18024",
    "19047",
    "19803",
    "24643",
    "26492",
    "26792",
    "27470",
    "29677",
    "30887",
    "30993",
    "31005",
    "31893",
    "32583",
    "34358",
    "34684",
    "36684",
    "37251",
    "37656",
    "37661",
    "41893",
    "41915",
    "43927",
    "43955",
    "44706",
    "44714",
    "49109",
    "52219",
    "52373",
    "52586",
    "53172",
    "55704",
    "55790",
    "56930",
    "57643",
    "59603",
    "61389",
    "62683",
    "63105",
    "63478",
    "65177",
    "69551",
    "69866",
    "73085",
    "73545",
    "7624",
    "76498",
    "78562",
    "82056",
    "83843",
    "86850",
    "87320",
    "89529",
    "89804",
    "90349",
    "92171",
    "95773",
    "96599",
    "97574",
    "97585",
]


@click.command()
def command():
    ultrasignup_ids = list(
        Race.objects.exclude(ultrasignup_id=None)
        .order_by("-pk")
        .only("ultrasignup_id")
        .values_list("ultrasignup_id", flat=True)
    )

    race_ids = list(set(ultrasignup_ids).union(set(RACES)))

    with sync_playwright() as p:
        # Launch the browser and open a new page
        dids = []

        for parent_did in RACES:
            # playwright.firefox
            browser = p.firefox.launch()
            page = browser.new_page()

            # Navigate to the URL
            url = f"https://ultrasignup.com/results_event.aspx?did={parent_did}"
            page.goto(url)
            rendered_html = page.content()

            soup = BeautifulSoup(rendered_html, features="lxml")

            event_name = soup.find("h1").string

            event, created = Event.objects.get_or_create(title=event_name, defaults={"status": Event.STATUS_DRAFT})

            table = soup.find_all("table")[2]
            for cell in table.find_all("td"):
                try:
                    year = cell.text.strip()
                    print(f"{year=}")

                    anchor = cell.find("a")
                    if anchor:
                        href = anchor.get("href")
                        href = f"https://ultrasignup.com{href}"
                        print(f"{href=}")

                        if "did" in href:
                            parsed_url = urlparse(href)
                            params = parse_qs(parsed_url.query)
                            did = params["did"][0]
                            print(f"{did=}")

                            # log our dids for later
                            dids.append(
                                {
                                    "did": did,
                                    "name": event_name,
                                    "year": year,
                                }
                            )

                            race = Race.objects.get(ultrasignup_id=did)
                            event.races.add(race)

                except Race.DoesNotExist:
                    print(f"[red]{did=}[/red]")

                    title = f"{event_name} {year}"
                    try:
                        race, created = Race.objects.get_or_create(
                            title=title,
                            ultrasignup_id=did,
                            defaults={
                                "slug": slugify(title),
                                "start_datetime": f"{year}-01-01 12:00:00",
                            },
                        )
                    except IntegrityError as e:
                        print(f"[red]{e}[/red]")

                except Exception as e:
                    print(f"[red]{e}[/red]")

            # for index, row in dfs[0].iterrows():
            #     print(row)

            # Close the browser
            browser.close()

        # clean_rank = lambda x: float(x.replace('%', ''))
        # converters = {
        #     "Place": int,
        #     "First": str,
        #     "Last": str,
        #     "City": str,
        #     "Age": str,
        #     "Gender": str,
        #     "GP": int,
        #     "Time": str,
        #     "Rank": clean_rank,  # float,
        # }
        # dfs = pandas.read_html(rendered_html, converters=converters)
        # print(len(dfs))
        # print(dfs[2].info())
        # print(dfs[2])

        # print("[blue]{}[/blue]".format("-" * 20))

        print(f"[blue]{dids=}[/blue]")
        for did in dids:
            try:
                # Navigate to the URL
                url = f"https://ultrasignup.com/service/events.svc/results/{did['did']}/1/json?_search=false&rows=2000&page=1&sidx=&sord=asc"
                response = requests.get(url)
                response.raise_for_status()

                filename = slugify(f"{did['did']} {did['name']} {did['year']} ")
                filename = f"{filename}.json"

                Path("exports", filename).write_text(json.dumps(response.json(), indent=2))

            except Exception as e:
                print(f"[red]{e}[/red]")

        # Extract the table data using pandas
        # data_frame = pandas.read_html(rendered_html)
