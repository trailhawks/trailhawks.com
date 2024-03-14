# from enum import Enum

import django  # noqa
from spatula import (
    HtmlListPage,
    HtmlPage,
    JsonListPage,
    NullSource,
    Page,
    SelectorError,
    XPath,
)

django.setup()  # noqa

from races.models import Race  # noqa


class RaceListFromDjango(Page):
    source = NullSource()

    def process_error_response(self, exception):
        self.logger.warning(exception)

    def process_page(self):
        races = Race.objects.exclude(ultrasignup_id=None)
        for race in races:
            source = f"https://ultrasignup.com/results_event.aspx?did={race.ultrasignup_id}"
            yield RaceResultListPage(
                dict(
                    did=race.ultrasignup_id,
                    race_url=f"https://trailhawks.com{race.get_absolute_url()}",
                    year=race.start_datetime.year,
                ),
                source=source,
            )


class RaceResultListPage(HtmlListPage):
    """
    Every race may have zero or more distances which have their own unique`did`
    race number.
    """

    selector = XPath("//a[@class='event_link' or @class='event_selected_link']", min_items=None)
    source = NullSource()

    def process_error_response(self, exception):
        self.logger.warning(exception)

    def process_item(self, item):
        href = XPath("@href").match_one(item)
        if not href.startswith("http"):
            href = f"https://ultrasignup.com{href}"
        race_id = href.split("=")[-1]
        return RaceResultDetail(dict(race_id=race_id, race_results_url=href, **self.input), source=href)


class RaceResultDetail(HtmlPage):
    """
    Process the main race information including individual information about the event.
    """

    example_source = "https://ultrasignup.com/results_event.aspx?did=63105"
    source = NullSource()

    def process_error_response(self, exception):
        self.logger.warning(exception)

    def process_page(self):
        try:
            cancellation = XPath("//span[contains(@class,'cancellation_text')]").match_one(self.root)
            cancellation = True
        except SelectorError:
            cancellation = False

        try:
            did = XPath("//a[@class='event_selected_link']").match_one(self.root).get("href").split("=")[-1]
        except SelectorError:
            did = ""

        try:
            distance = XPath("//a[@class='event_selected_link']").match_one(self.root).text
        except SelectorError:
            distance = ""

        # try:
        #     distance_results = XPath(
        #         "//a[@class='event_link' or @class='event_selected_link']"
        #     ).match(self.root)
        #     distance_results = {
        #         item.text: item.get("href") for item in distance_results
        #     }
        # except SelectorError:
        #     distance_results = None

        try:
            event_date = XPath("//span[@class='event-date']").match_one(self.root).text
        except SelectorError:
            event_date = ""

        try:
            virtual = XPath("//span[contains(@class,'virtual_text')]").match_one(self.root)
            virtual = True
        except SelectorError:
            virtual = False

        title = XPath("//h1").match_one(self.root)
        website = XPath("//a[@class='websiteitem']").match_one(self.root).get("href")

        return ResultJsonListPage(
            dict(
                cancellation=cancellation,
                date=event_date,
                distance=distance,
                # slug=slugify(title.text),
                title=title.text,
                virtual=virtual,
                website=website,
                **self.input,
            ),
            source=f"https://ultrasignup.com/service/events.svc/results/{did}/1/json",
        )


class ResultJsonListPage(JsonListPage):
    """
    Parse each row of our JSON results file supplemented with additional page
    information so that we know which race we have parsed.
    """

    example_source = "https://ultrasignup.com/service/events.svc/results/63105/1/json"
    source = NullSource()

    def process_item(self, item):
        # print(item)
        return dict(**self.input, **item)


if __name__ == "__main__":
    page = RaceListFromDjango()
    for e in page.do_scrape():
        print(e)
