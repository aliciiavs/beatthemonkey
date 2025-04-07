import pandas as pd
import plotly.graph_objects as go
from dash import Dash, dcc, html, Input, Output, State, callback_context
import simulate_investment  # Import your simulation function
#import connect
import inflation
import dash_bootstrap_components as dbc

# Initialize the app
app = Dash(__name__)

# App Layout
app.layout = html.Div([
    # Set the background color and font for the whole page
    html.Div([
        html.H1("Investing Learning Dashboard", style={
            'text-align': 'center',
            'color': '#333',  # Dark gray color for the header
            'font-size': '36px',
            'margin-top': '0px'
        }),

        # Two sections side by side
        html.Div([
            html.Div([
                html.Span("💡", id="popover-icon", style={"cursor": "pointer", "fontSize": "1.5em"}),
                html.Span('Select Profile'),
                dbc.Popover(
                    [
                        dbc.PopoverHeader("What does this mean?", style={'font-family': 'Arial, sans-serif', 'font-size':'15px', 'font-weight': 'bold'}),
                        dbc.PopoverBody(id="popover-body", style={'font-family': 'Arial, sans-serif', 'font-size':'15px'})
                    ],
                    id="popover",
                    target="popover-icon",
                    trigger="click",
                    style={
                'marginLeft': '-319px',  # Adjust the horizontal margin
                'marginTop': '30px',  # Adjust the vertical margin
                'max-width': '250px'  # Optional: limit the width of the popover
            }
                ),
                dcc.Dropdown(
                    options=[
                        {'label': 'Random', 'value': 'random'},
                        {'label': 'Losing', 'value': 'losing'},
                        {'label': 'Buy-The-Dip', 'value': 'buythedip'},
                        {'label': 'First', 'value': 'first'}
                    ],
                    value='random',
                    id='slct_profile'
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
                    id='slct_asset'
                ),
            ], style={'padding': '20px', 'flex': 1, 'background-color': '#ffffff', 'border-radius': '8px',         # Sets the width of the element
    'margin-left': '250px'}),

            html.Div([
                html.Div([
                    html.Label('Initial Investment', style={'width': '150px', 'display': 'inline-block'}),
                    dcc.Input(id='my_initial_inv', type='number', placeholder="Initial Investment",
                            value=1000,
                            min=0,
                            max=999999999,
                            style={
                                'width': '175px', 'font-size': '14px', 'padding': '8px', 'border-radius': '5px',
                                'border': '1px solid #ccc'
                            })
                ], style={'display': 'flex', 'align-items': 'center', 'margin-bottom': '10px'}),
                html.Div([
                    html.Label('Monthly Investment', style={'width': '150px', 'display': 'inline-block'}),
                    dcc.Input(id='my_monthly_inv', type='number', placeholder="Monthly Investment",
                            value=250,
                            min=0,
                            max=999999999,
                            style={
                                'width': '175px', 'font-size': '14px', 'padding': '8px', 'border-radius': '5px',
                                'border': '1px solid #ccc'
                            })
                ], style={'display': 'flex', 'align-items': 'center', 'margin-bottom': '10px'}),
                html.Div([
                    html.Label('Years to Invest', style={'width': '150px', 'display': 'inline-block'}),
                    dcc.Input(id='my_year_count', type='number', placeholder="Years to Invest",
                            value=10,
                            min=1,
                            max=150,
                            style={
                                'width': '175px', 'font-size': '14px', 'padding': '8px', 'border-radius': '5px',
                                'border': '1px solid #ccc'
                            })
                ], style={'display': 'flex', 'align-items': 'center', 'margin-bottom': '10px'}),
            ], style={'padding': '12px', 'flex': 1, 'border-radius': '8px', 'width': '200px',         # Sets the width of the element
                'margin-left': '-600px', 'border-radius': '8px', 'margin-top':'10px'}),
        ], style={
            'display': 'flex',
            'flex-direction': 'row',
            'align-items': 'flex-start',
            'gap': '20px',
            'padding-left': '40px',
            'padding-right': '40px',
        }),
        html.Br(),

        # Preset Buttons and Reset Button on the right side top
        html.Div([
            html.Button(
                'Preset 1', id='preset-1', n_clicks=0,
                style={
                    'height': '35px', 'width': '100px', 'border': 'none',
                    'border-radius': '5px', 'font-size': '14px', 'margin-bottom': '10px', 'background-color': '#ffffff'
                }
            ),
            html.Button(
                'Preset 2', id='preset-2', n_clicks=0,
                style={
                    'height': '35px', 'width': '100px', 'border': 'none',
                    'border-radius': '5px', 'font-size': '14px', 'margin-bottom': '10px'
                }
            ),
            html.Button(
                'Preset 3', id='preset-3', n_clicks=0,
                style={
                    'height': '35px', 'width': '100px', 'border': 'none',
                    'border-radius': '5px', 'font-size': '14px', 'margin-bottom': '10px'
                }
            ),

            html.Button(
                'Reset', id='reset-btn', n_clicks=0,
                style={
                    'height': '35px', 'width': '100px', 'background-color': 'lightcoral', 'border': 'none',
                    'border-radius': '5px', 'font-size': '14px', 'margin-bottom': '10px'
                }
            ),
        ], style={
            'position': 'absolute',
            'top': '85px',
            'right': '350px',
            'display': 'flex',
            'flex-direction': 'column',
            'gap': '10px',
            'padding-top':'10px'
        }),

        # Submit Button
        html.Button('Submit', id='submit-btn', n_clicks=0,
                    style={
                        'position': 'absolute', 'top': '250px', 'left': '50%',
                        'transform': 'translateX(-50%)', 'display': 'block',
                        'margin-top': '75px', 'height': '35px', 'width': '100px',
                        'background-color': '#4CAF50', 'border': 'none', 'color': 'white',
                        'border-radius': '5px', 'font-size': '16px'
                    }),
        html.Br(),

        # Output & Graph Section
        html.Div(id='output_container', children=[], style={'text-align': 'center', 'margin-top': '70px', 'font-size':'20px', 'color': 'green'}),
        dcc.Graph(id='line_chart', style={'margin-top': '80px', 'width': '100%', 'height': '450px'})
    ], style={
        'background-color': '#f4f4f9',  # Light gray background for the app
        'font-family': 'Arial, sans-serif',  # Apply font globally

    })
])

