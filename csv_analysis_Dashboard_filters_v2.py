import pandas as pd
import os
import dash
from dash import dcc, html, dash_table, Input, Output, State, MATCH, ALL
import logging

import warnings
warnings.simplefilter(action="ignore", category=pd.errors.SettingWithCopyWarning)

# Configure logging
logging.basicConfig(level=logging.INFO)

# Get the absolute path of the directory where the current script is located
script_dir = os.path.dirname(os.path.abspath(__file__))

# Construct the full path to 'wc3_filters.csv' and 'wc3_filters_heroes.csv' within the 'mappings' folder
filters_file_path = os.path.join(script_dir, 'mappings', 'wc3_filters.csv')
heroes_file_path = os.path.join(script_dir, 'mappings', 'wc3_filters_heroes.csv')  # Hero filters file

# Load 'wc3_filters.csv'
try:
    df_filters = pd.read_csv(filters_file_path, sep=';')
    logging.info("CSV file 'wc3_filters.csv' loaded successfully.")
except FileNotFoundError:
    logging.error(f"The file {filters_file_path} does not exist.")
    df_filters = pd.DataFrame()
except pd.errors.EmptyDataError:
    logging.error(f"The file {filters_file_path} is empty.")
    df_filters = pd.DataFrame()
except pd.errors.ParserError:
    logging.error(f"The file {filters_file_path} is not in CSV format.")
    df_filters = pd.DataFrame()
except Exception as e:
    logging.error(f"Unexpected error loading 'wc3_filters.csv': {e}")
    df_filters = pd.DataFrame()

logging.info(f"Columns in df_filters: {df_filters.columns.tolist()}")
if df_filters.empty:
    raise ValueError("df_filters is empty. Please check 'wc3_filters.csv'.")

df_filters.columns = df_filters.columns.str.strip().str.lower()

required_columns = ['race', 'name', 'type', 'string_winner', 'string_loser']
missing_columns = [col for col in required_columns if col not in df_filters.columns]
if missing_columns:
    raise KeyError(f"Missing required columns in df_filters: {missing_columns}")

df_filters_sorted = df_filters.sort_values(by=['race', 'type', 'name']).reset_index(drop=True)
# logging.info(f"First few rows of df_filters_sorted:\n{df_filters_sorted.head()}")

# Load 'wc3_filters_heroes.csv'
try:
    df_filters_heroes = pd.read_csv(heroes_file_path, sep=';')
    logging.info("Hero filters CSV file 'wc3_filters_heroes.csv' loaded successfully.")
except FileNotFoundError:
    logging.error(f"The file {heroes_file_path} does not exist.")
    df_filters_heroes = pd.DataFrame()
except pd.errors.EmptyDataError:
    logging.error(f"The file {heroes_file_path} is empty.")
    df_filters_heroes = pd.DataFrame()
except pd.errors.ParserError:
    logging.error(f"The file {heroes_file_path} is not in CSV format.")
    df_filters_heroes = pd.DataFrame()
except Exception as e:
    logging.error(f"Unexpected error loading 'wc3_filters_heroes.csv': {e}")
    df_filters_heroes = pd.DataFrame()

logging.info(f"Columns in df_filters_heroes: {df_filters_heroes.columns.tolist()}")
if df_filters_heroes.empty:
    raise ValueError("df_filters_heroes is empty. Please check 'wc3_filters_heroes.csv'.")

df_filters_heroes.columns = df_filters_heroes.columns.str.strip().str.lower()

required_columns_heroes = ['name', 'mapping']
missing_columns_heroes = [col for col in required_columns_heroes if col not in df_filters_heroes.columns]
if missing_columns_heroes:
    raise KeyError(f"Missing required columns in df_filters_heroes: {missing_columns_heroes}")

df_filters_heroes_sorted = df_filters_heroes.sort_values(by=['name']).reset_index(drop=True)
logging.info(f"First few rows of df_filters_heroes_sorted:\n{df_filters_heroes_sorted.head()}")

def ms_to_mmss(ms):
    if pd.isnull(ms):
        return "00:00"
    seconds = int(ms / 1000)
    minutes = seconds // 60
    seconds %= 60
    return f"{minutes:02d}:{seconds:02d}"

def load_data(file_path):
    try:
        if file_path.endswith('.csv'):
            df_main_data = pd.read_csv(file_path, low_memory=False) # Renamed to avoid conflict
        else:
            raise ValueError("Unsupported file type. Please provide a CSV file.")
        df_main_data['players_winner_raceDetected'] = df_main_data['players_winner_raceDetected'].astype(str).str.strip().str.upper()
        df_main_data['players_loser_raceDetected'] = df_main_data['players_loser_raceDetected'].astype(str).str.strip().str.upper()
        df_main_data['players_winner_raceDetected'] = df_main_data['players_winner_raceDetected'].replace({'NAN': 'UNKNOWN', '': 'UNKNOWN'})
        df_main_data['players_loser_raceDetected'] = df_main_data['players_loser_raceDetected'].replace({'NAN': 'UNKNOWN', '': 'UNKNOWN'})
        return df_main_data
    except Exception as e:
        logging.error(f"Error loading data: {e}")
        return None

