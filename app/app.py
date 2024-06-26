import json
import plotly.graph_objs as go
import plotly.express as px
import dash
from dash import html, dcc, dash_table
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
from assets.fig_layout import my_figlayout
from utils import create_dict, city_stats

URLS_PATH = 'data/mesta.csv'
THREADS = 16

# Načtení souřadnic krajů z JSON souboru
with open("data/kraje.json", "r", encoding='utf-8') as f:
    kraje_geojson = json.load(f)

# Načtení souřadnic měst z JSON souboru
with open("data/souradnice_mest.json", "r") as json_file:
    souradnice_mest = json.load(json_file)

cities = create_dict(URLS_PATH, THREADS)
df = city_stats(cities)

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
    hoverinfo='text',  # Zobrazovat pouze text při najetí na marker
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

fig.update_layout(my_figlayout)
fig.update_layout(showlegend=False)

# Vytvoření aplikace Dash
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP, dbc.icons.FONT_AWESOME],)

# Přidání komponenty mapy do rozložení aplikace
app.layout = html.Div([
    dcc.Graph(figure=fig, className='graph-container my-graph', id='map'),
    html.Div([
        dcc.Graph(id='bar-plot'),
        dcc.Graph(id='time-series-plot'),
        dcc.Graph(id='celkem-plot')  # New graph for 'celkem'
    ]),
    dbc.Modal([
        dbc.ModalHeader("Region Information", id="modal-header"),
        dbc.ModalBody([
            dcc.Input(id='search-input', type='text', placeholder='Search...', className='mb-2'),
            html.Div(id="modal-body")
        ]),
        dbc.ModalFooter(dbc.Button(html.Span("", style={"font-size": "0em"}), id="close-modal", className="close-modal-button bg-white border-0")),
    ], id="modal", is_open=False, fade=False, fullscreen=True),
])

@app.callback(
    Output('bar-plot', 'figure'),
    Output('time-series-plot', 'figure'),
    Output('celkem-plot', 'figure'),  # Output for the new graph
    Input('bar-plot', 'id')
)
def update_graphs(_):
    # Sorting DataFrame in descending order
    df_sorted_by_freq = df.sort_values(by='frekvence', ascending=False)
    df_sorted_by_celkem = df.sort_values(by='celkem', ascending=False)

    # Bar Plot
    bar_fig = px.bar(df_sorted_by_freq, x='mesto', y='frekvence', title="Průměrná měsíční frekvence záznamů", labels={'frekvence': 'Frekvence', 'mesto': 'Město'})
    bar_fig.update_layout(my_figlayout)
    # Time Series Plot
    time_series_fig = px.scatter(df, x='prvni', y='mesto', title="První záznam", labels={'prvni': 'První záznam', 'mesto': 'Město'})
    time_series_fig.update_layout(my_figlayout)
    # New Plot for 'celkem'
    celkem_fig = px.bar(df_sorted_by_celkem, x='mesto', y='celkem', title="Celkový počet záznamů", labels={'celkem': 'Celkem', 'mesto': 'Město'})
    celkem_fig.update_layout(my_figlayout)
    return bar_fig, time_series_fig, celkem_fig

@app.callback(
    Output("modal", "is_open"),
    [Input("map", "clickData"), Input("close-modal", "n_clicks")],
    [State("modal", "is_open")],
)
def toggle_modal(click_data, close_clicks, is_open):
    if close_clicks:
        return False
    if click_data:
        return not is_open
    return is_open

@app.callback(
    [Output("modal-header", "children"), Output("modal-body", "children")],
    [Input("map", "clickData"), Input("search-input", "value")]
)
def update_modal_content(click_data, search_value):
    if not click_data or "text" not in click_data["points"][0]:
        return "", ""
    region_name = click_data["points"][0]["text"]
    region_data = cities[region_name]

    # Filter dle inputu
    if search_value:
        region_data = region_data[region_data.apply(lambda row: search_value.lower() in str(row).lower(), axis=1)]

    # Link na PDF soubor
    region_data['pdf_link'] = region_data['pdf_link'].apply(lambda x: f'[Link]({x})' if x else '[Není k dispozici]')

    # Informace o kraji při rozkliknutí
    return html.P(f"{region_name}"), dash_table.DataTable(
        id='data-table',
        style_data={
            'whiteSpace': 'normal',
            'textAlign': 'left',
            'height': 'auto',
        },
        style_table={'overflowX': 'auto'},
        columns=[
            {"name": i, "id": i, "presentation": "markdown"} if i == 'pdf_link' else {"name": i, "id": i}
            for i in region_data.columns if i in ['název','datum_vyvěšení', 'dokument', 'pdf_link']
        ],
        data=region_data.to_dict('records')
    )

# Spuštění serveru Dash
if __name__ == '__main__':
    app.run_server(debug=False)
