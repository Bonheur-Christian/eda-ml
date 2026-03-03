import pandas as pd
from django.shortcuts import render
from .dashboard import frequency_table, profit_calculation, cross_tabulation, pivot_table,visualizing_sales_with_sunburst_chart, frequency_barchart, sales_by_country_map


def dashboard_view(request):
    """Main dashboard view that loads vehicle data and renders charts."""
    queryset = pd.read_csv("dummy_data/vehicles_data_1000.csv")
    df = pd.DataFrame(queryset)

    return render(request, "vehicles/index.html", {
        "frequency_table": frequency_table(df),
        "profit_calculation":profit_calculation(df), 
        "cross_tabulation":cross_tabulation(df),
        "pivot_table":pivot_table(df),
        "visualizing_sales_with_sunburst_chart":visualizing_sales_with_sunburst_chart(df),
        "frequency_barchart":frequency_barchart(df),
        "sales_by_country_map":sales_by_country_map(df)

    })
