import plotly.express as px
import plotly.offline as opy
import plotly.graph_objects as go

import pandas as pd


def frequency_table(df):
    """Generate a one-way frequency table for manufacturers."""
    # Simple counts
    manufacturer_counts = df['manufacturer'].value_counts().reset_index()
    manufacturer_counts.columns = ['Manufacturer', 'Count']

    # Convert to HTML using the correct method name: .to_html()
    table_html = manufacturer_counts.to_html(
        classes="table table-bordered table-striped table-sm",
        float_format='%.2f',
        justify='center'
    )
    return table_html


def profit_calculation(df):
    df['profit'] = df['selling_price'] - df['wholesale_price']
    group = df.groupby(["manufacturer", "transmission","fuel_type"]).agg({
        "profit":"sum", 
        "selling_price":["sum", "count"], 
        "wholesale_price":"sum"
    })

    return group.to_html(
        classes="table table-bordered table-striped table-sm",
        float_format='%.2f',
        justify='center'
    )

def cross_tabulation(df):
    crosstab = pd.crosstab(df["manufacturer"], df["body_type"],values=df["selling_price"], aggfunc="sum" ,margins=True).round(2)

    return crosstab.to_html(
        classes="table table-bordered table-striped table-sm",
        float_format='%.2f',
        justify='center'
    )


def pivot_table(df):
    pivottable =pd.pivot_table(df, 
                                index="manufacturer", 
                                values=["selling_price", "wholesale_price"], 
                                aggfunc=["sum", "mean"])

    return pivottable.to_html(
        classes="table table-bordered table-striped table-sm",
        float_format='%.2f',
        justify='center'
    )


def visualizing_sales_with_sunburst_chart(df, height=800):
    fig = px.sunburst(df,path=["manufacturer", "fuel_type", "body_type"],values="selling_price")
    fig.update_traces(textinfo="label+value")
    fig.update_layout(height=height)
    return opy.plot(fig, output_type="div")



def frequency_barchart(df):
    """Generate a bar chart for manufacturer frequency distribution."""
    # Get manufacturer counts
    manufacturer_counts = df['manufacturer'].value_counts().reset_index()
    manufacturer_counts.columns = ['Manufacturer', 'Count']
    
    # Sort by count descending for better visualization
    manufacturer_counts = manufacturer_counts.sort_values('Count', ascending=False)
    
    # Create bar chart using Plotly
    fig = px.bar(
        manufacturer_counts,
        x='Manufacturer',
        y='Count',
        title='Manufacturer Frequency Distribution',
        labels={'Manufacturer': 'Manufacturer', 'Count': 'Number of Vehicles'},
        color='Count',
        color_continuous_scale='Blues',
        text='Count'
    )
    
    # Update layout for better appearance
    fig.update_traces(
        texttemplate='%{text}',
        textposition='outside'
    )
    
    fig.update_layout(
        xaxis_tickangle=-45,
        plot_bgcolor='white',
        paper_bgcolor='white',
        font=dict(family="Inter, sans-serif", size=12),
        showlegend=False,
        height=500,
        margin=dict(b=100)
    )
    
    # Update axes
    fig.update_xaxes(showgrid=False, showline=True, linewidth=1, linecolor='#dee2e6')
    fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor='#f1f3f5', showline=True, linewidth=1, linecolor='#dee2e6')
    
    # Convert to HTML
    chart_html = fig.to_html(
        include_plotlyjs='cdn',
        full_html=False,
        config={'displayModeBar': False}
    )
    
    return chart_html

# def sales_by_country_map(df):
 
#     # Calculate total sales per country
#     country_sales = df.groupby('client_country').agg({
#         'selling_price': 'sum',
#         'manufacturer': 'count'  # Changed from 'client_country' to any other column
#     }).reset_index()
    
#     country_sales.columns = ['Country', 'Total Sales', 'Number of Clients']
    
#     # Sort by total sales
#     country_sales = country_sales.sort_values('Total Sales', ascending=False)
    
#     # Create choropleth map
#     fig = px.choropleth(
#         country_sales,
#         locations='Country',
#         locationmode='country names',
#         color='Total Sales',
#         hover_name='Country',
#         hover_data={
#             'Total Sales': ':$,.0f', 
#             'Number of Clients': ':,.0f',
#             'Country': False
#         },
#         color_continuous_scale='Blues',
#         title='Total Sales Distribution by Country',
#         labels={'Total Sales': 'Total Sales ($)'}
#     )
    
