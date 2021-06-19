from enum import Enum

from spatula import (
    HtmlListPage,
    HtmlPage,
    JsonListPage,
    NullSource,
    Page,
    SelectorError,
    XPath,
)


class Races(Enum):
    PI_DAY = 69866
    SANDERS_SAUNTER = 73085
    SHORELINE_SHUFFLE = 78562
    SKYLINE_SHUFFLE = 76498
    THE_HAWK_HUNDRED = 83843
    THE_NIGHT_HAWK = 82056
    THE_SNAKE = 63478


DEFAULT_RACE_ID = Races.THE_HAWK_HUNDRED.value


class RaceList(Page):
    """
    Seed our top-level races to gather data.
    """

    source = NullSource()

    def process_page(self):
        for race in Races:
            yield RaceListDetail(
                dict(
                    ultrasignup_id=race.value,
                ),
                source=f"https://ultrasignup.com/results_event.aspx?did={race.value}",
            )


class RaceListDetail(HtmlListPage):
    """
    Collect annual year information for every race.
    """

    example_source = f"https://ultrasignup.com/results_event.aspx?did={DEFAULT_RACE_ID}"
    selector = XPath("//td/a[contains(@href,'/results_event.aspx?')]")
    source = NullSource()

    def process_error_response(self, exc):
        self.logger.warning(exc)

    def process_item(self, item):
        href = XPath("@href").match_one(item)
        if not href.startswith("http"):
            href = f"https://ultrasignup.com{href}"

        did = href.split("=")[-1]

        return RaceResultListPage(
            dict(
                did=did,
                race_url=href,
                ultrasignup_id=self.input.get("ultrasignup_id", did),
                year=item.text,
            ),
            source=href,
        )


class RaceResultListPage(HtmlListPage):
    """
    Every race may have zero or more distances which have their own unique`did`
    race number.
    """

    # example_source = f"https://ultrasignup.com/results_event.aspx?did={DEFAULT_RACE_ID}"
    selector = XPath(
        "//a[@class='event_link' or @class='event_selected_link']", min_items=None
    )
    source = NullSource()

    def process_item(self, item):
        href = XPath("@href").match_one(item)
        if not href.startswith("http"):
            href = f"https://ultrasignup.com{href}"
        return RaceResultDetail(dict(race_results_url=href, **self.input), source=href)


class RaceResultDetail(HtmlPage):
    """
    Process the main race information including individual information about the event.
    """

    example_source = "https://ultrasignup.com/results_event.aspx?did=63105"
    source = NullSource()

    def process_page(self):
        try:
            cancellation = XPath(
                "//span[contains(@class,'cancellation_text')]"
            ).match_one(self.root)
            cancellation = True
        except SelectorError:
            cancellation = False

        try:
            distance = (
                XPath("//a[@class='event_selected_link']").match_one(self.root).text
            )
        except SelectorError:
            distance = ""

        try:
            distance_results = XPath(
                "//a[@class='event_link' or @class='event_selected_link']"
            ).match(self.root)
            distance_results = {
                item.text: item.get("href") for item in distance_results
            }
        except SelectorError:
            distance_results = None

        try:
            event_date = XPath("//span[@class='event-date']").match_one(self.root).text
        except SelectorError:
            event_date = ""

        try:
            virtual = XPath("//span[contains(@class,'virtual_text')]").match_one(
                self.root
            )
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
                distance_results=distance_results,
                title=title.text,
                virtual=virtual,
                website=website,
                **self.input,
            ),
            source=f"https://ultrasignup.com/service/events.svc/results/{self.input['did']}/1/json",
        )


class ResultJsonListPage(JsonListPage):
    """
    Parse each row of our JSON results file supplemented with additional page
    information so that we know which race we have parsed.
    """

    example_source = "https://ultrasignup.com/service/events.svc/results/63478/1/json"
    source = NullSource()

    def process_item(self, item):
        return dict(**self.input, **item)


if __name__ == "__main__":
    page = RaceList()
    for e in page.do_scrape():
        print(e)
