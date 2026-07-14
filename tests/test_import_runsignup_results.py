from races.management.commands.import_runsignup_results import (
    _bib,
    _gender,
    resolve_race_id,
    select_year_events,
)


class TestBib:
    def test_numeric(self):
        assert _bib("77") == 77
        assert _bib(77) == 77

    def test_non_numeric(self):
        assert _bib("") is None
        assert _bib(None) is None
        assert _bib("DNF") is None


class TestGender:
    def test_maps(self):
        assert _gender("M") == "Man"
        assert _gender("F") == "Woman"

    def test_unknown_blank(self):
        assert _gender(None) == ""
        assert _gender("X") == ""


class TestResolveRaceId:
    def test_from_query_string(self):
        assert resolve_race_id("https://runsignup.com/Race/Register/?raceId=162555") == 162555

    def test_no_network_when_id_present(self):
        # a raceId in the URL must be used directly (no HTTP request)
        assert resolve_race_id("https://x/?a=1&raceId=999&b=2") == 999


class TestSelectYearEvents:
    EVENTS = [
        {"event_id": 1133365, "name": "The Snake 10-Mile Trail Race", "start_time": "7/25/2026 07:00"},
        {"event_id": 981469, "name": "The Snake 10-Mile Trail Race", "start_time": "7/26/2025 07:00"},
        {"event_id": 838108, "name": "The Snake 10-Mile Trail Race", "start_time": "7/20/2024 07:00"},
    ]

    def test_picks_matching_year(self):
        assert select_year_events(self.EVENTS, 2024) == [(838108, "The Snake 10-Mile Trail Race")]

    def test_no_match(self):
        assert select_year_events(self.EVENTS, 2019) == []

    def test_multi_distance_same_year(self):
        events = [
            {"event_id": 883159, "name": "5K", "start_time": "10/5/2024 08:00"},
            {"event_id": 885699, "name": "10K", "start_time": "10/5/2024 08:00"},
            {"event_id": 700000, "name": "5K", "start_time": "10/1/2023 08:00"},
        ]
        assert select_year_events(events, 2024) == [(883159, "5K"), (885699, "10K")]