@app.callback(
    Output('popover-body', 'children'),
    Input('slct_profile', 'value')
)
def update_popover_text(profile):
    if profile == 'random':
        return "Dollar-Cost Averaging (DCA): This strategy involves investing randomly at irregular intervals."
    elif profile == 'losing':
        return "This strategy invests when a price is consistently falling."
    elif profile == 'buythedip':
        return "This strategy invests when the price drops significantly (buying the dip)."
    elif profile == 'first':
        return "This strategy invests on the first trading day of each month."
    return "Select a strategy to learn more."

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
    # Ensure all fields are provided
    if not all([profile, asset, initial, monthly, years]):
        return "Please fill all fields.", go.Figure()

    print(f"Profile: {profile}, Asset: {asset}, Initial: {initial}, Monthly: {monthly}, Years: {years}")

    # Define the preset combinations (adjust as needed)
    preset_combinations = [
        ('random', '^GSPC', 1000, 200, 10),  # Preset 1
        ('losing', '^IXIC', 5000, 300, 5),    # Preset 2
        ('first', 'GC=F', 10000, 500, 20)      # Preset 3
    ]

    try:
        # If the inputs match one of the preset combinations, run the alternative simulation function
        if (profile, asset, initial, monthly, years) in preset_combinations:
            preset_id = preset_combinations.index((profile, asset, initial, monthly, years)) + 1
            #portfolio_dates, portfolio_values, total_invested = connect.fetch_preset_table(preset_id)
        else:
            # Otherwise, run the regular simulation function
            portfolio_dates, portfolio_values, total_invested = simulate_investment.simulate_investment2(
                asset, initial, monthly, profile, years
            )
            portfolio_df = inflation.calculate_value(portfolio_dates, initial, monthly)
            adjusted_values = portfolio_df['Adjusted Value']
            generated = portfolio_values[-1] - total_invested[-1]
            if generated > 0:
                container = f"If you had invested {years} years ago, today you would have earned {round(generated):,} $ !!!"
            elif generated < 0:
                container = f"If you had invested {years} years ago, you would have lost {round(generated):,} $ ..."

        fig = go.Figure([
            go.Scatter(x=portfolio_dates, y=portfolio_values, mode='lines', name='Portfolio Value'),
            go.Scatter(x=portfolio_dates, y=total_invested, mode='lines', name='Total Invested'),
            go.Scatter(x=portfolio_dates, y=adjusted_values, mode='lines', name='Adjusted Total Investment')
        ])
        return container, fig

    except Exception as e:
        print(f"Error in simulation: {e}")
        return f"Error fetching data: {str(e)}", go.Figure()


