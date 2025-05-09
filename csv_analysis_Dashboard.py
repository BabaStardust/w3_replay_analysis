import pandas as pd
import dash
from dash import dcc, html, dash_table, Input, Output
import plotly.express as px
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)

# Helper function to convert milliseconds to mm:ss format
def ms_to_mmss(ms):
    if pd.isnull(ms):
        return "00:00"
    seconds = int(ms / 1000)
    minutes = seconds // 60
    seconds = seconds % 60
    return f"{minutes:02d}:{seconds:02d}"

# Load the dataset into a DataFrame
def load_data(file_path):
    try:
        if file_path.endswith('.csv'):
            df = pd.read_csv(file_path, low_memory=False)
        else:
            raise ValueError("Unsupported file type. Please provide a CSV file.")
        return df
    except Exception as e:
        logging.error(f"Error loading the data: {e}")
        return None

# Summary Calculation Functions

def calculate_total_gold_units(df):
    # Calculate total gold for winner units
    target_columns = [col for col in df.columns if col.startswith('players_winner_units_summary_') and col.endswith('_gold')]
    if target_columns:
        df['players_winner_units_summary_total_gold'] = df[target_columns].sum(axis=1)
    else:
        df['players_winner_units_summary_total_gold'] = 0

    # Calculate total gold for loser units
    target_columns = [col for col in df.columns if col.startswith('players_loser_units_summary_') and col.endswith('_gold')]
    if target_columns:
        df['players_loser_units_summary_total_gold'] = df[target_columns].sum(axis=1)
    else:
        df['players_loser_units_summary_total_gold'] = 0

    return df

def calculate_total_lumber_buildings(df):
    # Calculate total lumber for winner buildings
    target_columns = [col for col in df.columns if col.startswith('players_winner_buildings_summary_') and col.endswith('_lumber')]
    if target_columns:
        df['players_winner_buildings_summary_total_lumber'] = df[target_columns].sum(axis=1)
    else:
        df['players_winner_buildings_summary_total_lumber'] = 0

    # Calculate total lumber for loser buildings
    target_columns = [col for col in df.columns if col.startswith('players_loser_buildings_summary_') and col.endswith('_lumber')]
    if target_columns:
        df['players_loser_buildings_summary_total_lumber'] = df[target_columns].sum(axis=1)
    else:
        df['players_loser_buildings_summary_total_lumber'] = 0

    return df

def calculate_total_lumber_upgrades(df):
    # Calculate total lumber for winner upgrades
    target_columns = [col for col in df.columns if col.startswith('players_winner_upgrades_summary_') and col.endswith('_lumber')]
    if target_columns:
        df['players_winner_upgrades_summary_total_lumber'] = df[target_columns].sum(axis=1)
    else:
        df['players_winner_upgrades_summary_total_lumber'] = 0

    # Calculate total lumber for loser upgrades
    target_columns = [col for col in df.columns if col.startswith('players_loser_upgrades_summary_') and col.endswith('_lumber')]
    if target_columns:
        df['players_loser_upgrades_summary_total_lumber'] = df[target_columns].sum(axis=1)
    else:
        df['players_loser_upgrades_summary_total_lumber'] = 0

    return df

def calculate_total_gold_buildings(df):
    # Calculate total gold for winner buildings
    target_columns = [col for col in df.columns if col.startswith('players_winner_buildings_summary_') and col.endswith('_gold')]
    if target_columns:
        df['players_winner_buildings_summary_total_gold'] = df[target_columns].sum(axis=1)
    else:
        df['players_winner_buildings_summary_total_gold'] = 0

    # Calculate total gold for loser buildings
    target_columns = [col for col in df.columns if col.startswith('players_loser_buildings_summary_') and col.endswith('_gold')]
    if target_columns:
        df['players_loser_buildings_summary_total_gold'] = df[target_columns].sum(axis=1)
    else:
        df['players_loser_buildings_summary_total_gold'] = 0

    return df

def calculate_total_gold_upgrades(df):
    # Calculate total gold for winner upgrades
    target_columns = [col for col in df.columns if col.startswith('players_winner_upgrades_summary_') and col.endswith('_gold')]
    if target_columns:
        df['players_winner_upgrades_summary_total_gold'] = df[target_columns].sum(axis=1)
    else:
        df['players_winner_upgrades_summary_total_gold'] = 0

    # Calculate total gold for loser upgrades
    target_columns = [col for col in df.columns if col.startswith('players_loser_upgrades_summary_') and col.endswith('_gold')]
    if target_columns:
        df['players_loser_upgrades_summary_total_gold'] = df[target_columns].sum(axis=1)
    else:
        df['players_loser_upgrades_summary_total_gold'] = 0

    return df