def calculate_total_gold_units(df_calc):
    winner_cols = [c for c in df_calc.columns if c.startswith('players_winner_units_summary_') and c.endswith('_gold')]
    df_calc['players_winner_units_summary_total_gold'] = df_calc[winner_cols].sum(axis=1) if winner_cols else 0
    loser_cols = [c for c in df_calc.columns if c.startswith('players_loser_units_summary_') and c.endswith('_gold')]
    df_calc['players_loser_units_summary_total_gold'] = df_calc[loser_cols].sum(axis=1) if loser_cols else 0
    return df_calc

def calculate_total_lumber_buildings(df_calc):
    winner_cols = [c for c in df_calc.columns if c.startswith('players_winner_buildings_summary_') and c.endswith('_lumber')]
    df_calc['players_winner_buildings_summary_total_lumber'] = df_calc[winner_cols].sum(axis=1) if winner_cols else 0
    loser_cols = [c for c in df_calc.columns if c.startswith('players_loser_buildings_summary_') and c.endswith('_lumber')]
    df_calc['players_loser_buildings_summary_total_lumber'] = df_calc[loser_cols].sum(axis=1) if loser_cols else 0
    return df_calc

def calculate_total_lumber_upgrades(df_calc):
    winner_cols = [c for c in df_calc.columns if c.startswith('players_winner_upgrades_summary_') and c.endswith('_lumber')]
    df_calc['players_winner_upgrades_summary_total_lumber'] = df_calc[winner_cols].sum(axis=1) if winner_cols else 0
    loser_cols = [c for c in df_calc.columns if c.startswith('players_loser_upgrades_summary_') and c.endswith('_lumber')]
    df_calc['players_loser_upgrades_summary_total_lumber'] = df_calc[loser_cols].sum(axis=1) if loser_cols else 0
    return df_calc

def calculate_total_gold_buildings(df_calc):
    winner_cols = [c for c in df_calc.columns if c.startswith('players_winner_buildings_summary_') and c.endswith('_gold')]
    df_calc['players_winner_buildings_summary_total_gold'] = df_calc[winner_cols].sum(axis=1) if winner_cols else 0
    loser_cols = [c for c in df_calc.columns if c.startswith('players_loser_buildings_summary_') and c.endswith('_gold')]
    df_calc['players_loser_buildings_summary_total_gold'] = df_calc[loser_cols].sum(axis=1) if loser_cols else 0
    return df_calc

def calculate_total_gold_upgrades(df_calc):
    winner_cols = [c for c in df_calc.columns if c.startswith('players_winner_upgrades_summary_') and c.endswith('_gold')]
    df_calc['players_winner_upgrades_summary_total_gold'] = df_calc[winner_cols].sum(axis=1) if winner_cols else 0
    loser_cols = [c for c in df_calc.columns if c.startswith('players_loser_upgrades_summary_') and c.endswith('_gold')]
    df_calc['players_loser_upgrades_summary_total_gold'] = df_calc[loser_cols].sum(axis=1) if loser_cols else 0
    return df_calc

def calculate_total_gold_items(df_calc):
    winner_cols = [c for c in df_calc.columns if c.startswith('players_winner_items_summary_') and c.endswith('_gold')]
    df_calc['players_winner_items_summary_total_gold'] = df_calc[winner_cols].sum(axis=1) if winner_cols else 0
    loser_cols = [c for c in df_calc.columns if c.startswith('players_loser_items_summary_') and c.endswith('_gold')]
    df_calc['players_loser_items_summary_total_gold'] = df_calc[loser_cols].sum(axis=1) if loser_cols else 0
    return df_calc

def calculate_total_lumber_units(df_calc):
    winner_cols = [c for c in df_calc.columns if c.startswith('players_winner_units_summary_') and c.endswith('_lumber')]
    df_calc['players_winner_units_summary_total_lumber'] = df_calc[winner_cols].sum(axis=1) if winner_cols else 0
    loser_cols = [c for c in df_calc.columns if c.startswith('players_loser_units_summary_') and c.endswith('_lumber')]
    df_calc['players_loser_units_summary_total_lumber'] = df_calc[loser_cols].sum(axis=1) if loser_cols else 0
    return df_calc

def calculate_total_food_units(df_calc):
    winner_cols = [c for c in df_calc.columns if c.startswith('players_winner_units_summary_') and c.endswith('_food')]
    df_calc['players_winner_units_summary_total_food'] = df_calc[winner_cols].sum(axis=1) if winner_cols else 0
    loser_cols = [c for c in df_calc.columns if c.startswith('players_loser_units_summary_') and c.endswith('_food')]
    df_calc['players_loser_units_summary_total_food'] = df_calc[loser_cols].sum(axis=1) if loser_cols else 0
    return df_calc

