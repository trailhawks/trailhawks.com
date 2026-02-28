import typer
from django_typer.management import TyperCommand
from rich.console import Console

import httpx

from races.models import Race
from runs.models import Run


RACE_FIELDS = [
    "title",
    "slug",
    "description",
    "distance",
    "start_datetime",
    "annual",
    "number",
    "slogan",
    "race_type",
    "unit",
    "active",
    "awards",
    "cut_off",
    "course_map",
    "reg_url",
    "reg_description",
    "ultrasignup_id",
    "discounts",
    "lodging",
    "packet_pickup",
    "facebook_url",
    "facebook_event_url",
]

RUN_FIELDS = [
    "name",
    "slug",
    "day_of_week",
    "run_time",
    "details",
    "active",
]


class Command(TyperCommand):
    help = "Sync races and runs from the production Trail Hawks API."

    def handle(
        self,
        base_url: str = typer.Argument(default="https://trailhawks.com", help="Base URL of the Trail Hawks site"),
        races: bool = typer.Option(True, "--races/--no-races", help="Sync races"),
        runs: bool = typer.Option(True, "--runs/--no-runs", help="Sync runs"),
        dry_run: bool = typer.Option(False, "--dry-run", help="Show what would be synced without making changes"),
    ):
        console = Console()
        client = httpx.Client(base_url=base_url, timeout=30)

        if races:
            self._sync_model(client, console, dry_run, "races", Race, RACE_FIELDS, "title")

        if runs:
            self._sync_model(client, console, dry_run, "runs", Run, RUN_FIELDS, "name")

    def _sync_model(self, client, console, dry_run, endpoint, model, fields, label_field):
        label = endpoint.title()
        console.print(f"[bold]Fetching {endpoint}...[/bold]")

        try:
            response = client.get(f"/api/{endpoint}/")
            response.raise_for_status()
        except httpx.HTTPStatusError as exc:
            console.print(f"  [red]API returned {exc.response.status_code} for /api/{endpoint}/ — skipping.[/red]")
            console.print(f"  [red]You may need to deploy schema changes to production first.[/red]")
            return

        data = response.json()
        console.print(f"  Found {len(data)} {endpoint} from API")

        created = 0
        updated = 0

        for item in data:
            defaults = {}
            for field in fields:
                if field in item:
                    defaults[field] = item[field]

            obj_id = item["id"]
            name = defaults.get(label_field, "Unknown")

            if dry_run:
                exists = model.objects.filter(id=obj_id).exists()
                action = "update" if exists else "create"
                console.print(f"  [dim]Would {action}:[/dim] {name} (id={obj_id})")
                if exists:
                    updated += 1
                else:
                    created += 1
            else:
                _, was_created = model.objects.update_or_create(id=obj_id, defaults=defaults)
                if was_created:
                    created += 1
                    console.print(f"  [green]Created:[/green] {name} (id={obj_id})")
                else:
                    updated += 1
                    console.print(f"  [yellow]Updated:[/yellow] {name} (id={obj_id})")

        prefix = "[bold blue]DRY RUN[/bold blue] " if dry_run else ""
        console.print(f"\n{prefix}{label}: {created} created, {updated} updated\n")
