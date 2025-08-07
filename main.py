import typer

from commands import general, management
from utils import token

app = typer.Typer()

@app.command()
def log_in():
    """Log in an existing user."""
    general.log_in()

@app.command()
def get_current_user():
    """Get the current user from the token."""
    is_token_file_exists = token.TOKEN_FILE.exists()
    if not is_token_file_exists:
        typer.echo("You must log in first.")
        raise typer.Exit()
    user = token.get_current_user()
    typer.echo(f"Current user: {user['email']} with role {user['role']}")

@app.command()
def create_employee():
    """Create a new employee."""
    management.ManagementCommand.create_employee()

if __name__ == "__main__":
    app()
