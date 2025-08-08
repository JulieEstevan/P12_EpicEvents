from rich.console import Console
from rich.prompt import Prompt
from rich.panel import Panel
from rich.table import Table
from rich import box
from getpass_asterisk.getpass_asterisk import getpass_asterisk as getpass

from database.database import get_db
from models.user import User
from models.client import Client
from models.contract import Contract
from models.event import Event
from utils.token import create_token, clear_token, load_token, decode_token


console = Console()

def prompt_required_input(prompt_message, validators, field_name, max_length) -> str:
    """Prompt the user for input and validate that it is not empty."""
    while True:
        user_input = Prompt.ask(f"[bold yellow]{prompt_message}[/bold yellow]").strip()
        try:
            validators(user_input, field_name, max_length)
            return user_input
        except ValueError as e:
                console.print(f"[red]Error:[/red] {e}")
                continue

def log_in() -> None:
    """Log in an existing user."""
    console.print(Panel("Log In", title="User Command", box=box.ROUNDED))
    email = Prompt.ask("[bold yellow]Email[/bold yellow]").strip().lower()
    password = getpass("Password: ")

    db = next(get_db())
    user = db.query(User).filter(User.email == email).first()
    
    if not user or not user.verify_password(password):
        console.print("[red]Error:[/red] Invalid email or password.")
        return None
    create_token(user)
    console.print(f"[green]Welcome back, {user.first_name} {user.last_name}![/green]")

def log_out() -> None:
    """Log out the current user."""
    clear_token()
    console.print("[green]You have been logged out successfully.[/green]")

def get_current_user() -> dict:
    """Get the current user from the token."""
    token = load_token()
    user = decode_token(token)
    return user

def display_clients_list():
    """Display the list of clients."""
    db = next(get_db())
    clients = db.query(Client).all()
    
    if not clients:
        console.print("[red]No clients found.[/red]")
        return
    
    table = Table(title="Clients List", box=box.ROUNDED)
    table.add_column("ID", style="cyan", no_wrap=True)
    table.add_column("Name", style="magenta")
    table.add_column("Email", style="green")
    
    for client in clients:
        table.add_row(str(client.id), client.name, client.email)
    
    console.print(table)

def display_contracts_list():
    """Display the list of contracts."""
    db = next(get_db())
    contracts = db.query(Contract).all()
    
    if not contracts:
        console.print("[red]No contracts found.[/red]")
        return
    
    table = Table(title="Contracts List", box=box.ROUNDED)
    table.add_column("ID", style="cyan", no_wrap=True)
    table.add_column("Client ID", style="magenta")
    table.add_column("Details", style="green")
    
    for contract in contracts:
        table.add_row(str(contract.id), str(contract.client_id), contract.details)
    
    console.print(table)

def display_events_list():
    """Display the list of events."""
    db = next(get_db())
    events = db.query(Event).all()
    
    if not events:
        console.print("[red]No events found.[/red]")
        return
    
    table = Table(title="Events List", box=box.ROUNDED)
    table.add_column("ID", style="cyan", no_wrap=True)
    table.add_column("Name", style="magenta")
    table.add_column("Date", style="green")
    
    for event in events:
        table.add_row(str(event.id), event.name, str(event.date))
    
    console.print(table)
