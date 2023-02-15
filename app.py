# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.
import logging

from dash import Dash, html, dcc, Input, Output, callback, State
import pandas as pd
import dash_bootstrap_components as dbc

from helpers.table_creation import generate_tables

df = pd.read_csv('agent-compatibility.csv')
df = df[df['CLUSTER_TYPE'].notna()]

app = Dash(external_stylesheets=[dbc.themes.ZEPHYR])

agent_version_dropdown = html.Div(
    ["Agent Version: ", agent_version := dcc.Dropdown(
        df.AGENT_VERSION.unique(),
        id='agent-version',
        value='12.10.0-rc2'
    )],
    style={"width": "15%"},
)

grouping_dropdown = html.Div(
    ["Group By: ", grouping := dcc.Dropdown(
        df.columns,
        id='grouping',
        value='CLUSTER_TYPE'
    )],
)

arch_dropdown = html.Div(
    ["Architecture is: ", arch_compatibility := dcc.Dropdown(
        df.ARCHITECTURE.unique(),
        id='arch-comp',
    )],
)

grouping_selection = dbc.Card(
    [grouping_dropdown],
    style={"width": "25%"},
)

customer_inputs = dbc.Card(
    [
     arch_dropdown,
     ])

app.layout = html.Div([
    dbc.Container([
        dbc.Row(agent_version_dropdown, justify='end'),
        html.Br(),
        dbc.Row(grouping_selection, justify='end'),
        html.Button(id='update-button-state', n_clicks=0, children='Update'),
        dbc.Row([dbc.Col(customer_inputs),
                 dbc.Col(table_ouput := html.Div(), width=8)])], fluid=True)
])


@callback(
    Output(table_ouput, component_property='children'),
    Input('update-button-state', 'n_clicks'),
    State(agent_version, component_property='value'),
    State(grouping, component_property='value'),
    State(arch_compatibility, component_property='value')
)
def update_output_div(n_clicks, agent_version, grouping, arch_compatibility):
    if n_clicks:
        logging.error(f'On click {n_clicks} customer investigated {arch_compatibility} with agent {agent_version} and grouped this info by {grouping}')
    return generate_tables(df, agent_version, grouping, arch_compatibility)


if __name__ == '__main__':
    app.run_server(debug=True)