def calculate_total_gold_items(df):
    # Calculate total gold for winner items
    target_columns = [col for col in df.columns if col.startswith('players_winner_items_summary_') and col.endswith('_gold')]
    if target_columns:
        df['players_winner_items_summary_total_gold'] = df[target_columns].sum(axis=1)
    else:
        df['players_winner_items_summary_total_gold'] = 0

    # Calculate total gold for loser items
    target_columns = [col for col in df.columns if col.startswith('players_loser_items_summary_') and col.endswith('_gold')]
    if target_columns:
        df['players_loser_items_summary_total_gold'] = df[target_columns].sum(axis=1)
    else:
        df['players_loser_items_summary_total_gold'] = 0

    return df

def calculate_total_lumber_units(df):
    # Calculate total lumber for winner units
    target_columns = [col for col in df.columns if col.startswith('players_winner_units_summary_') and col.endswith('_lumber')]
    if target_columns:
        df['players_winner_units_summary_total_lumber'] = df[target_columns].sum(axis=1)
    else:
        df['players_winner_units_summary_total_lumber'] = 0

    # Calculate total lumber for loser units
    target_columns = [col for col in df.columns if col.startswith('players_loser_units_summary_') and col.endswith('_lumber')]
    if target_columns:
        df['players_loser_units_summary_total_lumber'] = df[target_columns].sum(axis=1)
    else:
        df['players_loser_units_summary_total_lumber'] = 0

    return df

def calculate_total_food_units(df):
    # Calculate total food for winner units
    target_columns = [col for col in df.columns if col.startswith('players_winner_units_summary_') and col.endswith('_food')]
    if target_columns:
        df['players_winner_units_summary_total_food'] = df[target_columns].sum(axis=1)
    else:
        df['players_winner_units_summary_total_food'] = 0

    # Calculate total food for loser units
    target_columns = [col for col in df.columns if col.startswith('players_loser_units_summary_') and col.endswith('_food')]
    if target_columns:
        df['players_loser_units_summary_total_food'] = df[target_columns].sum(axis=1)
    else:
        df['players_loser_units_summary_total_food'] = 0

    return df

def calculate_total_buildtime_units(df):
    # Calculate total buildtime for winner units
    target_columns = [col for col in df.columns if col.startswith('players_winner_units_summary_') and col.endswith('_buildtime')]
    if target_columns:
        df['players_winner_units_summary_total_buildtime'] = df[target_columns].sum(axis=1)
    else:
        df['players_winner_units_summary_total_buildtime'] = 0

    # Calculate total buildtime for loser units
    target_columns = [col for col in df.columns if col.startswith('players_loser_units_summary_') and col.endswith('_buildtime')]
    if target_columns:
        df['players_loser_units_summary_total_buildtime'] = df[target_columns].sum(axis=1)
    else:
        df['players_loser_units_summary_total_buildtime'] = 0

    return df

def calculate_total_gold_all(df):
    # Calculate total gold for all winner summaries
    required_columns = [
        'players_winner_units_summary_total_gold',
        'players_winner_buildings_summary_total_gold',
        'players_winner_upgrades_summary_total_gold',
        'players_winner_items_summary_total_gold'
    ]
    existing_columns = [col for col in required_columns if col in df.columns]
    if existing_columns:
        df['players_winner_all_summary_gold'] = df[existing_columns].sum(axis=1)
    else:
        df['players_winner_all_summary_gold'] = 0

    # Calculate total gold for all loser summaries
    required_columns = [
        'players_loser_units_summary_total_gold',
        'players_loser_buildings_summary_total_gold',
        'players_loser_upgrades_summary_total_gold',
        'players_loser_items_summary_total_gold'
    ]
    existing_columns = [col for col in required_columns if col in df.columns]
    if existing_columns:
        df['players_loser_all_summary_gold'] = df[existing_columns].sum(axis=1)
    else:
        df['players_loser_all_summary_gold'] = 0

    return df

