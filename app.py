import dash
import dash_bootstrap_components as dbc

from dash import html, dcc

app = dash.Dash(
    __name__,
    external_stylesheets=[dbc.themes.BOOTSTRAP],
    use_pages=True,
    suppress_callback_exceptions=True,
)

app.layout = html.Div([
    dcc.Store(
        id='stored-data',
        storage_type='session',
     ),
	dash.page_container,
])

if __name__ == "__main__":
    app.run_server(debug=True)
