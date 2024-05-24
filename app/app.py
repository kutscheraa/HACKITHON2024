import json
import plotly.graph_objs as go
import dash
from dash import html, dcc
from dash.dependencies import Input, Output


from assets.fig_layout import my_figlayout, my_figlayout2
# Načtení souřadnic krajů z JSON souboru
with open("data/kraje.json", "r", encoding='utf-8') as f:
    kraje_geojson = json.load(f)

# Načtení souřadnic měst z JSON souboru
with open("souradnice_mest.json", "r") as json_file:
    souradnice_mest = json.load(json_file)

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
        fillcolor="rgba(0,0,0,0)",
        marker=dict(size=0),
        hoverinfo='none',
        name=feature['properties']['name'],
    ))

# Nastavení layoutu mapy
fig.update_layout(
    mapbox=dict(
        style="carto-positron",
        center=dict(lat=49.8175, lon=15.473),  # Střed mapy
        zoom=6,
    ),
    legend=dict(
        yanchor="top",
        y=0.99,
        xanchor="left",
        x=0.01
    )
)

fig.update_layout(my_figlayout2)
# Vytvoření aplikace Dash
app = dash.Dash(__name__)

# Přidání komponenty mapy do rozložení aplikace
app.layout = html.Div([
    html.H1('HACKITHON 2024'),
    dcc.Graph(figure=fig)
], className='row-content par')

# Spuštění serveru Dash
if __name__ == '__main__':
    app.run_server(debug=True)
