from .models.models import create_tables
from .cli.cli import cli_app

def main():
    create_tables()
    cli_app()

if __name__ == "__main__":
    main()