# Combined callback for preset and reset functionality
@app.callback(
    [
        # Preset button styles (3 outputs)
        Output('preset-1', 'style'),
        Output('preset-2', 'style'),
        Output('preset-3', 'style'),
        # Preset button n_clicks (3 outputs)
        Output('preset-1', 'n_clicks'),
        Output('preset-2', 'n_clicks'),
        Output('preset-3', 'n_clicks'),
        # Input field values (5 outputs)
        Output('slct_profile', 'value'),
        Output('slct_asset', 'value'),
        Output('my_initial_inv', 'value'),
        Output('my_monthly_inv', 'value'),
        Output('my_year_count', 'value'),
        # Input field styles (5 outputs)
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
        Input('reset-btn', 'n_clicks')
    ]
)
def update_preset_and_reset(p1, p2, p3, reset):
    ## Default styles for input fields and preset buttons
    # Default style for input fields
    default_style_input = {
    'height': '25px',
    'width': '175px',
    'border': 'none',
    'border-radius': '5px',
    'font-size': '16px',
    'padding': '8px',
    'margin-bottom': '10px',
    'background-color': 'lightgray',
    'display': 'flex',
    'justify-content': 'flex-end',    # Align child elements to the right
    'align-items': 'center'          # Vertically center the content
    }


    # Default style for preset buttons
    default_preset_style = {
        'display': 'block',
        'margin': 'auto',
        'height': '35px',
        'width': '100px',
        'border': 'none',
        'border-radius': '5px',
        'font-size': '14px',
        'margin-bottom': '10px',
        'background-color': 'lightgray'
    }

    # Active styles for preset buttons
    active_style_1 = {
        'display': 'block',
        'margin': 'auto',
        'height': '35px',
        'width': '100px',
        'border': 'none',
        'border-radius': '5px',
        'font-size': '14px',
        'margin-bottom': '10px',
        'background-color': 'lightblue'
    }

    active_style_2 = {
        'display': 'block',
        'margin': 'auto',
        'height': '35px',
        'width': '100px',
        'border': 'none',
        'border-radius': '5px',
        'font-size': '14px',
        'margin-bottom': '10px',
        'background-color': 'lightgreen'
    }

    active_style_3 = {
        'display': 'block',
        'margin': 'auto',
        'height': '35px',
        'width': '100px',
        'border': 'none',
        'border-radius': '5px',
        'font-size': '14px',
        'margin-bottom': '10px',
        'background-color': 'lightyellow'
    }
   
    # Default input values
    default_values = ('random', '^GSPC', 1000, 250, 10)
    
    ctx = callback_context
    if not ctx.triggered:
        trigger = None
    else:
        trigger = ctx.triggered[0]['prop_id'].split('.')[0]
    
    # If reset button is clicked, return default values and styles
    if trigger == 'reset-btn' and reset > 0:
        return (
            default_preset_style, default_preset_style, default_preset_style,  # Preset button styles
            0, 0, 0,                                                          # Preset n_clicks
            *default_values,                                                   # Input field values
            default_style_input, default_style_input, default_style_input, 
            default_style_input, default_style_input                           # Input field styles
        )
    # If Preset 1 is clicked and active (odd clicks)
    elif trigger == 'preset-1' and p1 % 2 == 1:
        return (
            active_style_1, default_preset_style, default_preset_style,  # Preset button styles
            0, 0, 0,                                                    # Preset n_clicks
            'random', '^GSPC', 1000, 250, 10,                            # Input values for Preset 1
            {**default_style_input, 'background-color': 'lightblue'},
            {**default_style_input, 'background-color': 'lightblue'},
            {**default_style_input, 'background-color': 'lightblue'},
            {**default_style_input, 'background-color': 'lightblue'},
            {**default_style_input, 'background-color': 'lightblue'}
        )
    elif trigger == 'preset-2' and p2 % 2 == 1:
        return (
            default_preset_style, active_style_2, default_preset_style,
            0, 0, 0,
            'losing', '^IXIC', 5000, 300, 5,
            {**default_style_input, 'background-color': 'lightgreen'},
            {**default_style_input, 'background-color': 'lightgreen'},
            {**default_style_input, 'background-color': 'lightgreen'},
            {**default_style_input, 'background-color': 'lightgreen'},
            {**default_style_input, 'background-color': 'lightgreen'}
        )
    elif trigger == 'preset-3' and p3 % 2 == 1:
        return (
            default_preset_style, default_preset_style, active_style_3,
            0, 0, 0,
            'first', 'GC=F', 10000, 500, 20,
            {**default_style_input, 'background-color': 'lightyellow'},
            {**default_style_input, 'background-color': 'lightyellow'},
            {**default_style_input, 'background-color': 'lightyellow'},
            {**default_style_input, 'background-color': 'lightyellow'},
            {**default_style_input, 'background-color': 'lightyellow'}
        )
    else:
        # If no preset is active, return default preset styles and input defaults
        return (
            default_preset_style, default_preset_style, default_preset_style,
            0, 0, 0,
            *default_values,
            default_style_input, default_style_input, default_style_input, default_style_input, default_style_input
        )

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)