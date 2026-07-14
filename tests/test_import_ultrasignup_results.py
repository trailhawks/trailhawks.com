from races.management.commands.import_ultrasignup_results import (
    _bib,
    _clean_time,
    parse_distances,
)


class TestCleanTime:
    def test_blank_placeholders(self):
        assert _clean_time("") == ""
        assert _clean_time("0") == ""
        assert _clean_time("00") == ""

    def test_pads_single_digit_hour(self):
        # 7-char H:MM:SS times are zero-padded to HH:MM:SS for consistency
        assert _clean_time("9:59:59") == "09:59:59"
        assert _clean_time("1:56:22") == "01:56:22"

    def test_leaves_two_digit_hour(self):
        assert _clean_time("12:34:56") == "12:34:56"


class TestBib:
    def test_numeric(self):
        assert _bib("1614") == 1614
        assert _bib(1614) == 1614

    def test_non_numeric_is_none(self):
        assert _bib("") is None
        assert _bib(None) is None
        assert _bib("N/A") is None


def _page(distance_names, dids, this_did):
    """Minimal stand-in for an UltraSignup results_event page."""
    tabs = " | ".join(f"<a href='/results_event.aspx?did={d}'>x</a>" for d in dids)
    # include unrelated history dids to prove they're ignored
    history = "".join(f"<a href='/results_event.aspx?did={d}'>y</a>" for d in (12054, 999999))
    return f'<span class="distances">{", ".join(distance_names)}</span>{tabs}{history}<a href="./results_event.aspx?did={this_did}">self</a>'


class TestParseDistances:
    def test_multi_distance_consecutive(self):
        # The Hawk: 4 consecutive distance dids
        html = _page(["100 Miler", "50 Miler", "100 Miler Pacer", "Marathon"], [52373, 52374, 52375, 52376], 52373)
        assert parse_distances(html, 52373) == [
            ("100 Miler", 52373),
            ("50 Miler", 52374),
            ("100 Miler Pacer", 52375),
            ("Marathon", 52376),
        ]

    def test_stored_did_not_first(self):
        # stored id is the middle distance; siblings still discovered both directions
        html = _page(["100 Miler", "50 Miler", "Marathon"], [52373, 52374, 52375], 52374)
        assert parse_distances(html, 52374) == [
            ("100 Miler", 52373),
            ("50 Miler", 52374),
            ("Marathon", 52375),
        ]

    def test_single_distance(self):
        html = _page(["10 Miler"], [102084], 102084)
        assert parse_distances(html, 102084) == [("10 Miler", 102084)]

    def test_history_dids_ignored(self):
        # 12054 / 999999 are prior-year events, not consecutive with the run
        html = _page(["5K"], [86850], 86850)
        assert parse_distances(html, 86850) == [("5K", 86850)]

    def test_name_count_mismatch_falls_back(self):
        # 2 tabs but only 1 name -> second distance labelled None, not dropped
        html = _page(["50K"], [90349, 90350], 90349)
        result = parse_distances(html, 90349)
        assert result == [("50K", 90349), (None, 90350)]
