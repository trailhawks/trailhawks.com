import asyncio

import httpx
from django.conf import settings
from pydantic_ai import Agent

from .schemas import RaceAgentResult


SYSTEM_PROMPT = """\
You are a race data extraction agent. Given the HTML content of a race registration \
or information page (from UltraSignup, RunSignUp, or similar sites), extract structured \
race data.

Rules:
- Only extract data that is clearly present on the page.
- Leave fields as null if the information is not found.
- For 'unit', use 1 for Kilometers and 2 for Miles.
- For 'race_type', use 1 for Run, 2 for Bike, 3 for Swim.
- For 'start_datetime', provide a full ISO 8601 datetime string.
- For 'ultrasignup_id', extract just the numeric ID from UltraSignup URLs (the ?did= parameter).
- For text fields like 'description', 'awards', 'reg_description', 'packet_pickup', \
and 'discounts', use plain text (not HTML or markdown).
"""


def get_race_agent() -> Agent[None, RaceAgentResult]:
    return Agent(
        settings.AI_MODEL,
        system_prompt=SYSTEM_PROMPT,
        output_type=RaceAgentResult,
    )


async def fetch_url_content(url: str) -> str:
    async with httpx.AsyncClient(follow_redirects=True, timeout=30.0) as client:
        response = await client.get(url)
        response.raise_for_status()
        return response.text[:100_000]


async def _run_race_agent(url: str) -> RaceAgentResult:
    content = await fetch_url_content(url)
    agent = get_race_agent()
    result = await agent.run(f"Extract race data from the following page content:\n\n{content}")
    return result.output


def run_race_agent(url: str) -> RaceAgentResult:
    return asyncio.run(_run_race_agent(url))


COMPARE_FIELDS = [
    "title",
    "annual",
    "number",
    "slogan",
    "description",
    "distance",
    "unit",
    "start_datetime",
    "course_map",
    "cut_off",
    "reg_url",
    "reg_description",
    "ultrasignup_id",
    "awards",
    "discounts",
    "lodging",
    "packet_pickup",
    "facebook_url",
    "facebook_event_url",
    "race_type",
    "active",
]


def compute_race_diff(race, result: RaceAgentResult) -> dict:
    """Compare agent result to a Race instance, return {field: (old, new)} for changed fields."""
    changes = {}
    for field in COMPARE_FIELDS:
        new_value = getattr(result, field)
        if new_value is None:
            continue
        old_value = getattr(race, field)
        if old_value != new_value:
            changes[field] = (old_value, new_value)
    return changes


def apply_race_changes(race, changes: dict) -> None:
    """Apply a diff dict to a Race instance and save."""
    if not changes:
        return
    update_fields = []
    for field, (_old, new) in changes.items():
        setattr(race, field, new)
        update_fields.append(field)
    race.save(update_fields=update_fields)


CHAT_SYSTEM_PROMPT = """\
You are a helpful race management assistant for the Lawrence Trail Hawks running club. \
You help staff members view and update race information.

You have access to the following race data:
{race_context}

When the user asks to update a field, respond with a JSON block in the following format \
so the system can parse it:
```json
{{"updates": {{"field_name": "new_value", ...}}}}
```

Available fields you can update: title, annual, number, slogan, description, distance, \
unit (1=Kilometers, 2=Miles), start_datetime (ISO 8601), course_map, cut_off, reg_url, \
reg_description, ultrasignup_id, awards, discounts, lodging, packet_pickup, facebook_url, \
facebook_event_url, race_type (1=Run, 2=Bike, 3=Swim), active (true/false).

If the user asks a question about the race, answer based on the data provided. \
If the user asks to change something, include the JSON update block in your response. \
Be concise and helpful.
"""


def format_race_context(race) -> str:
    """Format a Race instance into a text summary for the chat agent."""
    unit_display = dict(race.UNIT_CHOICES).get(race.unit, "Unknown")
    race_type_display = dict(race.DISCIPLINE_CHOICES).get(race.race_type, "Unknown")
    lines = [
        f"Title: {race.title}",
        f"Annual: {race.annual or '(not set)'}",
        f"Number: {race.number or '(not set)'}",
        f"Slogan: {race.slogan or '(not set)'}",
        f"Description: {race.description or '(not set)'}",
        f"Distance: {race.distance or '(not set)'} {unit_display}",
        f"Start: {race.start_datetime}",
        f"Course Map: {race.course_map or '(not set)'}",
        f"Cut Off: {race.cut_off or '(not set)'}",
        f"Registration URL: {race.reg_url or '(not set)'}",
        f"Registration Description: {race.reg_description or '(not set)'}",
        f"UltraSignup ID: {race.ultrasignup_id or '(not set)'}",
        f"Awards: {race.awards or '(not set)'}",
        f"Discounts: {race.discounts or '(not set)'}",
        f"Lodging: {race.lodging or '(not set)'}",
        f"Packet Pickup: {race.packet_pickup or '(not set)'}",
        f"Facebook URL: {race.facebook_url or '(not set)'}",
        f"Facebook Event URL: {race.facebook_event_url or '(not set)'}",
        f"Race Type: {race_type_display}",
        f"Active: {race.active}",
    ]
    return "\n".join(lines)


def get_chat_agent(race) -> Agent:
    race_context = format_race_context(race)
    return Agent(
        settings.AI_MODEL,
        system_prompt=CHAT_SYSTEM_PROMPT.format(race_context=race_context),
    )


def run_chat_agent(race, message: str) -> str:
    agent = get_chat_agent(race)
    result = asyncio.run(agent.run(message))
    return result.output
