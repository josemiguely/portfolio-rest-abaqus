from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from investments.models import Portfolio, Price, Quantity
from decimal import Decimal
from datetime import datetime

class PortfolioMetricsView(APIView):
    def get(self, request):
        fecha_inicio = request.query_params.get("fecha_inicio")
        fecha_fin = request.query_params.get("fecha_fin")
        portfolio_name = request.query_params.get("portfolio", "portafolio 1")

        try:
            fecha_inicio = datetime.strptime(fecha_inicio, "%Y-%m-%d").date()
            fecha_fin = datetime.strptime(fecha_fin, "%Y-%m-%d").date()
        except (ValueError, TypeError):
            return Response(
                {"error": "Invalid date format. Use YYYY-MM-DD."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            portfolio = Portfolio.objects.get(name=portfolio_name)
        except Portfolio.DoesNotExist:
            return Response(
                {"error": f"Portfolio {portfolio_name} not found."},
                status=status.HTTP_404_NOT_FOUND,
            )

        # Get initial date from Quantity
        initial_date = (
            Quantity.objects.filter(portfolio=portfolio).order_by("date").first().date
        )

        # Get quantities with prefetched assets
        quantities = Quantity.objects.filter(
            portfolio=portfolio, date=initial_date
        ).select_related("asset")

        # Get unique dates and prices with prefetched assets
        asset_ids = [q.asset_id for q in quantities]
        prices = (
            Price.objects.filter(
                date__gte=fecha_inicio, date__lte=fecha_fin, asset_id__in=asset_ids
            )
            .select_related("asset")
            .order_by("date")
        )

        prices_by_date = {}
        for price in prices:
            date_key = price.date
            if date_key not in prices_by_date:
                prices_by_date[date_key] = []
            prices_by_date[date_key].append(price)

        # Calculate metrics
        results = []
        dates = sorted(prices_by_date.keys())
        for date in dates:
            daily_prices = prices_by_date[date]
            portfolio_value = Decimal(0)
            weights = []

            for quantity in quantities:
                price_found = False
                for price in daily_prices:
                    if price.asset_id == quantity.asset_id:
                        # x_i,t = p_i,t * c_i,0
                        amount = price.value * quantity.value
                        portfolio_value += amount
                        weights.append(
                            {
                                "asset": quantity.asset.name,
                                "amount": float(amount),
                                "weight": 0,  # Will be updated after calculating V_t
                            }
                        )
                        price_found = True
                        break
                if not price_found:
                    print(
                        f"No price found for {quantity.asset.name} on {date}. Skipping..."
                    )

            # Update weights: w_i,t = x_i,t / V_t
            for weight in weights:
                if portfolio_value > 0:
                    weight["weight"] = float(
                        Decimal(str(weight["amount"])) / portfolio_value
                    )
                else:
                    weight["weight"] = 0

            results.append(
                {
                    "date": date.strftime("%Y-%m-%d"),
                    "portfolio_value": float(portfolio_value),
                    "weights": weights,
                }
            )
        # TODO: ADD serializer and paginate response
        return Response(
            {"portfolio_name": portfolio_name, "results": results, },
            status=status.HTTP_200_OK,
        )
