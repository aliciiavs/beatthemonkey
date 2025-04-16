import dash
from dash import html, dcc
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
import random

# Initialize the Dash app
app = dash.Dash(__name__)

# Layout with video and conditional GIF display
app.layout = html.Div([
    dbc.Row([

        # GIF and status message on the right side
        dbc.Col([
            html.H4("Monkey Status", style={'textAlign': 'center'}),
            html.Img(id='monkey-gif', src='assets/angry_monkey.gif', style={"width": "100%", "max-width": "300px"}),  # Default GIF
            html.Div(id='status-message', style={'textAlign': 'center'}),
            html.Button("Change Mood", id="change-mood-btn", n_clicks=0, style={'marginTop': '20px'})
        ], width=6),  # The other side takes half the screen width
    ]),
])

# Callback to update the GIF and status based on the button click
@app.callback(
    [Output('monkey-gif', 'src'),
     Output('status-message', 'children')],
    [Input('change-mood-btn', 'n_clicks')],
    prevent_initial_call=True
)
def change_mood(n_clicks):
    # Randomly determine if the monkey is happy or sad
    if n_clicks > 0:
        mood = random.choice(['happy', 'sad'])
        
        if mood == 'happy':
            return 'assets/happy_monkey.gif', "The monkey is happy!"
        else:
            return 'assets/angry_monkey.gif', "The monkey is sad!"
    
    # Default state when no button is clicked
    return 'assets/monkey_sad.gif', "The monkey is sad!"

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
