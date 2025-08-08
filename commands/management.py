from rich.console import Console
from rich.prompt import Prompt
from rich.panel import Panel
from rich.table import Table
from rich import box
from sqlalchemy.exc import IntegrityError
from getpass_asterisk.getpass_asterisk import getpass_asterisk as getpass

from commands.general import prompt_required_input
from models.user import User, UserRole
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


class ManagementCommand:
    def create_employee():
        """Create a new employee."""
        console.print(Panel("Create a New Employee", title="Management Command", box=box.ROUNDED))
        first_name = prompt_required_input("First Name", validate_string_length, "first_name", 50)
        last_name = prompt_required_input("Last Name", validate_string_length, "last_name", 50)
        email = prompt_required_input("Email", validate_email, "email", 120)
        phone = prompt_required_input("Phone", validate_phone_number, "phone", 20)
        role = Prompt.ask(
            "[bold yellow]Role[/bold yellow] (SALES, SUPPORT, MANAGEMENT)",
            choices=[role.value for role in UserRole]
        ).strip().upper()

        # Validate password
        password = getpass("Set Password:")
        confirm_password = getpass("Confirm Password:")
        if password != confirm_password:
            console.print("[red]Error:[/red] Passwords do not match. Please try again.")
            return

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
        except IntegrityError as e:
            db.rollback()
            console.print(f"[red]Error:[/red] {e.orig}")
    
    def update_employee():
        """Update an existing employee."""
        console.print(Panel("Update Employee", title="Management Command", box=box.ROUNDED))
        email = prompt_required_input("Email of the employee to update", validate_email, "email", 120)
        db = next(get_db())
        user = db.query(User).filter(User.email == email).first()
        
        if not user:
            console.print(f"[red]Error:[/red] No employee found with email {email}.")
            return
        
        first_name = Prompt.ask("[bold yellow]First Name[/bold yellow]", default=user.first_name)
        validate_string_length(first_name, "first_name", 50)
        last_name = Prompt.ask("[bold yellow]Last Name[/bold yellow]", default=user.last_name)
        validate_string_length(last_name, "last_name", 50)
        phone = Prompt.ask("[bold yellow]Phone[/bold yellow]", default=user.phone)
        validate_phone_number(phone, "phone", 20)
        role = Prompt.ask(
            "[bold yellow]Role[/bold yellow] (SALES, SUPPORT, MANAGEMENT)",
            choices=[role.value for role in UserRole],
            default=user.role.value
        ).strip().upper()

        user.first_name = first_name
        user.last_name = last_name
        user.phone = phone
        user.role = UserRole(role)

        db.commit()
        console.print(f"[green]Employee {first_name} {last_name} updated successfully![/green]")
    
    def delete_employee():
        """Delete an existing employee."""
        console.print(Panel("Delete Employee", title="Management Command", box=box.ROUNDED))
        email = prompt_required_input("Email of the employee to delete", validate_email, "email", 120)
        db = next(get_db())
        user = db.query(User).filter(User.email == email).first()
        
        if not user:
            console.print(f"[red]Error:[/red] No employee found with email {email}.")
            return
        
        confirm = Prompt.ask(f"Are you sure you want to delete {user.first_name} {user.last_name}? (yes/no)", choices=["yes", "no"])
        if confirm.lower() == "yes":
            db.delete(user)
            db.commit()
            console.print(f"[green]Employee {user.first_name} {user.last_name} deleted successfully![/green]")
        else:
            console.print("[yellow]Deletion cancelled.[/yellow]")
    
    def display_employees():
        """Display all employees."""
        db = next(get_db())
        employees = db.query(User).filter(User.role != UserRole.ADMIN).all()
        
        if not employees:
            console.print("[red]No employees found.[/red]")
            return
        
        table = Table(title="Employees", box=box.ROUNDED)
        table.add_column("First Name", justify="left")
        table.add_column("Last Name", justify="left")
        table.add_column("Email", justify="left")
        table.add_column("Phone", justify="left")
        table.add_column("Role", justify="left")

        for employee in employees:
            table.add_row(
                employee.first_name,
                employee.last_name,
                employee.email,
                employee.phone,
                employee.role.value
            )
        
        console.print(table)

    def create_contract():
        """Create a new contract."""
        db = next(get_db())

        console.print(Panel("Create a New Contract", title="Management Command", box=box.ROUNDED))
        client_id = prompt_required_input("Client ID", validate_positive_integer, "client_id", 0)
        client = db.query(Client).filter(Client.client_id == client_id).first()
        if not client:
            console.print(f"[red]Error:[/red] No client found with ID {client_id}.")
            return
        console.print(f"Creating contract for client: {client.full_name}")
        sales_contact = db.query(User).filter(User.user_id == client.sales_contact_id).first()
        if not sales_contact:
            console.print(f"[red]Error:[/red] No sales contact found for client {client.full_name}.")
            return
        sales_contact_id = sales_contact.user_id
        console.print(f"Sales contact: {sales_contact.first_name} {sales_contact.last_name}")
        total_amount = prompt_required_input("Total Amount", validate_positive_amount, "total_amount", 0)
        remaining_amount = prompt_required_input("Remaining Amount", validate_positive_amount, "remaining_amount", 0)
        if int(remaining_amount) > int(total_amount):
            console.print("[red]Error:[/red] Remaining amount cannot be greater than total amount.")
            return
        is_signed = Prompt.ask("Is the contract signed? (yes/no)", choices=["yes", "no"]).strip().lower()
        is_signed = True if is_signed == "yes" else False

        # Create contract instance
        new_contract = Contract(
            total_amount=total_amount,
            remaining_amount=remaining_amount,
            is_signed=is_signed,
            client_id=client.client_id,
            sales_contact_id=sales_contact_id
        )

        # Save to database
        db.add(new_contract)
        try:
            db.commit()
            console.print(f"[green]Contract created successfully for client {client.full_name}![/green]")
        except IntegrityError as e:
            db.rollback()
            console.print(f"[red]Error:[/red] {e.orig}")
    
    def update_contract():
        """Update an existing contract."""
        console.print(Panel("Update Contract", title="Management Command", box=box.ROUNDED))
        contract_id = prompt_required_input("Contract ID", validate_positive_integer, "contract_id", 0)
        db = next(get_db())
        contract = db.query(Contract).filter(Contract.contract_id == contract_id).first()
        
        if not contract:
            console.print(f"[red]Error:[/red] No contract found with ID {contract_id}.")
            return
        
        total_amount = Prompt.ask("[bold yellow]Total Amount[/bold yellow]", default=contract.total_amount)
        validate_positive_amount(total_amount, "total_amount", 0)
        remaining_amount = Prompt.ask("[bold yellow]Remaining Amount[/bold yellow]", default=contract.remaining_amount)
        validate_positive_amount(remaining_amount, "remaining_amount", 0)
        if int(remaining_amount) > total_amount:
            console.print("[red]Error:[/red] Remaining amount cannot be greater than total amount.")
            return
        is_signed = Prompt.ask("Is the contract signed? (yes/no)", choices=["yes", "no"]).strip().lower()
        is_signed = True if is_signed == "yes" else False

        contract.total_amount = total_amount
        contract.remaining_amount = remaining_amount
        contract.is_signed = is_signed

        db.commit()
        console.print(f"[green]Contract {contract_id} updated successfully![/green]")
