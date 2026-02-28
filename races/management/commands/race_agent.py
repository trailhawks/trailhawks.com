import typer
from django_typer.management import TyperCommand
from rich.console import Console
from rich.table import Table

from races.agents import apply_race_changes, compute_race_diff, run_race_agent
from races.models import Race


class Command(TyperCommand):
    help = "Fetch race information from a URL using an AI agent and update a Race."

    def handle(
        self,
        race_pk: int = typer.Argument(help="Primary key of the Race to update"),
        url: str | None = typer.Argument(
            default=None, help="URL to fetch race information from (defaults to race reg_url)"
        ),
        dry_run: bool = typer.Option(False, "--dry-run", help="Show changes without applying"),
        apply: bool = typer.Option(False, "--apply", help="Apply changes without confirmation"),
    ):
        console = Console()

        try:
            race = Race.objects.get(pk=race_pk)
        except Race.DoesNotExist:
            console.print(f"[red]Race with pk={race_pk} not found.[/red]")
            raise typer.Exit(code=1)

        if not url:
            url = race.reg_url
            if not url:
                console.print("[red]No URL provided and race has no reg_url set.[/red]")
                raise typer.Exit(code=1)

        console.print(f"[bold]Race:[/bold] {race}")
        console.print(f"[bold]URL:[/bold] {url}")
        console.print()

        with console.status("Fetching and analyzing race data..."):
            result = run_race_agent(url)

        changes = compute_race_diff(race, result)

        if not changes:
            console.print("[green]No changes detected.[/green]")
            return

        table = Table(title="Proposed Changes")
        table.add_column("Field", style="cyan")
        table.add_column("Current", style="red")
        table.add_column("New", style="green")

        for field, (old, new) in changes.items():
            old_str = str(old) if old is not None else "(empty)"
            new_str = str(new) if new is not None else "(empty)"
            if len(old_str) > 80:
                old_str = old_str[:80] + "..."
            if len(new_str) > 80:
                new_str = new_str[:80] + "..."
            table.add_row(field, old_str, new_str)

        console.print(table)
        console.print()

        if dry_run:
            console.print("[yellow]Dry run — no changes applied.[/yellow]")
            return

        if not apply:
            confirmed = typer.confirm("Apply these changes?")
            if not confirmed:
                console.print("[yellow]Cancelled.[/yellow]")
                return

        apply_race_changes(race, changes)
        console.print(f"[green]Applied {len(changes)} change(s) to {race}.[/green]")
