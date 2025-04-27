import pandas as pd
from django.db import transaction

def load_weights_and_prices_data(
    *, file_path: str
) -> tuple[pd.DataFrame, pd.DataFrame]:
    weights_df = pd.read_excel(file_path, sheet_name="weights")
    prices_df = pd.read_excel(file_path, sheet_name="Precios")
    return weights_df, prices_df


@transaction.atomic
def import_weights_and_prices_data(*, dataframes: tuple[pd.DataFrame, pd.DataFrame]):
    print("Importing weights and prices data...")
    print("Finished importing weights and prices data")
