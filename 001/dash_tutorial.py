import dash
from dash import html
from dash import dcc
from dash.dependencies import Input, Output
import plotly.express as px
import dash_table

import pandas as pd

df = px.data.gapminder()


app = dash.Dash()

markdown_text="""
# Markdown sample
## Title 2
"""

year_options = []
for year in df['year'].unique():
    year_options.append({'label': str(year), 'value': year})

continent_options = []
for continent in df['continent'].unique():
    continent_options.append({'label': str(continent), 'value': continent})


app.layout = html.Div(
    children = [

        html.H1(children='Callback Sample1.'),
        dcc.Input(
            id='input_text_id',
            value='initial val',
            type='text',
        ),
        html.Div(id='output_div_id'),

        html.H1(children='Callback Sample2.'),
        dcc.Graph(
            id='graph',
            style=dict(width='60%'),
        ),
        dcc.Dropdown(
            id='select-year',
            options=year_options,
            value=df['year'].min(),
            style=dict(width='30%'),
        ),

        html.H3(children='select continent.'),
        dcc.Dropdown(
            id='select-continent',
            options=continent_options,
            value='Asia',
            style=dict(width='30%'),
        ),


        # 表の挿入
        html.H1(children='Callback Sample3.'),
        html.H2(children='Gapminder Data', style=dict(textAlign='center')),

        dash_table.DataTable(
            style_cell=dict(textAlign='center', width='300px'),
            fixed_rows=dict(headers=True),
            page_size=15,
            sort_action='native',
            filter_action='native',
            columns=[
                dict(name=col, id=col) for col in df.columns
            ],
            data=df.to_dict('records'),
            fill_width=False,
        ),

        # widget sample
        html.H1(children='Widget Sample.'),
        html.H2(children='Dropdown'),
        dcc.Dropdown(
            options=[
                {'label': 'N1', 'value':100},
                {'label': 'N2', 'value':200},
                {'label': 'N3', 'value':300},
            ]
        ),
        html.H2(children='Slider'),
        dcc.Slider(min=0, max=10, step=1),

        html.H2(children='Input text'),
        dcc.Textarea(
            placeholder='input text...',
            style=dict(width='50%')
        ),

        html.H2(children='Checklist'),
        dcc.Checklist(
            options=[
                {'label': 'N1', 'value':100},
                {'label': 'N2', 'value':200},
                {'label': 'N3', 'value':300},
            ],
            value=[100, 300]
        ),

        html.H2(children='Radio button'),
        dcc.RadioItems(
            options=[
                {'label': 'N1', 'value':100},
                {'label': 'N2', 'value':200},
                {'label': 'N3', 'value':300},
            ],
            value=300
        ),

        html.H1(children='Graph Sample.'),
        dcc.Graph(
            id='test_graph',
            figure=px.scatter(
                df,
                x='gdpPercap',
                y='lifeExp',
                log_x=True
            ),
        ),
        dcc.Markdown(children=markdown_text)
    ]
)


@app.callback(
    Output(component_id='output_div_id', component_property='children'),
    Input(component_id='input_text_id', component_property='value'),
)
def update_text(text):
    return f'入力された値は{text}です'

@app.callback(
    #Output(component_id='output_div_id', component_property='children'),
    #Input(component_id='input_text_id', component_property='value'),
    Output(component_id='graph', component_property='figure'),
    Input(component_id='select-year', component_property='value'),
    Input(component_id='select-continent', component_property='value'),
)
def update_dashborad(year, continent):
    selected_df = df[(df['year'] == year) & (df['continent'] == continent)]
    fig = px.scatter(
        selected_df,
        x='gdpPercap',
        y='lifeExp',
        log_x=True,
    )
    return fig



if __name__ == '__main__':
    app.run_server(debug=True)

