import dash
from dash import Dash
from dash import html, Input, Output, callback, dcc
import dash_bootstrap_components as dbc
import pandas as pd
import json
import plotly.graph_objs as go
import plotly.express as px

from assets.fig_layout import my_figlayout, my_linelayout, my_figlayout2

app = Dash(__name__, use_pages=False, external_stylesheets=[dbc.themes.BOOTSTRAP, dbc.icons.FONT_AWESOME],
           suppress_callback_exceptions=True, prevent_initial_callbacks=True)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'
server = app.server

# Load GeoJSON data from file
with open('data/kraje.json', 'r', encoding='utf-8') as f:
    geojson = json.load(f)

# Create a dataframe with all Czech regions and some dummy counts
df = pd.DataFrame({
    'region': [
        'Hlavní město Praha',
        'Středočeský kraj',
        'Jihočeský kraj',
        'Plzeňský kraj',
        'Karlovarský kraj',
        'Ústecký kraj',
        'Liberecký kraj',
        'Královéhradecký kraj',
        'Pardubický kraj',
        'Kraj Vysočina',
        'Jihomoravský kraj',
        'Olomoucký kraj',
        'Zlínský kraj',
        'Moravskoslezský kraj'
    ],
})

fig = px.choropleth_mapbox(df, 
                           geojson=geojson, 
                           locations='region', 
                           featureidkey="properties.name:cs", 
                           color='region',
                           labels={'count': 'Count'},
                           mapbox_style="carto-positron",
                           zoom=6.0, 
                           center={"lat": 49.7437522, "lon": 15.3386356},
                           )

# Update layout to include borders
fig.update_layout(my_figlayout2)
fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})
fig.update_traces(marker_line_width=1, marker_line_color='black')  # Add border color and width

map_component = dcc.Graph(
    id='geojson-map',
    figure=fig
)

# Add the map component to the app layout
app.layout = html.Div([
    html.H1('HACKITHON 2024'),
    map_component
], className='row-content')

############################################################################################
# Run App
if __name__ == '__main__':
    app.run_server(debug=True)
