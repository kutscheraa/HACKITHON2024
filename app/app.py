import json
import plotly.graph_objs as go
import dash
from dash import html, dcc
import dash_bootstrap_components as dbc

from assets.fig_layout import my_figlayout, my_figlayout2
# Načtení souřadnic krajů z JSON souboru
with open("data/kraje.json", "r", encoding='utf-8') as f:
    kraje_geojson = json.load(f)

# Načtení souřadnic měst z JSON souboru
with open("souradnice_mest.json", "r") as json_file:
    souradnice_mest = json.load(json_file)

# Extracting bounds from the provided GeoJSON
geojson_bounds = {
    "west": 12.0905752,
    "east": 18.8592531,
    "south": 48.5518081,
    "north": 51.0556945
}

# Seznam souřadnic pro plotly
lats = [data["lat"] for data in souradnice_mest.values()]
lons = [data["lon"] for data in souradnice_mest.values()]
mesta = list(souradnice_mest.keys())

# Vytvoření mapy pomocí Plotly
fig = go.Figure()

# Přidání bodů měst na mapu
fig.add_trace(go.Scattermapbox(
    lat=lats,
    lon=lons,
    mode='markers',
    marker=dict(size=10, color='red'),
    text=mesta,  # Jméno města při najetí na tečku
    hoverinfo='text',  # Zobrazovat pouze text při najetí na tečku
    name='Města',
))

# Přidání hranic krajů
for feature in kraje_geojson['features']:
    geo_lat = []
    geo_lon = []
    for lon, lat in feature['geometry']['coordinates'][0]:
        geo_lon.append(lon)
        geo_lat.append(lat)
    fig.add_trace(go.Scattermapbox(
        lat=geo_lat,
        lon=geo_lon,
        mode="lines",
        line=dict(width=1),
        fill="toself",
        fillcolor="rgba(0,0,0,0)",  # Fully transparent for other regions
        marker=dict(size=0),
        hoverinfo='none',
        name=feature['properties']['name'],
    ))

# Nastavení layoutu mapy
fig.update_layout(
    mapbox=dict(
        style="carto-positron",
        center=dict(lat=49.7439047, lon=15.3381061),  # Střed mapy
        zoom=6.5,  # Adjust zoom level as necessary
    ),
    margin={"r":0,"t":0,"l":0,"b":0},
)

fig.update_layout(my_figlayout2)
# Vytvoření aplikace Dash
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP, dbc.icons.FONT_AWESOME],)

# Přidání komponenty mapy do rozložení aplikace
app.layout = html.Div([
    html.H1('HACKITHON 2024'),
    dcc.Graph(figure=fig, className='graph-container')
], className='row-content par')

# Spuštění serveru Dash
if __name__ == '__main__':
    app.run_server(debug=True)