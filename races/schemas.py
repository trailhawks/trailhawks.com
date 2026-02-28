from datetime import datetime

from pydantic import BaseModel, Field


class RaceAgentResult(BaseModel):
    """Structured output for race data extracted from external URLs."""

    title: str | None = Field(default=None, description="The name/title of the race event")
    annual: str | None = Field(default=None, description="Annual designation, e.g. '10th Annual' or 'Inaugural'")
    number: int | None = Field(default=None, description="The edition number of the race, e.g. 10 for '10th Annual'")
    slogan: str | None = Field(default=None, description="Race slogan or tagline")
    description: str | None = Field(default=None, description="Detailed description of the race event")
    distance: str | None = Field(default=None, description="Race distance as a string, e.g. '26.2' or '50'")
    unit: int | None = Field(
        default=None,
        description="Distance unit: 1 for Kilometers, 2 for Miles",
    )
    start_datetime: datetime | None = Field(default=None, description="Race start date and time in ISO 8601 format")
    course_map: str | None = Field(default=None, description="URL to the course map")
    cut_off: str | None = Field(default=None, description="Race cut-off time, e.g. '13 hours'")
    reg_url: str | None = Field(default=None, description="URL for race registration")
    reg_description: str | None = Field(default=None, description="Description of registration details and pricing")
    ultrasignup_id: str | None = Field(
        default=None,
        description="UltraSignup event ID (the ?did= parameter from ultrasignup.com URLs)",
    )
    awards: str | None = Field(default=None, description="Description of race awards")
    discounts: str | None = Field(default=None, description="Description of any registration discounts")
    lodging: str | None = Field(default=None, description="URL for lodging information")
    packet_pickup: str | None = Field(default=None, description="Details about packet pickup location and times")
    facebook_url: str | None = Field(default=None, description="URL to the race's Facebook page")
    facebook_event_url: str | None = Field(default=None, description="URL to the race's Facebook event page")
    race_type: int | None = Field(
        default=None,
        description="Race discipline: 1 for Run, 2 for Bike, 3 for Swim",
    )
    active: bool | None = Field(default=None, description="Whether the race is currently active")
