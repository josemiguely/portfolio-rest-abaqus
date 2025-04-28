from django.core.management.base import BaseCommand

from investments.services import calculate_initial_quantities


class Command(BaseCommand):
    help = "Calculate initial quantities for portfolios"

    def handle(self, *args, **kwargs):
        try:
            self.stdout.write("Running initial quantity calculation...")
            calculate_initial_quantities()
            self.stdout.write(
                self.style.SUCCESS("Successfully calculated initial quantities")
            )

        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f"Error calculating initial quantities: {str(e)}")
            )
