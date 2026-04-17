# ============================================================
# COM7021 - Data Visualisation Portfolio
# European Bakery Sales Analysis
# Farid Negahbani
# Student ID:24154844
# Run: python dashboard_app.py
# Open: http://127.0.0.1:8050
#pip install pandas plotly dash dash-bootstrap-components numpy
#python dashboard_app.py
# ============================================================

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from dash import Dash, html, dcc, callback, Output, Input

# --- Load & Prepare Data ---
df = pd.read_csv('bakery_cleaned.csv')
df['Date'] = pd.to_datetime(df['Date'])

cities = sorted(df['City'].unique())
confectioneries = sorted(df['Confectionary'].unique())

years = sorted([int(y) for y in df['Year'].unique()])

app = Dash(__name__)
app.title = "European Bakery Sales"

app.layout = html.Div([
    # ===== HEADER =====
    html.Div([
        html.H1("European Bakery Sales",
                style={'textAlign': 'center',
                       'color': '#38bdf8',
                       'marginBottom': '5px',
                       'fontSize': '28px'}),

        html.P([
            "Arden University | COM7021 Data Visualisation | Interactive Analysis | ",
            "Farid Negahbani | SID: 24154844",
            html.Br(),
            "5 Cities | 5 Confectioneries | 5 Years"
        ],
            style={'textAlign': 'center',
                   'color': '#cbd5e1',
                   'fontSize': '14px'})
    ],
        style={'backgroundColor': '#1e293b',
               'padding': '15px',
               'borderRadius': '10px',
               'marginBottom': '20px'}
    ),

    html.Div([
        html.Div([
            html.Label("Select City:", style={'fontWeight': 'bold'}),
            dcc.Dropdown(
                id='city-filter',
                options=[{'label': 'All Cities', 'value': 'ALL'}] +
                        [{'label': c, 'value': c} for c in cities],
                value='ALL', clearable=False
            )
        ], style={'width': '30%', 'display': 'inline-block', 'padding': '0 10px'}),

        html.Div([
            html.Label("Select Confectionery:", style={'fontWeight': 'bold'}),
            dcc.Dropdown(
                id='conf-filter',
                options=[{'label': 'All Types', 'value': 'ALL'}] +
                        [{'label': c, 'value': c} for c in confectioneries],
                value='ALL', clearable=False
            )
        ], style={'width': '30%', 'display': 'inline-block', 'padding': '0 10px'}),

        html.Div([
            html.Label("Year Range:", style={'fontWeight': 'bold'}),
            dcc.RangeSlider(
                id='year-slider',
                min=int(min(years)),
                max=int(max(years)),
                step=1,
                value=[int(min(years)), int(max(years))],
                marks={int(y): str(y) for y in years}
            )
        ], style={'width': '35%', 'display': 'inline-block', 'padding': '0 10px'})
    ], style={'marginBottom': '20px'}),

    # KPI
    html.Div(id='kpi-cards', style={
        'display': 'flex', 'justifyContent': 'space-around', 'marginBottom': '20px'
    }),

    # Charts Row 1
    html.Div([
        html.Div([dcc.Graph(id='chart-profit-city')],
                 style={'width': '50%', 'display': 'inline-block'}),
        html.Div([dcc.Graph(id='chart-profit-conf')],
                 style={'width': '50%', 'display': 'inline-block'})
    ]),

    # Charts Row 2
    html.Div([
        html.Div([dcc.Graph(id='chart-temporal')],
                 style={'width': '50%', 'display': 'inline-block'}),
        html.Div([dcc.Graph(id='chart-scatter')],
                 style={'width': '50%', 'display': 'inline-block'})
    ]),

    # Charts Row 3
    html.Div([
        html.Div([dcc.Graph(id='chart-heatmap')],
                 style={'width': '50%', 'display': 'inline-block'}),
        html.Div([dcc.Graph(id='chart-treemap')],
                 style={'width': '50%', 'display': 'inline-block'})
    ])

], style={'fontFamily': 'Arial, sans-serif', 'padding': '20px',
          'maxWidth': '1400px', 'margin': '0 auto'})


def filter_data(city, conf, year_range):
    dff = df.copy()
    if city != 'ALL':
        dff = dff[dff['City'] == city]
    if conf != 'ALL':
        dff = dff[dff['Confectionary'] == conf]
    dff = dff[(dff['Year'] >= year_range[0]) & (dff['Year'] <= year_range[1])]
    return dff


@callback(Output('kpi-cards', 'children'),
          Input('city-filter', 'value'),
          Input('conf-filter', 'value'),
          Input('year-slider', 'value'))