def calculate_total_buildtime_units(df_calc):
    winner_cols = [c for c in df_calc.columns if c.startswith('players_winner_units_summary_') and c.endswith('_buildtime')]
    df_calc['players_winner_units_summary_total_buildtime'] = df_calc[winner_cols].sum(axis=1) if winner_cols else 0
    loser_cols = [c for c in df_calc.columns if c.startswith('players_loser_units_summary_') and c.endswith('_buildtime')]
    df_calc['players_loser_units_summary_total_buildtime'] = df_calc[loser_cols].sum(axis=1) if loser_cols else 0
    return df_calc

def calculate_total_gold_all(df_calc):
    w_cols = [
        'players_winner_units_summary_total_gold',
        'players_winner_buildings_summary_total_gold',
        'players_winner_upgrades_summary_total_gold',
        'players_winner_items_summary_total_gold'
    ]
    df_calc['players_winner_all_summary_gold'] = df_calc[w_cols].sum(axis=1) if all(c in df_calc.columns for c in w_cols) else 0

    l_cols = [
        'players_loser_units_summary_total_gold',
        'players_loser_buildings_summary_total_gold',
        'players_loser_upgrades_summary_total_gold',
        'players_loser_items_summary_total_gold'
    ]
    df_calc['players_loser_all_summary_gold'] = df_calc[l_cols].sum(axis=1) if all(c in df_calc.columns for c in l_cols) else 0
    return df_calc

def calculate_total_lumber_all(df_calc):
    w_cols = [
        'players_winner_units_summary_total_lumber',
        'players_winner_buildings_summary_total_lumber',
        'players_winner_upgrades_summary_total_lumber'
    ]
    df_calc['players_winner_all_summary_lumber'] = df_calc[w_cols].sum(axis=1) if all(c in df_calc.columns for c in w_cols) else 0

    l_cols = [
        'players_loser_units_summary_total_lumber',
        'players_loser_buildings_summary_total_lumber',
        'players_loser_upgrades_summary_total_lumber'
    ]
    df_calc['players_loser_all_summary_lumber'] = df_calc[l_cols].sum(axis=1) if all(c in df_calc.columns for c in l_cols) else 0
    return df_calc

def calculate_avg_std(df_calc, column):
    avg = df_calc[column].mean()
    std_dev = df_calc[column].std()
    count = df_calc.shape[0]
    return avg, std_dev, count

# Load the main data (globally for this module)
main_data_file_path = os.path.join(script_dir, 'working_directory', 'combined_replay_data_enhanced.csv')
df_global_filters = load_data(main_data_file_path) # Renamed to avoid conflict with other df variables
if df_global_filters is None:
    raise Exception("Filters dashboard data could not be loaded. Check file path and format.")

