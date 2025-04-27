from django.core.management.base import BaseCommand, CommandError
from investments.services import (
    load_weights_and_prices_data,
    import_weights_and_prices_data,
)


class Command(BaseCommand):
    help = "Loads portfolio data from an excel file into the database"
    DEFAULT_FILE_PATH = "investments/datos.xlsx"

    def add_arguments(self, parser):
        parser.add_argument("--file_path", help="path to excel file")

    def handle(self, *args, **kwargs):
        file_path = kwargs.get("file_path") or self.DEFAULT_FILE_PATH
        try:
            weighs_and_prices_dfs = load_weights_and_prices_data(file_path=file_path)
            import_weights_and_prices_data(dataframes=weighs_and_prices_dfs)
            self.stdout.write(
                self.style.SUCCESS(f"Successfully loaded {file_path} into the database")
            )
        except Exception as e:
            self.stdout.write(f"Couldnt load {file_path} into the database")
            self.stdout.write(self.style.ERROR(str(e)))
