import numpy as np
import pandas as pd
import dash_bootstrap_components as dbc
import dash
import plotly.express as px

from dash import html, dcc, callback, Input, Output, State, ALL

from tools.utils import create_df

dash.register_page(
    __name__,
    path='/',
    title='home', name='home'
    )

# -------------------------------
'''
Initial input:
- quantity of piles
- pile size
- footing dimension
- column size
'''
label_1 = ('Quantity of pile', 'Pile size, cm')
pile_id = ('pile-no', 'pile-size')

label_2 = ('Footing dimensions, cm', 'Column size, cm')
width_id = ('footing-width', 'column-width')
length_id = ('footing-length', 'column-depth')

definition = html.Div([
    html.Div([
        dbc.Row([
            dbc.Col([
                html.H5(label_1[i]),               
            ], width=3, className='mt-2'),
            dbc.Col([
                dbc.Input(id=pile_id[i], type='number')], width=3, className='mt-2')               
        ])for i in range(2)
    ]),
    html.Div([
        dbc.Row([
            dbc.Col([
                html.H5(label_2[i]),               
            ], width=3, className='mt-2'),
            dbc.Col([
                dbc.Input(id=width_id[i], type='number')], width=3, className='mt-2'), 
            dbc.Col([
                dbc.Input(id=length_id[i], type='number')], width=3, className='mt-2') 
        ])
        for i in range(2)
    ]),
    dbc.Button('Submit', id='button-1', n_clicks=0, className='btn1 mt-4'),
    html.Hr()
    # TODO button cannot click if all input not full-fill
])

layout = dbc.Container(id='content', children=[
    definition,
    html.Form(id='xy-vector', children=[]),
    dbc.Button('Submit', id='button-2', n_clicks=0, className='btn2 mt-4'),
    # dcc.Textarea(id='coor-text', value='Hello', style={'width': '50%', 'height': 300}),
])

# -------------------------------
'''
Construct input for coordinate:
- X-Y coordinate 
- error vector for each pile
'''
label3 = ('x', 'y', 'ex', 'ey')
@callback(
    Output('xy-vector', 'children'),
    Input('button-1', 'n_clicks'),
    State('pile-no', 'value'),
    prevent_initial_call=True,
)
def render_xy_input(n, n_pile):
    if n_pile != None:
        return html.Div([
            html.Div([
                dbc.Row([
                    dbc.Col(['Difine X-Y vector for each pile'], width=6),
                    dbc.Col(['Difine error vector for each pile'], width=6)
                ]),     
            ]),
            # html.Div([
            #     dbc.Row([
            #         dbc.Col([
            #             dbc.Input(
            #                 id=f'{label3[j]}-{i+1}',
            #                 type='number', className='mt-2',
            #                 placeholder=f'{label3[j]}-{i+1}'),                          
            #         ])for j in range(4)
            #     ])for i in range(n_pile)
            # ]),
            html.Div([
                dbc.Row([
                    dbc.Col([dbc.Input(type='number', id={'type':'x-coor', 'id':f'x-{i+1}'}, placeholder=f'x-{i+1}', className='mt-2')]),
                    dbc.Col([dbc.Input(type='number', id={'type':'y-coor', 'id':f'y-{i+1}'}, placeholder=f'y-{i+1}', className='mt-2')]),
                    dbc.Col([dbc.Input(type='number', id={'type':'x-err', 'id':f'ex-{i+1}'}, placeholder=f'ex-{i+1}', className='mt-2')]),
                    dbc.Col([dbc.Input(type='number', id={'type':'y-err', 'id':f'ey-{i+1}'}, placeholder=f'ey-{i+1}', className='mt-2')]),
                ])for i in range(n_pile)
            ]),
            # dbc.Button('Submit', id='button-2', n_clicks=0, className='btn2 mt-4'),
            # dcc.Textarea(id='coor-text', value='Hello', style={'width': '50%', 'height': 300}),
            dcc.Graph(id='graph', className='pb-4', figure={}),
            html.Hr()
    ])
    # TODO button cannot click if all input not full-fill

# -------------------------------
# get X-Y coordinate
@callback(
    Output('graph', 'figure'),

    Input('button-2', 'n_clicks'),
    State({'type':'x-coor', 'id':ALL}, 'value'),
    State({'type':'y-coor', 'id':ALL}, 'value'),
    State({'type':'x-err', 'id':ALL}, 'value'),
    State({'type':'y-err', 'id':ALL}, 'value'),
    State('footing-width', 'value'),
    State('footing-length', 'value'),
    State('column-width', 'value'),
    State('column-depth', 'value'),
    State('pile-size', 'value'),
    prevent_initial_call=True
)
def coor_text(n, x, y, ex, ey, B, L, w, d, p):
    if n > 0:
        X = np.array(x)
        Y = np.array(y)
        ex = np.array(ex)
        ey = np.array(ey)

        # coordinate of column and footing
        column_x = np.array([w/2, -w/2, -w/2, w/2, w/2]) #[x1, x2, x3, ..., x1] x-coordinate, m
        column_y = np.array([d/2, d/2, -d/2, -d/2, d/2]) #[y1, y2, y3, ..., y1] y-coordinate, m
        footing_x = np.array([B/2, -B/2, -B/2, B/2, B/2]) 
        footing_y = np.array([L/2, L/2, -L/2, -L/2, L/2]) 
        
        # coordinate of local pile section
        px_vector = np.array([p/2, -p/2, -p/2, p/2, p/2]) #[p1, p2, p3, ..., p1] local x-coordinate, m
        py_vector = np.array([p/2, p/2, -p/2, -p/2, p/2])#[r1, r2, r3, ..., r1] local y-coordinate, m

        X_new = X + ex
        Y_new = Y + ey

        rx = X_new.sum()
        ry = Y_new.sum()
        unit_vector = np.array([rx, ry])
        unit_vector = unit_vector.T
        unit_vector = pd.DataFrame({
            'x' : [0, unit_vector[0]],
            'y' : [0, unit_vector[1]]
        })
        R = np.linalg.norm(unit_vector)

        # coordinate of all piles and create df for plot
        piles = create_df(X, Y, px_vector, py_vector)
        piles_err = create_df(X_new, Y_new, px_vector, py_vector)

        footing = pd.DataFrame({
            'x' : footing_x,
            'y' : footing_y
        })

        column = pd.DataFrame({
            'x' : column_x,
            'y' : column_y
        })

    # plot
        # multi fig
        # https://stackoverflow.com/questions/69096931/how-do-i-combine-two-plots-into-one-figure-using-plotly
        import plotly.graph_objects as go
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=footing['x'], y=footing['y'],
            mode='lines+markers'))

        fig.add_trace(go.Scatter(
            x=column['x'], y=column['y'],
             mode='lines+markers'))

        fig.add_trace(go.Scatter(
            x=piles['x'], y=piles['y'],
            mode='lines+markers',
            line=dict(color='#31fc03', width=2 )))

        fig.add_trace(go.Scatter(
            x=piles_err['x'], y=piles_err['y'],
            mode='lines+markers',
            line=dict(color='firebrick', width=2, dash='dash')))

        fig.add_trace(go.Scatter(
            x=unit_vector['x'], y=unit_vector['y'],
            mode='markers', marker_symbol='cross'))

        return fig