def calculate_total_lumber_all(df):
    # Calculate total lumber for all winner summaries
    required_columns = [
        'players_winner_units_summary_total_lumber',
        'players_winner_buildings_summary_total_lumber',
        'players_winner_upgrades_summary_total_lumber'
    ]
    existing_columns = [col for col in required_columns if col in df.columns]
    if existing_columns:
        df['players_winner_all_summary_lumber'] = df[existing_columns].sum(axis=1)
    else:
        df['players_winner_all_summary_lumber'] = 0

    # Calculate total lumber for all loser summaries
    required_columns = [
        'players_loser_units_summary_total_lumber',
        'players_loser_buildings_summary_total_lumber',
        'players_loser_upgrades_summary_total_lumber'
    ]
    existing_columns = [col for col in required_columns if col in df.columns]
    if existing_columns:
        df['players_loser_all_summary_lumber'] = df[existing_columns].sum(axis=1)
    else:
        df['players_loser_all_summary_lumber'] = 0

    return df

# Function to calculate average and standard deviation for a column with optional filtering
def calculate_avg_std(df, column, duration_range=None):
    # Apply filtering based on provided filters
    filtered_df = df.copy()
    if duration_range:
        lower, upper = duration_range
        if lower is not None and upper is not None: # Ensure both bounds are provided
            filtered_df = filtered_df[(filtered_df['duration'] >= lower) & (filtered_df['duration'] <= upper)]

    avg = filtered_df[column].mean()
    std_dev = filtered_df[column].std()
    count = filtered_df.shape[0]  # Count of data points taken into account

    return avg, std_dev, count

# Function to calculate win percentage and total games for the selected matchup
def calculate_win_percentage(df, winner_race, loser_race, duration_range=None):
    filtered_df = df.copy()
    if duration_range:
        lower, upper = duration_range
        if lower is not None and upper is not None: # Ensure both bounds are provided
            filtered_df = filtered_df[(filtered_df['duration'] >= lower) & (filtered_df['duration'] <= upper)]

    if winner_race and loser_race:
        win_count = filtered_df[
            (filtered_df['players_winner_raceDetected'] == winner_race) &
            (filtered_df['players_loser_raceDetected'] == loser_race)
        ].shape[0]

        total_count = filtered_df[
            ((filtered_df['players_winner_raceDetected'] == winner_race) &
             (filtered_df['players_loser_raceDetected'] == loser_race)) |
            ((filtered_df['players_winner_raceDetected'] == loser_race) &
             (filtered_df['players_loser_raceDetected'] == winner_race))
        ].shape[0]

        win_percentage = (win_count / total_count) * 100 if total_count > 0 else 0
        return win_percentage, total_count
    # If only one race is selected or no races, calculate overall stats for the filtered data
    elif winner_race or loser_race:
         # Find total games involving the selected race(s) within the filters
         if winner_race and not loser_race:
             total_count = filtered_df[(filtered_df['players_winner_raceDetected'] == winner_race) | (filtered_df['players_loser_raceDetected'] == winner_race)].shape[0]
             win_count = filtered_df[filtered_df['players_winner_raceDetected'] == winner_race].shape[0]
         elif loser_race and not winner_race:
             total_count = filtered_df[(filtered_df['players_winner_raceDetected'] == loser_race) | (filtered_df['players_loser_raceDetected'] == loser_race)].shape[0]
             # For loser_race only, win percentage is calculated from the perspective of that race winning
             win_count = filtered_df[filtered_df['players_winner_raceDetected'] == loser_race].shape[0]
         else: # Should not happen based on logic, but good practice
             total_count = filtered_df.shape[0]
             win_count = 0 # Cannot determine win% without a reference point

         win_percentage = (win_count / total_count) * 100 if total_count > 0 else 0
         return win_percentage, total_count

    # If no race filter is applied, return 0 win percentage and total count of filtered games
    return 0, filtered_df.shape[0]

# Load the dataset globally for the module
file_path = 'working_directory/combined_replay_data_enhanced.csv'  # Update this path as needed
df_global = load_data(file_path)

if df_global is None:
    raise Exception("Data could not be loaded. Please check the file path and format.")

