import pandas as pd
import plotly.graph_objects as go
from dash import Dash, dcc, html, Input, Output, State

import simulate_investment  # Import your simulation function

app = Dash(__name__)

# App Layout
app.layout = html.Div([
    html.H1("Investing Learning Dashboard", style={'text-align': 'center'}),

    # Two sections side by side
    html.Div([
        html.Div([
            html.Label('Select Profile'),
            dcc.Dropdown(
                options=[
                    {'label': 'Random', 'value': 'random'},
                    {'label': 'Losing', 'value': 'losing'},
                    {'label': 'First', 'value': 'first'}
                ],
                value='random',
                id='slct_profile',
                style={'width': '100%'}
            ),

            html.Br(),
            html.Label('Select Asset'),
            dcc.Dropdown(
                options=[
                    {'label': 'S&P500', 'value': '^GSPC'},
                    {'label': 'NASDAQ', 'value': '^IXIC'},
                    {'label': 'GOLD', 'value': 'GC=F'}
                ],
                value='^GSPC',
                id='slct_asset',
                style={'width': '100%'}
            ),
        ], style={'padding': 10, 'flex': 1}),

        html.Div([
            html.Div([
                html.Label('Initial Investment', style={'width': '150px', 'display': 'inline-block'}),
                dcc.Input(id='my_initial_inv', type='number', placeholder="Initial Investment", value=1000, style={'width': '200px'})
            ], style={'display': 'flex', 'align-items': 'center', 'margin-bottom': '10px'}),

            html.Div([
                html.Label('Monthly Investment', style={'width': '150px', 'display': 'inline-block'}),
                dcc.Input(id='my_monthly_inv', type='number', placeholder="Monthly Investment", value=200, style={'width': '200px'})
            ], style={'display': 'flex', 'align-items': 'center', 'margin-bottom': '10px'}),

            html.Div([
                html.Label('Years to Invest', style={'width': '150px', 'display': 'inline-block'}),
                dcc.Input(id='my_year_count', type='number', placeholder="Years to Invest", value=10, style={'width': '200px'})
            ], style={'display': 'flex', 'align-items': 'center', 'margin-bottom': '10px'}),
        ], style={'padding': 10, 'flex': 1}),
    ], style={'display': 'flex', 'flexDirection': 'row', 'justify-content': 'center'}),

    html.Br(),

    # Submit Button
    html.Button('Submit', id='submit-btn', n_clicks=0, style={'display': 'block', 'margin': 'auto'}),

    html.Br(),

    # Output & Graph Section
    html.Div(id='output_container', children=[], style={'text-align': 'center'}),

    dcc.Graph(id='line_chart')  # Graph at the bottom
])


# Callback for updating graph
@app.callback(
    [Output('output_container', 'children'),
     Output('line_chart', 'figure')],
    [Input('submit-btn', 'n_clicks')],
    [State('slct_profile', 'value'),
     State('slct_asset', 'value'),
     State('my_initial_inv', 'value'),
     State('my_monthly_inv', 'value'),
     State('my_year_count', 'value')],
    prevent_initial_call=True  # Prevent auto-running on page load
)
def update_graph(n_clicks, profile, asset, initial, monthly, years):
    # Check for missing inputs
    if not all([profile, asset, initial, monthly, years]):
        return "Please fill all fields.", go.Figure()

    container = f"Profile: {profile}, Asset: {asset}"

    # Debugging: Print selections
    print(f"Profile: {profile}, Asset: {asset}, Initial: {initial}, Monthly: {monthly}, Years: {years}")

    # Try simulating investment
    try:
        # Ensure this function exists and works as expected
        portfolio_dates, portfolio_values, total_invested = simulate_investment.simulate_investment(asset, initial, monthly, profile, years)

        # Create graph
        fig = go.Figure([ 
            go.Scatter(x=portfolio_dates, y=portfolio_values, mode='lines', name='Portfolio Value'),
            go.Scatter(x=portfolio_dates, y=total_invested, mode='lines', name='Total Invested')
        ])

        return container, fig

    except Exception as e:
        print(f"Error in simulation: {e}")
        return f"Error fetching data: {str(e)}", go.Figure()


# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
