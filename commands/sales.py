from rich.console import Console
from rich.prompt import Prompt
from rich.panel import Panel
from rich.table import Table
from rich import box
from sqlalchemy.exc import IntegrityError

from commands.general import prompt_required_input, get_current_user
from models.user import User
from models.client import Client
from models.contract import Contract
from models.event import Event
from database.database import get_db
from utils.validators import (
    validate_email,
    validate_string_length,
    validate_phone_number,
    validate_positive_amount,
    validate_positive_integer
)


console = Console()

class SalesCommand:
    def create_client():
        """Create a new client."""
        db = next(get_db())

        console.print(Panel("Create a New Client", title="Sales Command", box=box.ROUNDED))
        current_user = get_current_user()
        if not current_user:
            console.print("[red]Error:[/red] No user is currently logged in.")
            return
        current_sales_employee = db.query(User).filter(User.email == current_user['email']).first()
        sales_contact_id = current_sales_employee.user_id
        print(f"Current Sales Contact ID: {sales_contact_id}")
        name = prompt_required_input("Client Name", validate_string_length, "name", 100)
        email = prompt_required_input("Email", validate_email, "email", 120)
        phone = prompt_required_input("Phone", validate_phone_number, "phone", 20)
        company_name = prompt_required_input("Company Name", validate_string_length, "company_name", 100)

        # Create client instance
        new_client = Client(
            full_name=name,
            email=email.strip().lower(),
            phone=phone,
            company_name=company_name,
            sales_contact_id=sales_contact_id
        )

        # Save to database
        try:
            db.add(new_client)
            db.commit()
            console.print(f"[green]Client {name} created successfully![/green]")
        except IntegrityError as e:
            db.rollback()
            console.print(f"[red]Error:[/red] {e.orig}")