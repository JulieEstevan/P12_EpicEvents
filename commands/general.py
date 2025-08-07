from rich.console import Console
from rich.prompt import Prompt
from rich.panel import Panel
from rich import box
from getpass import getpass

from database.database import get_db
from models.user import User, UserRole
from utils.token import create_token


console = Console()

def prompt_required_input(prompt_message, validators, field_name, max_length):
    """Prompt the user for input and validate that it is not empty."""
    while True:
        user_input = Prompt.ask(f"[bold yellow]{prompt_message}[/bold yellow]").strip()
        try:
            validators(user_input, field_name, max_length)
            return user_input
        except ValueError as e:
                console.print(f"[red]Error:[/red] {e}")
                continue

def log_in():
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