#     fig.update_layout(
#         plot_bgcolor='white',
#         paper_bgcolor='white',
#         font=dict(family="Inter, sans-serif", size=12),
#         height=600,
#         margin=dict(t=80, b=20, l=20, r=20),
#         geo=dict(
#             showframe=False,
#             showcoastlines=True,
#             coastlinecolor='#dee2e6',
#             projection_type='natural earth',
#             bgcolor='#f8f9fa'
#         ),
#         coloraxis_colorbar=dict(
#             title="Sales ($)",
#             tickprefix="$",
#             tickformat=",.0f",
#             len=0.7
#         )
#     )
    
#     # Convert to HTML
#     chart_html = fig.to_html(
#         include_plotlyjs='cdn',
#         full_html=False,
#         config={'displayModeBar': True, 'displaylogo': False}
#     )
    
#     return chart_html



def sales_by_country_map(df):
    """Generate a world map showing total sales distribution by country with labels."""
    # Simple aggregation - just sum the sales
    country_sales = df.groupby('client_country')['selling_price'].sum().reset_index()
    country_sales.columns = ['Country', 'Total Sales']
    
    # Get counts separately
    country_counts = df['client_country'].value_counts().reset_index()
    country_counts.columns = ['Country', 'Clients']
    
    # Merge them
    country_sales = country_sales.merge(country_counts, on='Country')
    
    # Country coordinates (approximate centers)
    country_coords = {
        'Uganda': {'lat': 1.3733, 'lon': 32.2903},
        'Canada': {'lat': 56.1304, 'lon': -106.3468},
        'United States': {'lat': 37.0902, 'lon': -95.7129},
        'Zambia': {'lat': -13.1339, 'lon': 27.8493},
        'Germany': {'lat': 51.1657, 'lon': 10.4515},
        'Australia': {'lat': -25.2744, 'lon': 133.7751},
        'China': {'lat': 35.8617, 'lon': 104.1954},
        'United Kingdom': {'lat': 55.3781, 'lon': -3.4360},
        'India': {'lat': 20.5937, 'lon': 78.9629},
        'France': {'lat': 46.2276, 'lon': 2.2137},
        'Rwanda': {'lat': -1.9403, 'lon': 29.8739},
        'Burundi': {'lat': -3.3731, 'lon': 29.9189},
        'Brazil': {'lat': -14.2350, 'lon': -51.9253},
        'Japan': {'lat': 36.2048, 'lon': 138.2529},
    }
    
    # Create figure
    fig = go.Figure()
    
    # Add choropleth layer
    fig.add_trace(go.Choropleth(
        locations=country_sales['Country'],
        locationmode='country names',
        z=country_sales['Total Sales'],
        colorscale='Blues',
        colorbar=dict(
            title="Sales ($)",
            tickprefix="$",
            tickformat=",.0f",
            len=0.7,
            x=1.02
        ),
        hovertemplate='<b>%{location}</b><br>Total Sales: $%{z:,.0f}<extra></extra>',
        showscale=True
    ))
    
    # Add text labels for each country
    for _, row in country_sales.iterrows():
        country = row['Country']
        if country in country_coords:
            # Format the sales amount
            sales_formatted = f"${row['Total Sales']:,.0f}"
            
            fig.add_trace(go.Scattergeo(
                lon=[country_coords[country]['lon']],
                lat=[country_coords[country]['lat']],
                text=f"<b>{country}</b><br>{sales_formatted}",
                mode='text',
                textfont=dict(
                    size=9,
                    color='#212529',
                    family='Inter, sans-serif'
                ),
                textposition='middle center',
                hoverinfo='skip',
                showlegend=False
            ))
    
    fig.update_layout(
        title={
            'text': 'Total Sales Distribution by Country',
            'font': {'size': 16, 'family': 'Inter, sans-serif'}
        },
        plot_bgcolor='white',
        paper_bgcolor='white',
        font=dict(family="Inter, sans-serif", size=12),
        height=600,
        margin=dict(t=80, b=20, l=20, r=20),
        geo=dict(
            showframe=False,
            showcoastlines=True,
            coastlinecolor='#dee2e6',
            projection_type='natural earth',
            bgcolor='#f8f9fa',
            showland=True,
            landcolor='#f1f3f5'
        )
    )
    
    # Convert to HTML
    chart_html = fig.to_html(
        include_plotlyjs='cdn',
        full_html=False,
        config={'displayModeBar': True, 'displaylogo': False}
    )
    
    return chart_html