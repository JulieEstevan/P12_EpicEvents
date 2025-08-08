import sys
from os import path
sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))

from rich.console import Console
from rich.prompt import Prompt
from rich.panel import Panel
from rich import box
from sqlalchemy.exc import IntegrityError
from getpass_asterisk.getpass_asterisk import getpass_asterisk as getpass

from commands.general import prompt_required_input
from models.user import User, UserRole
from database.database import get_db
from utils.validators import (
    validate_email,
    validate_string_length,
    validate_phone_number,
)


console = Console()


class ManagementCommand:
    def create_employee():
        """Create a new employee."""
        while True:
            console.print(Panel("Create a New Employee", title="Management Command", box=box.ROUNDED))
            first_name = prompt_required_input("First Name", validate_string_length, "first_name", 50)
            last_name = prompt_required_input("Last Name", validate_string_length, "last_name", 50)
            email = prompt_required_input("Email", validate_email, "email", 120)
            phone = prompt_required_input("Phone", validate_phone_number, "phone", 20)
            role = Prompt.ask(
                "Role (SALES, SUPPORT, MANAGEMENT)",
                choices=[role.value for role in UserRole]
            ).strip().upper()
            
            while True:
                password = getpass("Set Password:")
                confirm_password = getpass("Confirm Password:")
                if password != confirm_password:
                    console.print("[red]Error:[/red] Passwords do not match. Please try again.")
                    continue
                break

            # Create user instance
            new_user = User(
                first_name=first_name,
                last_name=last_name,
                email=email,
                phone=phone,
                role=UserRole(role),
            )
            new_user.set_password(password)

            # Save to database
            db = next(get_db())
            try:
                db.add(new_user)
                db.commit()
                console.print(f"[green]Employee {first_name} {last_name} created successfully![/green]")
                break
            except IntegrityError as e:
                db.rollback()
                console.print(f"[red]Error:[/red] {e.orig}")
