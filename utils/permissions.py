from rich.console import Console
from models.user import UserRole
from commands.general import get_current_user

ROLE_PERMISSIONS = {
    "MANAGEMENT": {
        "create_employee",
        "update_employee",
        "delete_employee",
        "create_contract",
        "update_contract",
        "update_event"
    },
    "SALES": {
        "create_client",
        "update_client",
        "update_contract",
        "contracts_list",
        "create_event"
    },
    "SUPPORT": {
        "events_list",
        "update_event"
    },
}

console = Console()

def get_user_role() -> UserRole:
    """Get the role of the current user."""
    user = get_current_user()
    if not user:
        console.print("[red]Error:[/red] No user is currently logged in.")
        return None
    role = UserRole(user['role'])
    console.print(f"[bold yellow]Current user role:[/bold yellow] {role.value}")
    return role

def has_permission(permission: str) -> bool:
    """Check if the current user has the specified permission."""
    role = get_user_role()
    if not role:
        return False
    permissions = ROLE_PERMISSIONS.get(role.value, set())
    if permission in permissions:
        console.print(f"[green]Permission granted:[/green] {permission}")
        return True
    else:
        console.print(f"[red]Permission denied:[/red] {permission}")
        return False
