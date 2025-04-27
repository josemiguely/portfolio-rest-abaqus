from decimal import Decimal
import pandas as pd
from django.db import transaction
from investments.models import Portfolio, Price, Weight, Asset, Quantity


def load_weights_and_prices_data(
    *, file_path: str
) -> tuple[pd.DataFrame, pd.DataFrame]:
    weights_df = pd.read_excel(file_path, sheet_name="weights")
    prices_df = pd.read_excel(file_path, sheet_name="Precios")
    return weights_df, prices_df


@transaction.atomic
def import_weights_and_prices_data(
    *, dataframes: tuple[pd.DataFrame, pd.DataFrame]
) -> None:

    print("Importing weights and prices data...")

    weights_df, prices_df = dataframes
    portfolio_columns = weights_df.columns[2:]
    date_values = weights_df["Fecha"].unique()
    initial_date = date_values[0]

    print("Importing portfolios...")
    for col in portfolio_columns:
        Portfolio.objects.get_or_create(
            name=col,
            defaults={"initial_value": Decimal(1_000_000_000)},
        )

    print("Importing assets...")
    asset_names = set(weights_df["activos"].unique()) | set(prices_df.columns[1:])
    for asset_name in asset_names:
        Asset.objects.get_or_create(name=asset_name)

    print("Importing weights...")
    for _, row in weights_df.iterrows():
        asset_name = row["activos"]
        asset = Asset.objects.get(name=asset_name)
        for col in portfolio_columns:
            portfolio = Portfolio.objects.get(name=col)
            weight_value = Decimal(str(row[col]))
            Weight.objects.get_or_create(
                portfolio=portfolio,
                asset=asset,
                date=initial_date,
                defaults={"value": weight_value},
            )

    # Import Prices
    for _, row in prices_df.iterrows():
        date = row["Dates"].date()
        for asset_name in prices_df.columns[1:]:
            asset = Asset.objects.get(name=asset_name)
            price_value = Decimal(str(row[asset_name]))
            Price.objects.get_or_create(
                asset=asset, date=date, defaults={"value": price_value}
            )

@transaction.atomic
def calculate_initial_quantities():
    print("Calculating initial quantities...")
    portfolios = Portfolio.objects.all()
    for portfolio in portfolios:
        weights = Weight.objects.filter(portfolio=portfolio)
        for weight in weights:
            asset = weight.asset
            try:
                price = Price.objects.get(asset=asset, date=weight.date)
                quantity_value = (weight.value * portfolio.initial_value) / price.value
                Quantity.objects.get_or_create(
                    portfolio=portfolio,
                    asset=asset,
                    date=weight.date,
                    defaults={"value": quantity_value},
                )
            except Price.DoesNotExist:
                print(f"No price found for {asset.name} on {weight.date}")
    print("Initial quantities calculated successfully")
    return True
