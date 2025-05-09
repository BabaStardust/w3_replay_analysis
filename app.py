from flask import Flask, redirect, url_for, render_template_string
# Make sure csv_analysis_Dashboard.py has the create_dash_app function
from csv_analysis_Dashboard import create_dash_app
from csv_analysis_Dashboard_filters_v2 import create_filters_dash_app # Import the new function

# Initialize Flask server
server = Flask(__name__)

# Create the Dash application instances by calling the functions
# Pass the Flask server and a unique url_base_pathname to each
dash_app_summary = create_dash_app(server, url_base_pathname='/dash-summary/')
dash_app_filters = create_filters_dash_app(server, url_base_pathname='/dash-filters/')

# HTML template for the navigation page
NAV_HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>Warcraft III Replay Analysis Dashboards</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 0; padding: 0; background-color: #f4f4f4; color: #333; }
        .container { max-width: 800px; margin: 50px auto; padding: 20px; background-color: #fff; box-shadow: 0 0 10px rgba(0,0,0,0.1); }
        h1 { color: #333; text-align: center; }
        .tabs { list-style-type: none; padding: 0; margin: 20px 0; text-align: center; }
        .tabs li { display: inline; margin-right: 10px; }
        .tabs a {
            text-decoration: none;
            padding: 10px 20px;
            background-color: #5cb85c;
            color: white;
            border-radius: 5px;
            transition: background-color 0.3s;
        }
        .tabs a:hover {
            background-color: #4cae4c;
        }
        p { text-align: center; font-size: 1.1em; }
    </style>
</head>
<body>
    <div class="container">
        <h1>Warcraft 3 Replay Analysis Dashboard</h1>
        <p><em>Stats based on warcraft3.info replays 111727 - 117597</em></p>
        <p>Please select a dashboard to view:</p>
        <ul class="tabs">
            <li><a href="{{ url_for('dash_summary_entry') }}">Graphical Dashboards</a></li>
            <li><a href="{{ url_for('dash_filters_entry') }}">Advanced Filters Dashboard</a></li>
        </ul>
        <p><strong>Notes:</strong></p>
        <p>Winrate of "Graphical Dashboards" will always display as 100% and does not include the inverse in the graphics</p>
        <p>This is a private project. Please do not share the link. If you have any questions, please contact me using Discord -> dson_ch</p>
    </div>
</body>
</html>
"""

@server.route('/')
def index():
    # Render the navigation page
    # We use url_for to dynamically get the base path of each Dash app
    summary_url = dash_app_summary.config.url_base_pathname
    filters_url = dash_app_filters.config.url_base_pathname
    # For simplicity, directly linking. If using render_template_string with url_for, Flask needs to know the endpoint names.
    # We can create dummy redirect routes or just use the known paths.
    # Let's create redirect routes for cleanliness with url_for in template.
    return render_template_string(NAV_HTML)

# These routes are just to make url_for work cleanly in the template above.
# The actual Dash apps are served by their respective instances.
@server.route('/dash-summary/')
def dash_summary_entry():
    return redirect(dash_app_summary.config.url_base_pathname)

@server.route('/dash-filters/')
def dash_filters_entry():
    return redirect(dash_app_filters.config.url_base_pathname)

if __name__ == '__main__':
    # Run the Flask server
    # Set debug=False for production deployment
    # The host='0.0.0.0' makes it accessible on your network, not just localhost
    server.run(debug=True, host='0.0.0.0', port=8050) # Using port 8050 as default Dash port 