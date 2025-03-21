import pandas as pd
import plotly.graph_objects as go
from dash import Dash, dcc, html, Input, Output, State, callback_context
import dash  # Needed for callback_context
import simulate_investment  # Import your simulation function

# Initialize the app
app = Dash(__name__)

# App Layout
app.layout = html.Div([
    html.H1("Investing Learning Dashboard", style={'text-align': 'center'}),

    # Two sections side by side
    html.Div([
        html.Div([
            html.Label('Select Profile', style={'margin-bottom': '5px', 'display': 'block'}),
            dcc.Dropdown(
                options=[
                    {'label': 'Random', 'value': 'random'},
                    {'label': 'Losing', 'value': 'losing'},
                    {'label': 'First', 'value': 'first'}
                ],
                value='random',
                id='slct_profile',
                style={'width': '200%'}
            ),
            html.Br(),
            html.Label('Select Asset', style={'margin-bottom': '5px', 'display': 'block'}),
            dcc.Dropdown(
                options=[
                    {'label': 'S&P500', 'value': '^GSPC'},
                    {'label': 'NASDAQ', 'value': '^IXIC'},
                    {'label': 'GOLD', 'value': 'GC=F'}
                ],
                value='^GSPC',
                id='slct_asset',
                style={'width': '200%', 'margin-bottom': '5px'}
            ),
        ], style={'padding': 12, 'flex': 1}),
        html.Div([
            html.Div([
                html.Label('Initial Investment', style={'width': '150px', 'display': 'inline-block'}),
                dcc.Input(id='my_initial_inv', type='number', placeholder="Initial Investment",
                          value=1000, style={'width': '175px', 'font-size': '14px'})
            ], style={'display': 'flex', 'align-items': 'center', 'margin-bottom': '10px'}),
            html.Div([
                html.Label('Monthly Investment', style={'width': '150px', 'display': 'inline-block'}),
                dcc.Input(id='my_monthly_inv', type='number', placeholder="Monthly Investment",
                          value=200, style={'width': '175px', 'font-size': '14px'})
            ], style={'display': 'flex', 'align-items': 'center', 'margin-bottom': '10px'}),
            html.Div([
                html.Label('Years to Invest', style={'width': '150px', 'display': 'inline-block'}),
                dcc.Input(id='my_year_count', type='number', placeholder="Years to Invest",
                          value=10, style={'width': '175px', 'font-size': '14px'})
            ], style={'display': 'flex', 'align-items': 'center', 'margin-bottom': '10px'}),
        ], style={'padding': 12, 'flex': 1}),
    ], style={'display': 'flex', 'flex-direction': 'column', 'align-items': 'flex-start', 'padding-left': '40px'}),
    html.Br(),

    # Preset Buttons and Reset Button on the right side top
    html.Div([
        html.Button(
            'Preset 1', id='preset-1', n_clicks=0,
            style={'display': 'block', 'margin': 'auto', 'height': '25px',
                   'width': '70px', 'background-color': 'lightgray'}
        ),
        html.Button(
            'Preset 2', id='preset-2', n_clicks=0,
            style={'display': 'block', 'margin': 'auto', 'height': '25px',
                   'width': '70px', 'background-color': 'lightgray'}
        ),
        html.Button(
            'Preset 3', id='preset-3', n_clicks=0,
            style={'display': 'block', 'margin': 'auto', 'height': '25px',
                   'width': '70px', 'background-color': 'lightgray'}
        ),
        html.Button(
            'Customize!', id='preset-4', n_clicks=0,
            style={'display': 'block', 'margin': 'auto', 'height': '25px',
                   'width': '70px', 'background-color': 'lightgray'}
        ),
        html.Button(
            'Reset', id='reset-btn', n_clicks=0,
            style={'display': 'block', 'margin': 'auto', 'height': '25px',
                   'width': '70px', 'background-color': 'lightcoral'}
        )
    ], style={
        'position': 'absolute',
        'top': '150px',
        'right': '250px',
        'display': 'flex',
        'flex-direction': 'column',
        'align-items': 'flex-start',
        'gap': '10px'
    }),

    # Submit Button
    html.Button('Submit', id='submit-btn', n_clicks=0,
                style={'position': 'absolute', 'top': '200px', 'left': '50%',
                       'transform': 'translateX(-50%)', 'display': 'block',
                       'margin-top': '100px', 'height': '25px', 'width': '70px'}),
    html.Br(),

    # Output & Graph Section
    html.Div(id='output_container', children=[], style={'text-align': 'center'}),
    dcc.Graph(id='line_chart', style={'margin-top': '-55px', 'width': '100%', 'height': '450px'})
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
    prevent_initial_call=True
)
def update_graph(n_clicks, profile, asset, initial, monthly, years):
    if not all([profile, asset, initial, monthly, years]):
        return "Please fill all fields.", go.Figure()

    container = f"Profile: {profile}, Asset: {asset}"
    print(f"Profile: {profile}, Asset: {asset}, Initial: {initial}, Monthly: {monthly}, Years: {years}")
    try:
        portfolio_dates, portfolio_values, total_invested = simulate_investment.simulate_investment(
            asset, initial, monthly, profile, years
        )
        fig = go.Figure([
            go.Scatter(x=portfolio_dates, y=portfolio_values, mode='lines', name='Portfolio Value'),
            go.Scatter(x=portfolio_dates, y=total_invested, mode='lines', name='Total Invested')
        ])
        return container, fig
    except Exception as e:
        print(f"Error in simulation: {e}")
        return f"Error fetching data: {str(e)}", go.Figure()


# Combined callback for preset and reset functionality
@app.callback(
    [
        # Preset button styles
        Output('preset-1', 'style'),
        Output('preset-2', 'style'),
        Output('preset-3', 'style'),
        Output('preset-4', 'style'),
        # Preset button n_clicks (reset to 0 when one is active or reset is pressed)
        Output('preset-1', 'n_clicks'),
        Output('preset-2', 'n_clicks'),
        Output('preset-3', 'n_clicks'),
        Output('preset-4', 'n_clicks'),
        # Input field values
        Output('slct_profile', 'value'),
        Output('slct_asset', 'value'),
        Output('my_initial_inv', 'value'),
        Output('my_monthly_inv', 'value'),
        Output('my_year_count', 'value'),
        # Input field styles
        Output('slct_profile', 'style'),
        Output('slct_asset', 'style'),
        Output('my_initial_inv', 'style'),
        Output('my_monthly_inv', 'style'),
        Output('my_year_count', 'style')
    ],
    [
        Input('preset-1', 'n_clicks'),
        Input('preset-2', 'n_clicks'),
        Input('preset-3', 'n_clicks'),
        Input('preset-4', 'n_clicks'),
        Input('reset-btn', 'n_clicks')
    ]
)
def update_preset_and_reset(p1, p2, p3, p4, reset):
    # Default styles
    default_style_input = {'width': '175px', 'font-size': '14px', 'background-color': 'white'}
    default_preset_style = {'display': 'block', 'margin': 'auto', 'height': '25px', 'width': '70px', 'background-color': 'lightgray'}
    
    # Active styles for presets
    active_style_1 = {'display': 'block', 'margin': 'auto', 'height': '25px', 'width': '70px', 'background-color': 'lightblue'}
    active_style_2 = {'display': 'block', 'margin': 'auto', 'height': '25px', 'width': '70px', 'background-color': 'lightgreen'}
    active_style_3 = {'display': 'block', 'margin': 'auto', 'height': '25px', 'width': '70px', 'background-color': 'lightyellow'}
    active_style_4 = {'display': 'block', 'margin': 'auto', 'height': '25px', 'width': '70px', 'background-color': 'lightcoral'}

    # Default input values
    default_values = ('random', '^GSPC', 1000, 200, 10)

    ctx = callback_context
    if not ctx.triggered:
        trigger = None
    else:
        trigger = ctx.triggered[0]['prop_id'].split('.')[0]
    
    # If reset button is clicked, return default preset styles, reset n_clicks, and default input values and styles.
    if trigger == 'reset-btn' and reset > 0:
        return (
            default_preset_style, default_preset_style, default_preset_style, default_preset_style,
            0, 0, 0, 0,
            *default_values,
            default_style_input, default_style_input, default_style_input, default_style_input, default_style_input
        )
    # Otherwise, check which preset button triggered
    elif trigger == 'preset-1' and p1 % 2 == 1:
        return (
            active_style_1, default_preset_style, default_preset_style, default_preset_style,
            0, 0, 0, 0,
            'random', '^GSPC', 1000, 200, 10,
            {**default_style_input, 'background-color': 'lightblue'},
            {**default_style_input, 'background-color': 'lightblue'},
            {**default_style_input, 'background-color': 'lightblue'},
            {**default_style_input, 'background-color': 'lightblue'},
            {**default_style_input, 'background-color': 'lightblue'}
        )
    elif trigger == 'preset-2' and p2 % 2 == 1:
        return (
            default_preset_style, active_style_2, default_preset_style, default_preset_style,
            0, 0, 0, 0,
            'losing', '^IXIC', 5000, 300, 5,
            {**default_style_input, 'background-color': 'lightgreen'},
            {**default_style_input, 'background-color': 'lightgreen'},
            {**default_style_input, 'background-color': 'lightgreen'},
            {**default_style_input, 'background-color': 'lightgreen'},
            {**default_style_input, 'background-color': 'lightgreen'}
        )
    elif trigger == 'preset-3' and p3 % 2 == 1:
        return (
            default_preset_style, default_preset_style, active_style_3, default_preset_style,
            0, 0, 0, 0,
            'first', 'GC=F', 10000, 500, 20,
            {**default_style_input, 'background-color': 'lightyellow'},
            {**default_style_input, 'background-color': 'lightyellow'},
            {**default_style_input, 'background-color': 'lightyellow'},
            {**default_style_input, 'background-color': 'lightyellow'},
            {**default_style_input, 'background-color': 'lightyellow'}
        )
    elif trigger == 'preset-4' and p4 % 2 == 1:
        return (
            default_preset_style, default_preset_style, default_preset_style, active_style_4,
            0, 0, 0, 0,
            'first', '^GSPC', 2000, 400, 15,
            {**default_style_input, 'background-color': 'lightcoral'},
            {**default_style_input, 'background-color': 'lightcoral'},
            {**default_style_input, 'background-color': 'lightcoral'},
            {**default_style_input, 'background-color': 'lightcoral'},
            {**default_style_input, 'background-color': 'lightcoral'}
        )
    else:
        # If no preset is active, return default preset styles and default input values/styles
        return (
            default_preset_style, default_preset_style, default_preset_style, default_preset_style,
            0, 0, 0, 0,
            *default_values,
            default_style_input, default_style_input, default_style_input, default_style_input, default_style_input
        )

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