def update_kpis(city, conf, year_range):
    dff = filter_data(city, conf, year_range)
    total_rev = dff['Revenue(£)'].sum()
    total_profit = dff['Profit(£)'].sum()
    avg_margin = (total_profit / total_rev * 100) if total_rev > 0 else 0
    total_units = dff['Units Sold'].sum()


    total_rev = float(total_rev)
    total_profit = float(total_profit)
    avg_margin = float(avg_margin)
    total_units = float(total_units)

    def kpi_card(title, value, color):
        return html.Div([
            html.H4(title, style={'color': '#7f8c8d', 'margin': '0', 'fontSize': '13px'}),
            html.H2(value, style={'color': color, 'margin': '5px 0', 'fontSize': '22px'})
        ], style={'textAlign': 'center', 'backgroundColor': 'white',
                  'padding': '15px', 'borderRadius': '10px',
                  'boxShadow': '0 2px 5px rgba(0,0,0,0.1)', 'width': '22%'})

    return [
        kpi_card("Total Revenue", f"£{total_rev:,.0f}", "#2196F3"),
        kpi_card("Total Profit", f"£{total_profit:,.0f}", "#4CAF50"),
        kpi_card("Avg Margin", f"{avg_margin:.1f}%", "#FF9800"),
        kpi_card("Units Sold", f"{total_units:,.0f}", "#9C27B0")
    ]


@callback(Output('chart-profit-city', 'figure'),
          Input('city-filter', 'value'),
          Input('conf-filter', 'value'),
          Input('year-slider', 'value'))
def update_profit_city(city, conf, year_range):
    dff = filter_data(city, conf, year_range)
    data = dff.groupby('City')['Profit(£)'].sum().sort_values(ascending=True).reset_index()
    fig = px.bar(data, x='Profit(£)', y='City', orientation='h',
                 color='Profit(£)', color_continuous_scale='RdYlGn',
                 title='Profit by City')
    fig.update_layout(template='plotly_white', height=350, showlegend=False)
    return fig


@callback(Output('chart-profit-conf', 'figure'),
          Input('city-filter', 'value'),
          Input('conf-filter', 'value'),
          Input('year-slider', 'value'))
def update_profit_conf(city, conf, year_range):
    dff = filter_data(city, conf, year_range)
    data = dff.groupby('Confectionary')['Profit(£)'].sum().sort_values(ascending=False).reset_index()
    fig = px.bar(data, x='Confectionary', y='Profit(£)',
                 color='Confectionary', title='Profit by Confectionery')
    fig.update_layout(template='plotly_white', height=350, showlegend=False)
    return fig


@callback(Output('chart-temporal', 'figure'),
          Input('city-filter', 'value'),
          Input('conf-filter', 'value'),
          Input('year-slider', 'value'))
def update_temporal(city, conf, year_range):
    dff = filter_data(city, conf, year_range)
    data = dff.groupby(['Year', 'City'])['Profit(£)'].sum().reset_index()

    data['Year'] = data['Year'].astype(int)
    fig = px.line(data, x='Year', y='Profit(£)', color='City',
                  markers=True, title='Yearly Profit Trends')
    fig.update_layout(template='plotly_white', height=350)
    return fig


@callback(Output('chart-scatter', 'figure'),
          Input('city-filter', 'value'),
          Input('conf-filter', 'value'),
          Input('year-slider', 'value'))
def update_scatter(city, conf, year_range):
    dff = filter_data(city, conf, year_range)
    fig = px.scatter(dff, x='Revenue(£)', y='Profit(£)',
                     color='City', hover_data=['Confectionary', 'Units Sold'],
                     title='Revenue vs Profit', opacity=0.6)
    fig.update_layout(template='plotly_white', height=350)
    return fig


@callback(Output('chart-heatmap', 'figure'),
          Input('city-filter', 'value'),
          Input('conf-filter', 'value'),
          Input('year-slider', 'value'))
def update_heatmap(city, conf, year_range):
    dff = filter_data(city, conf, year_range)
    pivot = dff.pivot_table(values='Profit_Margin(%)', index='City',
                            columns='Confectionary', aggfunc='mean')


    pivot = pivot.fillna(0).round(1)
    pivot.index = pivot.index.astype(str)
    pivot.columns = pivot.columns.astype(str)

    fig = px.imshow(pivot, text_auto='.1f', color_continuous_scale='RdYlGn',
                    title='Profit Margin % Heatmap', aspect='auto')
    fig.update_layout(height=350)
    return fig


@callback(Output('chart-treemap', 'figure'),
          Input('city-filter', 'value'),
          Input('conf-filter', 'value'),
          Input('year-slider', 'value'))
def update_treemap(city, conf, year_range):
    dff = filter_data(city, conf, year_range)
    data = dff.groupby(['City', 'Confectionary'])['Profit(£)'].sum().reset_index()

    if data.empty:
        fig = go.Figure()
        fig.update_layout(height=350, title='Profit Treemap (No Data)')
        return fig

    fig = px.treemap(data, path=['City', 'Confectionary'], values='Profit(£)',
                     color='Profit(£)', color_continuous_scale='RdYlGn',
                     title='Profit Treemap')
    fig.update_layout(height=350)
    return fig


if __name__ == '__main__':
    print("Dashboard running at http://127.0.0.1:8050")
    app.run(debug=True)