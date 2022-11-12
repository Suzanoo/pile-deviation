import dash
import dash_bootstrap_components as dbc
# import dash_defer_js_import as dji

from dash import html

app = dash.Dash(
    __name__,
    external_stylesheets=[dbc.themes.BOOTSTRAP],
    use_pages=True,
    suppress_callback_exceptions=True,
)

app.layout = html.Div([
	dash.page_container,
    # dji.Import(src="./assets/script.js"),
])

if __name__ == "__main__":
    app.run_server(debug=True)
