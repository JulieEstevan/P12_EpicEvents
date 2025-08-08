import typer
from rich import print
from rich.prompt import Prompt
from commands import general, management
from utils import token, permissions

app = typer.Typer()

@app.command()
def log_in():
    """Log in an existing user."""
    if token.TOKEN_FILE.exists() and token.load_token():
        print("[red]You are already logged in. Please log out first.[/red]")
        raise typer.Exit()
    general.log_in()

@app.command()
def log_out():
    """Log out the current user."""
    if not token.TOKEN_FILE.exists() or not token.load_token():
        print("[red]You are not logged in. Please log in first.[/red]")
        raise typer.Exit()
    general.log_out()

@app.command()
def display_lists():
    """Display the list of clients, contracts, or events based on user choice, if a user is connected."""
    if not token.TOKEN_FILE.exists() or not token.load_token():
        print("[red]You must be logged in to display lists.[/red]")
        raise typer.Exit()
    choice = Prompt.ask(
        "Which list would you like to display?",
        choices=["clients", "contracts", "events"],
        default="clients"
    ).strip().lower()
    if choice == 'clients':
        general.display_clients_list()
    elif choice == 'contracts':
        general.display_contracts_list()
    elif choice == 'events':
        general.display_events_list()

@app.command()
def create_employee():
    """Create a new employee."""
    if not permissions.has_permission("create_employee"):
        print("[red]You do not have permission to create an employee.[/red]")
        raise typer.Exit()
    management.ManagementCommand.create_employee()

if __name__ == "__main__":
    app()