# Function to create the Dash application
def create_dash_app(flask_server, url_base_pathname):
    # Use the globally loaded DataFrame
    df = df_global.copy()

    # Initialize Dash app, linking it to the Flask server
    dash_app = dash.Dash(
        server=flask_server,
        url_base_pathname=url_base_pathname, # Use the passed url_base_pathname
        suppress_callback_exceptions=True # Often needed when embedding
    )

    # Define the app layout
    dash_app.layout = html.Div([
        html.Div(
            dcc.Link(html.Button("Back to Main"), href='/', refresh=True),
            style={'marginBottom': '20px', 'textAlign': 'left'}  # Added textAlign for better alignment
        ),
        html.H1("Replay Data - Graphical Dashboards"),
        html.Div([
            html.Label('Filter by Winner Race:'),
            dcc.Dropdown(
                id='avg-std-winner-race-dropdown',
                options=[{'label': race, 'value': race} for race in df['players_winner_raceDetected'].unique()],
                value=None,  # Set to None to allow no default selection
                placeholder="Select Winner Race",
                clearable=True
            ),
            html.Br(),
            html.Label('Filter by Loser Race:'),
            dcc.Dropdown(
                id='avg-std-loser-race-dropdown',
                options=[{'label': race, 'value': race} for race in df['players_loser_raceDetected'].unique()],
                value=None,  # Set to None to allow no default selection
                placeholder="Select Loser Race",
                clearable=True
            ),
            html.Br(),
            html.Label('Filter by Duration Range (ms):'),
            html.Div([
                dcc.Input(
                    id='duration-lower-input',
                    type='number',
                    placeholder='Lower Bound',
                    style={'marginRight': '10px'}
                ),
                dcc.Input(
                    id='duration-upper-input',
                    type='number',
                    placeholder='Upper Bound'
                ),
            ]),
            html.Br(),
        ], style={'width': '48%', 'display': 'inline-block', 'verticalAlign': 'top', 'padding': '20px'}),
        html.Div([
            dash_table.DataTable(
                id='avg-std-table',
                columns=[
                    {"name": "Metric", "id": "metric"},
                    {"name": "Average", "id": "average"},
                    {"name": "Standard Deviation", "id": "std_dev"},
                    {"name": "Data Points Count", "id": "count"}
                ],
                data=[],  # Data will be populated by the callback
                filter_action='native',
                sort_action='native',
                page_action='none',  # Disable pagination to show all rows
                style_table={'overflowX': 'auto'},  # Enable horizontal scrolling

                # Conditional styling for specific columns
                style_cell_conditional=[
                    {
                        'if': {'column_id': 'metric'},  # Target the 'metric' column
                        'minWidth': '200px',            # Ensure the column has at least 200px width
                        'width': 'auto',                # Allow the width to adjust based on content
                        'whiteSpace': 'normal',         # Enable text wrapping if needed
                        'textAlign': 'left'             # Align text to the left
                    }
                ],

                # Default styles for all cells
                style_cell={
                    'minWidth': '100px', 'width': '150px', 'maxWidth': '180px',
                    'whiteSpace': 'normal',            # Allow text to wrap
                    'textAlign': 'left'
                },

                # Styles for the header
                style_header={
                    'backgroundColor': 'rgb(230, 230, 230)',
                    'fontWeight': 'bold'
                }
            )
        ], style={'width': '48%', 'display': 'inline-block', 'padding': '20px'}),
        html.Hr(),

        html.Div([
            dcc.Graph(id='lumber-delta-bar-graph')
        ], style={'padding': '20px'}),
        html.Hr(),
        html.Div([
            dcc.Graph(id='winner-lumber-graph')
        ], style={'padding': '20px'}),
        html.Hr(),
        html.Div([
            dcc.Graph(id='gold-delta-bar-graph')  # New Graph for Gold Delta
        ], style={'padding': '20px'}),
        html.Hr(),
        html.Div([
            dcc.Graph(id='winner-gold-graph')      # New Graph for Winner and Loser Gold Accumulation
        ], style={'padding': '20px'}),
        html.Hr(),
        html.Div([
            html.H3("Win Percentage and Total Games"),
            html.Div(id='win-percentage-display', style={'fontSize': 20, 'padding': '10px'})
        ], style={'padding': '20px'}),
    ])

    # Define callbacks within the create_dash_app function
    @dash_app.callback(
        [Output('avg-std-table', 'data'),
         Output('win-percentage-display', 'children'),
         Output('lumber-delta-bar-graph', 'figure'),
         Output('winner-lumber-graph', 'figure'),
         Output('gold-delta-bar-graph', 'figure'),
         Output('winner-gold-graph', 'figure')],
        [Input('avg-std-winner-race-dropdown', 'value'),
         Input('avg-std-loser-race-dropdown', 'value'),
         Input('duration-lower-input', 'value'),
         Input('duration-upper-input', 'value')]
    )
    def update_avg_std_table(winner_race, loser_race, duration_lower, duration_upper):
        logging.info("Callback triggered with filters:")
        logging.info(f"Winner Race: {winner_race}, Loser Race: {loser_race}, Duration: ({duration_lower}, {duration_upper})")

        # Start with the globally loaded DataFrame copy for filtering
        filtered_df = df.copy()

        # Apply Winner Race filter
        if winner_race:
            filtered_df = filtered_df[filtered_df['players_winner_raceDetected'] == winner_race]

        # Apply Loser Race filter
        if loser_race:
            filtered_df = filtered_df[filtered_df['players_loser_raceDetected'] == loser_race]

        # Apply Duration Range filter
        duration_range = None
        if duration_lower is not None and duration_upper is not None:
            if duration_lower > duration_upper:
                duration_lower, duration_upper = duration_upper, duration_lower
            filtered_df = filtered_df[(filtered_df['duration'] >= duration_lower) & (filtered_df['duration'] <= duration_upper)]
            duration_range = (duration_lower, duration_upper)
        elif duration_lower is not None:
            filtered_df = filtered_df[filtered_df['duration'] >= duration_lower]
            # Need an upper bound for range calculation, use max if only lower is provided
            # duration_range = (duration_lower, df['duration'].max()) # Or handle differently
        elif duration_upper is not None:
             filtered_df = filtered_df[filtered_df['duration'] <= duration_upper]
             # duration_range = (0, duration_upper) # Or handle differently

        logging.info(f"Filtered DataFrame shape: {filtered_df.shape}")

        # Recalculate all individual summary columns within the callback using the filtered_df
        filtered_df = calculate_total_gold_units(filtered_df)
        filtered_df = calculate_total_lumber_buildings(filtered_df)
        filtered_df = calculate_total_lumber_upgrades(filtered_df)
        filtered_df = calculate_total_gold_buildings(filtered_df)
        filtered_df = calculate_total_gold_upgrades(filtered_df)
        filtered_df = calculate_total_gold_items(filtered_df)
        filtered_df = calculate_total_lumber_units(filtered_df)
        filtered_df = calculate_total_food_units(filtered_df)
        filtered_df = calculate_total_buildtime_units(filtered_df)
        filtered_df = calculate_total_gold_all(filtered_df)
        filtered_df = calculate_total_lumber_all(filtered_df)

        # Verify that all summary columns are present in filtered_df
        required_columns = [
            'players_winner_units_summary_total_gold', 'players_loser_units_summary_total_gold',
            'players_winner_units_summary_total_lumber', 'players_loser_units_summary_total_lumber',
            'players_winner_units_summary_total_food', 'players_loser_units_summary_total_food',
            'players_winner_units_summary_total_buildtime', 'players_loser_units_summary_total_buildtime',
            'players_winner_upgrades_summary_total_gold', 'players_loser_upgrades_summary_total_gold',
            'players_winner_upgrades_summary_total_lumber', 'players_loser_upgrades_summary_total_lumber',
            'players_winner_buildings_summary_total_gold', 'players_loser_buildings_summary_total_gold',
            'players_winner_buildings_summary_total_lumber', 'players_loser_buildings_summary_total_lumber',
            'players_winner_items_summary_total_gold', 'players_loser_items_summary_total_gold',
            'players_winner_all_summary_gold', 'players_loser_all_summary_gold',
            'players_winner_all_summary_lumber', 'players_loser_all_summary_lumber'
        ]

        missing_columns = [col for col in required_columns if col not in filtered_df.columns]
        if missing_columns:
            logging.warning(f"Missing columns after filtering and recalculating: {missing_columns}")
            for col in missing_columns:
                filtered_df[col] = 0 # Add missing columns with 0

        # Define columns to analyze for the table
        columns_to_analyze = [
            'players_winner_units_summary_total_gold', 'players_loser_units_summary_total_gold',
            'players_winner_units_summary_total_lumber', 'players_loser_units_summary_total_lumber',
            'players_winner_units_summary_total_food', 'players_loser_units_summary_total_food',
            'players_winner_units_summary_total_buildtime', 'players_loser_units_summary_total_buildtime',
            'players_winner_upgrades_summary_total_gold', 'players_loser_upgrades_summary_total_gold',
            'players_winner_upgrades_summary_total_lumber', 'players_loser_upgrades_summary_total_lumber',
            'players_winner_buildings_summary_total_gold', 'players_loser_buildings_summary_total_gold',
            'players_winner_buildings_summary_total_lumber', 'players_loser_buildings_summary_total_lumber',
            'players_winner_items_summary_total_gold', 'players_loser_items_summary_total_gold',
            'players_winner_all_summary_gold', 'players_loser_all_summary_gold',
            'players_winner_all_summary_lumber', 'players_loser_all_summary_lumber'
        ]

        results = []
        for column in columns_to_analyze:
            avg, std_dev, count = calculate_avg_std(
                filtered_df, column, # Use filtered_df here
                duration_range=duration_range
            )
            # Format buildtime/duration columns
            if 'buildtime' in column or 'duration' in column:
                avg_formatted = f"{round(avg, 2)} ms ({ms_to_mmss(avg)})" if pd.notnull(avg) else "0 ms (00:00)"
                std_dev_formatted = f"{round(std_dev, 2)} ms ({ms_to_mmss(std_dev)})" if pd.notnull(std_dev) else "0 ms (00:00)"
            else:
                avg_formatted = round(avg, 2) if pd.notnull(avg) else 0
                std_dev_formatted = round(std_dev, 2) if pd.notnull(std_dev) else 0

            results.append({
                "metric": column,
                "average": avg_formatted,
                "std_dev": std_dev_formatted,
                "count": count
            })

        # Calculate Win Percentage using the original full df for context if needed, but apply filters
        # Using filtered_df here directly for consistency with table and graphs
        win_percentage, total_count = calculate_win_percentage(
            filtered_df, # Use filtered_df to calculate win % based on current view
            winner_race, loser_race,
            duration_range=duration_range
        )

        # Clarify win percentage display based on selection
        if winner_race and loser_race:
            win_percentage_text = f"{winner_race} Win % vs {loser_race}: {win_percentage:.2f}%"
        elif winner_race:
            win_percentage_text = f"{winner_race} Overall Win %: {win_percentage:.2f}%"
        elif loser_race:
            win_percentage_text = f"{loser_race} Overall Win %: {win_percentage:.2f}%" # Note: calculated as if loser_race was the winner
        else:
             win_percentage_text = "Win Percentage: N/A (Select Races)"

        win_percentage_display = f"{win_percentage_text} | Total Games in Filter: {total_count}"

        # Create lumber delta bar graph
        if not filtered_df.empty and 'duration' in filtered_df.columns:
            max_duration = filtered_df['duration'].max() if not filtered_df['duration'].empty else 0
            interval = 60000  # 1 minute intervals
            # Ensure bins start at 0 and handle potential NaN max_duration
            bins = list(range(0, int(max_duration) + interval, interval)) if pd.notnull(max_duration) and max_duration > 0 else [0, interval]
            if not bins or bins[-1] == 0 : bins = [0, interval] # Ensure at least one interval if data exists

            cumulative_lumber_delta_df_data = []
            for end in bins[1:]:
                filtered_bin_df = filtered_df[filtered_df['duration'] <= end]
                lumber_delta = 0
                count = 0 # Initialize count
                if not filtered_bin_df.empty:
                     # Check if required columns exist before calculating mean
                     if 'players_winner_all_summary_lumber' in filtered_bin_df.columns and 'players_loser_all_summary_lumber' in filtered_bin_df.columns:
                        winner_lumber_mean = filtered_bin_df['players_winner_all_summary_lumber'].mean()
                        loser_lumber_mean = filtered_bin_df['players_loser_all_summary_lumber'].mean()
                        if pd.notnull(winner_lumber_mean) and pd.notnull(loser_lumber_mean):
                             lumber_delta = winner_lumber_mean - loser_lumber_mean
                     count = filtered_bin_df.shape[0] # Get the count for the bin
                cumulative_lumber_delta_df_data.append({'duration': end, 'lumber_delta': lumber_delta, 'count': count}) # Add count here

            cumulative_lumber_delta_df = pd.DataFrame(cumulative_lumber_delta_df_data)

            if not cumulative_lumber_delta_df.empty:
                lumber_delta_fig = px.bar(
                    cumulative_lumber_delta_df,
                    x='duration',
                    y='lumber_delta',
                    text='count', # Add text labels based on the 'count' column
                    title='Delta of Total Lumber (Winner vs Loser) over Cumulative Duration Intervals',
                    labels={'duration': 'Duration (ms)', 'lumber_delta': 'Avg Lumber Delta', 'count': 'Games'}, # Update labels
                    hover_data={'count': True} # Ensure count appears in hover data
                )
                lumber_delta_fig.update_traces(texttemplate='n=%{text}', textposition='outside') # Format text and position
                lumber_delta_fig.update_xaxes(
                    tickmode='array',
                    tickvals=cumulative_lumber_delta_df['duration'],
                    ticktext=[f"{d} ms ({ms_to_mmss(d)})" for d in cumulative_lumber_delta_df['duration']]
                )
            else:
                 lumber_delta_fig = {'data': [], 'layout': {'title': 'No Data for Lumber Delta Graph'}}

        else: # Handle empty filtered_df for lumber delta
             lumber_delta_fig = {
                'data': [],
                'layout': {
                    'title': 'Delta of Total Lumber (Winner vs Loser) over Cumulative Duration Intervals',
                    'xaxis': {'title': 'Duration (ms)'}, 'yaxis': {'title': 'Lumber Delta'},
                    'annotations': [{'text': "No data available.", 'showarrow': False, 'xref': 'paper', 'yref': 'paper', 'x': 0.5, 'y': 0.5}]
                }
             }

        # Create winner lumber graph
        if not filtered_df.empty and 'duration' in filtered_df.columns:
             # Use the same bins as lumber delta graph
             lumber_summary_df_data = []
             for end in bins[1:]:
                 filtered_bin_df = filtered_df[filtered_df['duration'] <= end]
                 winner_lumber = 0
                 loser_lumber = 0
                 if not filtered_bin_df.empty:
                     if 'players_winner_all_summary_lumber' in filtered_bin_df.columns:
                         winner_lumber_mean = filtered_bin_df['players_winner_all_summary_lumber'].mean()
                         if pd.notnull(winner_lumber_mean): winner_lumber = winner_lumber_mean
                     if 'players_loser_all_summary_lumber' in filtered_bin_df.columns:
                         loser_lumber_mean = filtered_bin_df['players_loser_all_summary_lumber'].mean()
                         if pd.notnull(loser_lumber_mean): loser_lumber = loser_lumber_mean
                 lumber_summary_df_data.append({'duration': end, 'Winner Lumber': winner_lumber, 'Loser Lumber': loser_lumber})

             lumber_summary_df = pd.DataFrame(lumber_summary_df_data)

             if not lumber_summary_df.empty:
                 winner_lumber_fig = px.line(
                     lumber_summary_df,
                     x='duration',
                     y=['Winner Lumber', 'Loser Lumber'],
                     title='Avg Total Lumber (Winner vs Loser) over Cumulative Duration Intervals',
                     labels={'duration': 'Duration (ms)', 'value': 'Avg Lumber Amount', 'variable': 'Player Type'},
                     color_discrete_map={'Winner Lumber': 'blue', 'Loser Lumber': 'red'}
                 )
                 winner_lumber_fig.update_xaxes(
                     tickmode='array',
                     tickvals=lumber_summary_df['duration'],
                     ticktext=[f"{d} ms ({ms_to_mmss(d)})" for d in lumber_summary_df['duration']]
                 )
             else:
                  winner_lumber_fig = {'data': [], 'layout': {'title': 'No Data for Winner/Loser Lumber Graph'}}
        else: # Handle empty filtered_df for winner lumber
            winner_lumber_fig = {
                'data': [],
                'layout': {
                    'title': 'Players Winner and Loser All Summary Lumber over Increasing Duration Intervals',
                    'xaxis': {'title': 'Duration (ms)'}, 'yaxis': {'title': 'Lumber Amount'},
                    'annotations': [{'text': "No data available.", 'showarrow': False, 'xref': 'paper', 'yref': 'paper', 'x': 0.5, 'y': 0.5}]
                }
            }

        # Create gold delta bar graph (similar logic to lumber)
        if not filtered_df.empty and 'duration' in filtered_df.columns:
             # Use the same bins
             cumulative_gold_delta_df_data = []
             for end in bins[1:]:
                 filtered_bin_df = filtered_df[filtered_df['duration'] <= end]
                 gold_delta = 0
                 if not filtered_bin_df.empty:
                      if 'players_winner_all_summary_gold' in filtered_bin_df.columns and 'players_loser_all_summary_gold' in filtered_bin_df.columns:
                         winner_gold_mean = filtered_bin_df['players_winner_all_summary_gold'].mean()
                         loser_gold_mean = filtered_bin_df['players_loser_all_summary_gold'].mean()
                         if pd.notnull(winner_gold_mean) and pd.notnull(loser_gold_mean):
                              gold_delta = winner_gold_mean - loser_gold_mean
                 cumulative_gold_delta_df_data.append({'duration': end, 'gold_delta': gold_delta})

             cumulative_gold_delta_df = pd.DataFrame(cumulative_gold_delta_df_data)

             if not cumulative_gold_delta_df.empty:
                 gold_delta_fig = px.bar(
                     cumulative_gold_delta_df,
                     x='duration',
                     y='gold_delta',
                     title='Delta of Total Gold (Winner vs Loser) over Cumulative Duration Intervals',
                     labels={'duration': 'Duration (ms)', 'gold_delta': 'Avg Gold Delta'}
                 )
                 gold_delta_fig.update_xaxes(
                     tickmode='array',
                     tickvals=cumulative_gold_delta_df['duration'],
                     ticktext=[f"{d} ms ({ms_to_mmss(d)})" for d in cumulative_gold_delta_df['duration']]
                 )
             else:
                  gold_delta_fig = {'data': [], 'layout': {'title': 'No Data for Gold Delta Graph'}}

        else: # Handle empty filtered_df for gold delta
            gold_delta_fig = {
                'data': [],
                'layout': {
                    'title': 'Delta of Total Gold (Winner vs Loser) over Cumulative Duration Intervals',
                    'xaxis': {'title': 'Duration (ms)'}, 'yaxis': {'title': 'Gold Delta'},
                    'annotations': [{'text': "No data available.", 'showarrow': False, 'xref': 'paper', 'yref': 'paper', 'x': 0.5, 'y': 0.5}]
                }
            }

        # Create winner gold graph (similar logic to lumber)
        if not filtered_df.empty and 'duration' in filtered_df.columns:
            # Use the same bins
            gold_summary_df_data = []
            for end in bins[1:]:
                filtered_bin_df = filtered_df[filtered_df['duration'] <= end]
                winner_gold = 0
                loser_gold = 0
                if not filtered_bin_df.empty:
                     if 'players_winner_all_summary_gold' in filtered_bin_df.columns:
                        winner_gold_mean = filtered_bin_df['players_winner_all_summary_gold'].mean()
                        if pd.notnull(winner_gold_mean): winner_gold = winner_gold_mean
                     if 'players_loser_all_summary_gold' in filtered_bin_df.columns:
                         loser_gold_mean = filtered_bin_df['players_loser_all_summary_gold'].mean()
                         if pd.notnull(loser_gold_mean): loser_gold = loser_gold_mean
                gold_summary_df_data.append({'duration': end, 'Winner Gold': winner_gold, 'Loser Gold': loser_gold})

            gold_summary_df = pd.DataFrame(gold_summary_df_data)

            if not gold_summary_df.empty:
                winner_gold_fig = px.line(
                    gold_summary_df,
                    x='duration',
                    y=['Winner Gold', 'Loser Gold'],
                    title='Avg Total Gold (Winner vs Loser) over Cumulative Duration Intervals',
                    labels={'duration': 'Duration (ms)', 'value': 'Avg Gold Amount', 'variable': 'Player Type'},
                    color_discrete_map={'Winner Gold': 'gold', 'Loser Gold': 'silver'}
                )
                winner_gold_fig.update_xaxes(
                    tickmode='array',
                    tickvals=gold_summary_df['duration'],
                    ticktext=[f"{d} ms ({ms_to_mmss(d)})" for d in gold_summary_df['duration']]
                )
            else:
                 winner_gold_fig = {'data': [], 'layout': {'title': 'No Data for Winner/Loser Gold Graph'}}
        else: # Handle empty filtered_df for winner gold
            winner_gold_fig = {
                'data': [],
                'layout': {
                    'title': 'Players Winner and Loser All Summary Gold over Increasing Duration Intervals',
                    'xaxis': {'title': 'Duration (ms)'}, 'yaxis': {'title': 'Gold Amount'},
                    'annotations': [{'text': "No data available.", 'showarrow': False, 'xref': 'paper', 'yref': 'paper', 'x': 0.5, 'y': 0.5}]
                }
            }

        # Return results ensuring the order matches the Output list
        # Output order: table data, win %, lumber delta, winner lumber, gold delta, winner gold
        return results, win_percentage_display, lumber_delta_fig, winner_lumber_fig, gold_delta_fig, winner_gold_fig

    return dash_app