def create_filters_dash_app(flask_server, url_base_pathname):
    filters_dash_app = dash.Dash(
        server=flask_server,
        url_base_pathname=url_base_pathname,
        suppress_callback_exceptions=True
    )

    # Use the globally loaded df_global_filters for this app instance
    # This ensures data is loaded once per module import, not per app creation call
    # However, callbacks should operate on copies if they modify data,
    # or use the passed df from load_data if it's called within create_filters_dash_app

    filters_dash_app.layout = html.Div([
        html.Div(
            dcc.Link(html.Button("Back to Main"), href='/', refresh=True),
            style={'marginBottom': '20px', 'textAlign': 'left'}  # Added textAlign for better alignment
        ),
        html.H1("Replay Data Analysis with Advanced Filters"), # Modified Title
        html.Div([
            html.H3("Win Percentage and Total Games"),
            html.Div(id='win-percentage-display-filters', style={'fontSize': 20, 'padding': '10px'}) # Unique ID
        ], style={
            'padding': '20px',
            'backgroundColor': 'rgb(245, 245, 245)',
            'borderRadius': '5px',
            'marginBottom': '20px'
        }),
        html.Div([
            html.H3("Win Rate - Heroes selected"),
            html.Div(id='win-rate-heroes-selected-display-filters', style={'fontSize': 20, 'padding': '10px'}) # Unique ID
        ], style={
            'padding': '20px',
            'backgroundColor': 'rgb(245, 245, 245)',
            'borderRadius': '5px',
            'marginBottom': '20px'
        }),
        html.Div([
            html.Div([
                html.Label('Filter by Winner Race:'),
                dcc.Dropdown(
                    id='avg-std-winner-race-dropdown-filters', # Unique ID
                    options=[{'label': r, 'value': r} for r in df_global_filters['players_winner_raceDetected'].unique()],
                    value=None,
                    placeholder="Select Winner Race",
                    clearable=True
                ),
                html.Br(),
                html.Label('Filter by Loser Race:'),
                dcc.Dropdown(
                    id='avg-std-loser-race-dropdown-filters', # Unique ID
                    options=[{'label': r, 'value': r} for r in df_global_filters['players_loser_raceDetected'].unique()],
                    value=None,
                    placeholder="Select Loser Race",
                    clearable=True
                ),
                html.Br(),
                html.Label('Filter by Duration Range (ms):'),
                html.Div([
                    dcc.Input(
                        id='duration-lower-input-filters', # Unique ID
                        type='number',
                        placeholder='Lower Bound',
                        style={'marginRight': '10px'}
                    ),
                    dcc.Input(
                        id='duration-upper-input-filters', # Unique ID
                        type='number',
                        placeholder='Upper Bound'
                    ),
                ]),
                html.Br(),
                html.H2("Hero Filters"),
                html.Div([
                    html.Div([
                        html.H3("Winner Heroes"),
                        html.Div([
                            html.Label('1. Hero Winner:'),
                            dcc.Dropdown(
                                id='hero-winner-dropdown-1-filters', # Unique ID
                                options=[{'label': n, 'value': m} for n, m in zip(
                                    df_filters_heroes_sorted['name'],
                                    df_filters_heroes_sorted['mapping']
                                )],
                                value=None,
                                placeholder="Select 1. Hero Winner",
                                clearable=True
                            )
                        ], style={'paddingTop': '10px'}),
                        html.Br(),
                        html.Div([
                            html.Label('2. Hero Winner:'),
                            dcc.Dropdown(
                                id='hero-winner-dropdown-2-filters', # Unique ID
                                options=[{'label': n, 'value': m} for n, m in zip(
                                    df_filters_heroes_sorted['name'],
                                    df_filters_heroes_sorted['mapping']
                                )],
                                value=None,
                                placeholder="Select 2. Hero Winner",
                                clearable=True
                            )
                        ], style={'paddingTop': '10px'}),
                        html.Br(),
                        html.Div([
                            html.Label('3. Hero Winner:'),
                            dcc.Dropdown(
                                id='hero-winner-dropdown-3-filters', # Unique ID
                                options=[{'label': n, 'value': m} for n, m in zip(
                                    df_filters_heroes_sorted['name'],
                                    df_filters_heroes_sorted['mapping']
                                )],
                                value=None,
                                placeholder="Select 3. Hero Winner",
                                clearable=True
                            )
                        ], style={'paddingTop': '10px'}),
                    ], style={'width': '48%', 'display': 'inline-block', 'verticalAlign': 'top'}),

                    html.Div(style={'width': '4%', 'display': 'inline-block'}),

                    html.Div([
                        html.H3("Loser Heroes"),
                        html.Div([
                            html.Label('1. Hero Loser:'),
                            dcc.Dropdown(
                                id='hero-loser-dropdown-1-filters', # Unique ID
                                options=[{'label': n, 'value': m} for n, m in zip(
                                    df_filters_heroes_sorted['name'],
                                    df_filters_heroes_sorted['mapping']
                                )],
                                value=None,
                                placeholder="Select 1. Hero Loser",
                                clearable=True
                            )
                        ], style={'paddingTop': '10px'}),
                        html.Br(),
                        html.Div([
                            html.Label('2. Hero Loser:'),
                            dcc.Dropdown(
                                id='hero-loser-dropdown-2-filters', # Unique ID
                                options=[{'label': n, 'value': m} for n, m in zip(
                                    df_filters_heroes_sorted['name'],
                                    df_filters_heroes_sorted['mapping']
                                )],
                                value=None,
                                placeholder="Select 2. Hero Loser",
                                clearable=True
                            )
                        ], style={'paddingTop': '10px'}),
                        html.Br(),
                        html.Div([
                            html.Label('3. Hero Loser:'),
                            dcc.Dropdown(
                                id='hero-loser-dropdown-3-filters', # Unique ID
                                options=[{'label': n, 'value': m} for n, m in zip(
                                    df_filters_heroes_sorted['name'],
                                    df_filters_heroes_sorted['mapping']
                                )],
                                value=None,
                                placeholder="Select 3. Hero Loser",
                                clearable=True
                            )
                        ], style={'paddingTop': '10px'}),
                    ], style={'width': '48%', 'display': 'inline-block', 'verticalAlign': 'top'}),
                ], style={'display': 'flex', 'justifyContent': 'space-between'}),
                html.Br(),
                html.H2("Additional Filters"),
                html.Div([
                    html.Div("Human", style={'width': '23%', 'textAlign': 'center', 'fontWeight': 'bold', 'display': 'inline-block'}),
                    html.Div("Night Elf", style={'width': '23%', 'textAlign': 'center', 'fontWeight': 'bold', 'display': 'inline-block'}),
                    html.Div("Undead", style={'width': '23%', 'textAlign': 'center', 'fontWeight': 'bold', 'display': 'inline-block'}),
                    html.Div("Orc", style={'width': '23%', 'textAlign': 'center', 'fontWeight': 'bold', 'display': 'inline-block'}),
                ], style={'display': 'flex', 'justifyContent': 'space-between'}),
                html.Div([
                    html.Div([
                        *[
                            html.Div([
                                html.Label(f"{r['race']} {r['name']} {r['type']}:"),
                                dcc.Input(
                                    id={'type': 'additional-filter-filters', 'index': idx}, # Unique ID pattern
                                    type='number',
                                    placeholder=f"Minimum {r['name']} {r['type']}"
                                ),
                                html.Br()
                            ]) for idx, r in df_filters_sorted[df_filters_sorted['race'].str.lower() == 'human'].iterrows()
                        ]
                    ], style={'width': '23%', 'display': 'inline-block', 'verticalAlign': 'top'}),
                    html.Div([
                        *[
                            html.Div([
                                html.Label(f"{r['race']} {r['name']} {r['type']}:"),
                                dcc.Input(
                                    id={'type': 'additional-filter-filters', 'index': idx}, # Unique ID pattern
                                    type='number',
                                    placeholder=f"Minimum {r['name']} {r['type']}"
                                ),
                                html.Br()
                            ]) for idx, r in df_filters_sorted[df_filters_sorted['race'].str.lower() == 'night elf'].iterrows()
                        ]
                    ], style={'width': '23%', 'display': 'inline-block', 'verticalAlign': 'top'}),
                    html.Div([
                        *[
                            html.Div([
                                html.Label(f"{r['race']} {r['name']} {r['type']}:"),
                                dcc.Input(
                                    id={'type': 'additional-filter-filters', 'index': idx}, # Unique ID pattern
                                    type='number',
                                    placeholder=f"Minimum {r['name']} {r['type']}"
                                ),
                                html.Br()
                            ]) for idx, r in df_filters_sorted[df_filters_sorted['race'].str.lower() == 'undead'].iterrows()
                        ]
                    ], style={'width': '23%', 'display': 'inline-block', 'verticalAlign': 'top'}),
                    html.Div([
                        *[
                            html.Div([
                                html.Label(f"{r['race']} {r['name']} {r['type']}:"),
                                dcc.Input(
                                    id={'type': 'additional-filter-filters', 'index': idx}, # Unique ID pattern
                                    type='number',
                                    placeholder=f"Minimum {r['name']} {r['type']}"
                                ),
                                html.Br()
                            ]) for idx, r in df_filters_sorted[df_filters_sorted['race'].str.lower() == 'orc'].iterrows()
                        ]
                    ], style={'width': '23%', 'display': 'inline-block', 'verticalAlign': 'top'}),
                ], style={'display': 'flex', 'justifyContent': 'space-between'}),
            ], style={'width': '48%', 'display': 'inline-block', 'verticalAlign': 'top', 'padding': '20px'}),

            html.Div([
                dash_table.DataTable(
                    id='avg-std-table-filters', # Unique ID
                    columns=[
                        {"name": "Metric", "id": "metric"},
                        {"name": "Average", "id": "average"},
                        {"name": "Standard Deviation", "id": "std_dev"},
                        {"name": "Data Points Count", "id": "count"}
                    ],
                    data=[],
                    filter_action='native',
                    sort_action='native',
                    page_action='none',
                    style_table={'overflowX': 'auto'},
                    style_cell_conditional=[
                        {
                            'if': {'column_id': 'metric'},
                            'minWidth': '200px',
                            'width': 'auto',
                            'whiteSpace': 'normal',
                            'textAlign': 'left'
                        }
                    ],
                    style_cell={
                        'minWidth': '100px',
                        'width': '150px',
                        'maxWidth': '180px',
                        'whiteSpace': 'normal',
                        'textAlign': 'left'
                    },
                    style_header={
                        'backgroundColor': 'rgb(230, 230, 230)',
                        'fontWeight': 'bold'
                    }
                )
            ], style={'width': '48%', 'display': 'inline-block', 'padding': '20px'}),
        ], style={'display': 'flex', 'justifyContent': 'space-between'}),
        html.Hr(),
    ], style={'width': '100%', 'margin': '0 auto'})

    @filters_dash_app.callback(
        [
            Output('avg-std-table-filters', 'data'),
            Output('win-percentage-display-filters', 'children'),
            Output('win-rate-heroes-selected-display-filters', 'children')
        ],
        [
            Input('avg-std-winner-race-dropdown-filters', 'value'),
            Input('avg-std-loser-race-dropdown-filters', 'value'),
            Input('duration-lower-input-filters', 'value'),
            Input('duration-upper-input-filters', 'value'),
            Input({'type': 'additional-filter-filters', 'index': ALL}, 'value'),
            Input({'type': 'additional-filter-filters', 'index': ALL}, 'id'),
            Input('hero-winner-dropdown-1-filters', 'value'),
            Input('hero-winner-dropdown-2-filters', 'value'),
            Input('hero-winner-dropdown-3-filters', 'value'),
            Input('hero-loser-dropdown-1-filters', 'value'),
            Input('hero-loser-dropdown-2-filters', 'value'),
            Input('hero-loser-dropdown-3-filters', 'value')
        ]
    )
    def update_avg_std_table_filters( # Renamed callback function
        winner_race, loser_race, duration_lower, duration_upper,
        additional_filters_values, additional_filters_ids,
        hero_winner_1_mapping,
        hero_winner_2_mapping,
        hero_winner_3_mapping,
        hero_loser_1_mapping,
        hero_loser_2_mapping,
        hero_loser_3_mapping
    ):
        logging.info("Callback triggered for filters dashboard with filters:")
        logging.info(f"Winner Race: {winner_race}, Loser Race: {loser_race}")
        logging.info(f"Duration Range: {duration_lower} to {duration_upper}")
        logging.info(f"Additional Filters Values: {additional_filters_values}")
        logging.info(f"Additional Filters IDs: {additional_filters_ids}")
        logging.info(f"Hero Winner Mappings: {hero_winner_1_mapping}, {hero_winner_2_mapping}, {hero_winner_3_mapping}")
        logging.info(f"Hero Loser Mappings: {hero_loser_1_mapping}, {hero_loser_2_mapping}, {hero_loser_3_mapping}")

        additional_filters_map = { id_dict['index']: value for id_dict, value in zip(additional_filters_ids, additional_filters_values) }
        
        # Use a copy of the globally loaded dataframe for filtering
        df_copy = df_global_filters.copy()

        # ================
        # PART 1: Table filter
        # ================
        mask_table = pd.Series([True] * len(df_copy))

        if winner_race:
            mask_table &= (df_copy['players_winner_raceDetected'] == winner_race)
        if loser_race:
            mask_table &= (df_copy['players_loser_raceDetected'] == loser_race)

        if duration_lower is not None and duration_upper is not None:
            if duration_lower > duration_upper:
                duration_lower, duration_upper = duration_upper, duration_lower
            mask_table &= (df_copy['duration'] >= duration_lower) & (df_copy['duration'] <= duration_upper)

        for idx, filter_value in additional_filters_map.items():
            if filter_value is not None:
                try:
                    row = df_filters_sorted.loc[idx]
                except KeyError:
                    logging.warning(f"No df_filters row found for index {idx}. Skipping.")
                    continue

                sw = row['string_winner']
                sl = row['string_loser']
                logging.info(f"Applying additional filter idx={idx}, value={filter_value}: sw={sw}, sl={sl}")

                if sw in df_copy.columns and sl in df_copy.columns:
                    df_copy[sw] = pd.to_numeric(df_copy[sw], errors='coerce').fillna(0)
                    df_copy[sl] = pd.to_numeric(df_copy[sl], errors='coerce').fillna(0)
                    mask_table &= ((df_copy[sw] >= filter_value) | (df_copy[sl] >= filter_value))

        # Apply Winner Hero filters (position-specific)
        if hero_winner_1_mapping:
            mask_table &= (df_copy['players_winner_heroes_0_id'] == hero_winner_1_mapping)
        if hero_winner_2_mapping:
            mask_table &= (df_copy['players_winner_heroes_1_id'] == hero_winner_2_mapping)
        if hero_winner_3_mapping:
            mask_table &= (df_copy['players_winner_heroes_2_id'] == hero_winner_3_mapping)

        # Apply Loser Hero filters (position-specific)
        if hero_loser_1_mapping:
            mask_table &= (df_copy['players_loser_heroes_0_id'] == hero_loser_1_mapping)
        if hero_loser_2_mapping:
            mask_table &= (df_copy['players_loser_heroes_1_id'] == hero_loser_2_mapping)
        if hero_loser_3_mapping:
            mask_table &= (df_copy['players_loser_heroes_2_id'] == hero_loser_3_mapping)

        table_df = df_copy[mask_table]

        table_df = calculate_total_gold_units(table_df.copy())
        table_df = calculate_total_lumber_buildings(table_df.copy())
        table_df = calculate_total_lumber_upgrades(table_df.copy())
        table_df = calculate_total_gold_buildings(table_df.copy())
        table_df = calculate_total_gold_upgrades(table_df.copy())
        table_df = calculate_total_gold_items(table_df.copy())
        table_df = calculate_total_lumber_units(table_df.copy())
        table_df = calculate_total_food_units(table_df.copy())
        table_df = calculate_total_buildtime_units(table_df.copy())
        table_df = calculate_total_gold_all(table_df.copy())
        table_df = calculate_total_lumber_all(table_df.copy())

        required_columns_summary = [
            'players_winner_units_summary_total_gold',
            'players_loser_units_summary_total_gold',
            'players_winner_units_summary_total_lumber',
            'players_loser_units_summary_total_lumber',
            'players_winner_units_summary_total_food',
            'players_loser_units_summary_total_food',
            'players_winner_units_summary_total_buildtime',
            'players_loser_units_summary_total_buildtime',
            'players_winner_upgrades_summary_total_gold',
            'players_loser_upgrades_summary_total_gold',
            'players_winner_upgrades_summary_total_lumber',
            'players_loser_upgrades_summary_total_lumber',
            'players_winner_buildings_summary_total_gold',
            'players_loser_buildings_summary_total_gold',
            'players_winner_buildings_summary_total_lumber',
            'players_loser_buildings_summary_total_lumber',
            'players_winner_items_summary_total_gold',
            'players_loser_items_summary_total_gold',
            'players_winner_all_summary_gold',
            'players_loser_all_summary_gold',
            'players_winner_all_summary_lumber',
            'players_loser_all_summary_lumber'
        ]
        missing_cols = [c for c in required_columns_summary if c not in table_df.columns]
        for col in missing_cols:
            table_df[col] = 0

        columns_to_analyze = [
            'players_winner_units_summary_total_gold',
            'players_loser_units_summary_total_gold',
            'players_winner_units_summary_total_lumber',
            'players_loser_units_summary_total_lumber',
            'players_winner_units_summary_total_food',
            'players_loser_units_summary_total_food',
            'players_winner_units_summary_total_buildtime',
            'players_loser_units_summary_total_buildtime',
            'players_winner_upgrades_summary_total_gold',
            'players_loser_upgrades_summary_total_gold',
            'players_winner_upgrades_summary_total_lumber',
            'players_loser_upgrades_summary_total_lumber',
            'players_winner_buildings_summary_total_gold',
            'players_loser_buildings_summary_total_gold',
            'players_winner_buildings_summary_total_lumber',
            'players_loser_buildings_summary_total_lumber',
            'players_winner_items_summary_total_gold',
            'players_loser_items_summary_total_gold',
            'players_winner_all_summary_gold',
            'players_loser_all_summary_gold',
            'players_winner_all_summary_lumber',
            'players_loser_all_summary_lumber'
        ]
        
        # Ensure all columns from required_columns_summary are included in columns_to_analyze
        # and also ensure all columns needed for calculation functions are present.
        # This is a simplified placeholder; you might need more robust column checking.
        columns_to_analyze = list(set(columns_to_analyze + required_columns_summary))

        results = []
        for column in columns_to_analyze:
            if column not in table_df.columns: # Ensure column exists
                logging.warning(f"Column {column} not found in table_df for analysis. Skipping.")
                results.append({
                    "metric": column, "average": "N/A", "std_dev": "N/A", "count": 0
                })
                continue
            avg, std_dev, count = calculate_avg_std(table_df, column)
            if 'buildtime' in column or 'duration' in column:
                avg_fmt = f"{round(avg, 2)} ms ({ms_to_mmss(avg)})" if pd.notnull(avg) else "0 ms (00:00)"
                std_dev_fmt = f"{round(std_dev, 2)} ms ({ms_to_mmss(std_dev)})" if pd.notnull(std_dev) else "0 ms (00:00)"
            else:
                avg_fmt = round(avg, 2) if pd.notnull(avg) else 0
                std_dev_fmt = round(std_dev, 2) if pd.notnull(std_dev) else 0
            results.append({
                "metric": column,
                "average": avg_fmt,
                "std_dev": std_dev_fmt,
                "count": count
            })

        # ================
        # PART 2: DFCount_Winner_Filter & DFCount_Loser_Filter
        # ================
        DFCount_Winner_Filter = 0
        DFCount_Loser_Filter = 0
        if winner_race and loser_race:
            w_mask = (df_copy['players_winner_raceDetected'] == winner_race) & (df_copy['players_loser_raceDetected'] == loser_race)
            if duration_lower is not None and duration_upper is not None:
                 w_mask &= (df_copy['duration'] >= duration_lower) & (df_copy['duration'] <= duration_upper)
            for idx, fv in additional_filters_map.items():
                if fv is not None:
                    try: row = df_filters_sorted.loc[idx]
                    except KeyError: continue
                    sw, sl = row['string_winner'], row['string_loser']
                    if sw in df_copy.columns and sl in df_copy.columns:
                         df_copy[sw] = pd.to_numeric(df_copy[sw], errors='coerce').fillna(0)
                         df_copy[sl] = pd.to_numeric(df_copy[sl], errors='coerce').fillna(0)
                         w_mask &= ((df_copy[sw] >= fv) | (df_copy[sl] >= fv))
            
            # Apply Winner Hero filters (position-specific) for w_mask
            if hero_winner_1_mapping:
                w_mask &= (df_copy['players_winner_heroes_0_id'] == hero_winner_1_mapping)
            if hero_winner_2_mapping:
                w_mask &= (df_copy['players_winner_heroes_1_id'] == hero_winner_2_mapping)
            if hero_winner_3_mapping:
                w_mask &= (df_copy['players_winner_heroes_2_id'] == hero_winner_3_mapping)

            # Apply Loser Hero filters (position-specific) for w_mask
            if hero_loser_1_mapping:
                w_mask &= (df_copy['players_loser_heroes_0_id'] == hero_loser_1_mapping)
            if hero_loser_2_mapping:
                w_mask &= (df_copy['players_loser_heroes_1_id'] == hero_loser_2_mapping)
            if hero_loser_3_mapping:
                w_mask &= (df_copy['players_loser_heroes_2_id'] == hero_loser_3_mapping)
            DFCount_Winner_Filter = df_copy[w_mask].shape[0]

            l_mask = (df_copy['players_winner_raceDetected'] == loser_race) & (df_copy['players_loser_raceDetected'] == winner_race)
            if duration_lower is not None and duration_upper is not None:
                l_mask &= (df_copy['duration'] >= duration_lower) & (df_copy['duration'] <= duration_upper)
            for idx, fv in additional_filters_map.items():
                 if fv is not None:
                    try: row = df_filters_sorted.loc[idx]
                    except KeyError: continue
                    sw, sl = row['string_winner'], row['string_loser'] # These are general, not tied to winner/loser player
                    if sw in df_copy.columns and sl in df_copy.columns:
                         df_copy[sw] = pd.to_numeric(df_copy[sw], errors='coerce').fillna(0)
                         df_copy[sl] = pd.to_numeric(df_copy[sl], errors='coerce').fillna(0)
                         l_mask &= ((df_copy[sw] >= fv) | (df_copy[sl] >= fv)) # Applied to the game row

            # For l_mask, hero_winner_X_mapping applies to players_loser_heroes_X_id,
            # and hero_loser_X_mapping applies to players_winner_heroes_X_id.

            # Apply "Winner Hero" dropdown selections to the game's LOSER heroes (position-specific) for l_mask
            if hero_winner_1_mapping: # From "1. Hero Winner" dropdown
                l_mask &= (df_copy['players_loser_heroes_0_id'] == hero_winner_1_mapping)
            if hero_winner_2_mapping: # From "2. Hero Winner" dropdown
                l_mask &= (df_copy['players_loser_heroes_1_id'] == hero_winner_2_mapping)
            if hero_winner_3_mapping: # From "3. Hero Winner" dropdown
                l_mask &= (df_copy['players_loser_heroes_2_id'] == hero_winner_3_mapping)

            # Apply "Loser Hero" dropdown selections to the game's WINNER heroes (position-specific) for l_mask
            if hero_loser_1_mapping: # From "1. Hero Loser" dropdown
                l_mask &= (df_copy['players_winner_heroes_0_id'] == hero_loser_1_mapping)
            if hero_loser_2_mapping: # From "2. Hero Loser" dropdown
                l_mask &= (df_copy['players_winner_heroes_1_id'] == hero_loser_2_mapping)
            if hero_loser_3_mapping: # From "3. Hero Loser" dropdown
                l_mask &= (df_copy['players_winner_heroes_2_id'] == hero_loser_3_mapping)
            DFCount_Loser_Filter = df_copy[l_mask].shape[0]

        # ================
        # PART 3: Win Percentage
        # ================
        if (DFCount_Winner_Filter + DFCount_Loser_Filter) == 0:
            win_percentage_display = "No matching games found based on the selected filters."
        else:
            win_percent_calc = (DFCount_Winner_Filter / (DFCount_Winner_Filter + DFCount_Loser_Filter)) * 100
            total_games = DFCount_Winner_Filter + DFCount_Loser_Filter
            win_percentage_display = (
                f"Win Percentage: {win_percent_calc:.2f}% | Total Games: {total_games} | "
                f"{winner_race or 'N/A'} win count: {DFCount_Winner_Filter}, "
                f"{loser_race or 'N/A'} loss count: {DFCount_Loser_Filter}"
            )
            
        # ================
        # PART 4: Win Rate - Heroes selected (This part might need re-evaluation based on clear definition)
        # For now, it's the same as overall win percentage given the filters include heroes.
        # ================
        if (DFCount_Winner_Filter + DFCount_Loser_Filter) > 0:
            # This calculation is identical to win_percent_calc if heroes are part of the main filter.
            # The meaning might need to be "win rate WHEN these specific heroes are involved as selected (winner heroes for winner, loser heroes for loser)"
            # which is what DFCount_Winner_Filter already represents for the "winner" side of the matchup.
            win_rate_heroes_selected_calc = (DFCount_Winner_Filter / (DFCount_Winner_Filter + DFCount_Loser_Filter)) * 100
            win_rate_heroes_selected_display = f"Filtered Win Rate: {win_rate_heroes_selected_calc:.2f}% (based on current filters including heroes)"
        else:
            win_rate_heroes_selected_display = "Filtered Win Rate: N/A"

        return results, win_percentage_display, win_rate_heroes_selected_display

    return filters_dash_app