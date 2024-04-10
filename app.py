import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.graph_objects as go
import pandas as pd
import xbrl_functions

#load data
report_ids = [
    '677268',
    '677267'
]

df = pd.read_csv('xbrl_data.csv')
df['fact.value'] = pd.to_numeric(df['fact.value'], errors='coerce')
df = df[df['fact.value'].notna()]

final_ratios = pd.DataFrame(columns= ['report_id', 'report_entity_name', 'ratio', 'value', 'green_start', 'green_end', 'yellow_start', 'yellow_end', 'red_start', 'red_end', 'var_1_name', 'var_1_value', 'var_2_name', 'var_2_value'])

for report_id in report_ids:
    final_ratios = pd.concat([final_ratios, pd.DataFrame([xbrl_functions.get_short_run(df, report_id)], columns=final_ratios.columns)], ignore_index=True)
    final_ratios = pd.concat([final_ratios, pd.DataFrame([xbrl_functions.get_days_cash_on_hand(df, report_id)], columns=final_ratios.columns)], ignore_index=True)
    final_ratios = pd.concat([final_ratios, pd.DataFrame([xbrl_functions.get_liquidity(df, report_id)], columns=final_ratios.columns)], ignore_index=True)
    final_ratios = pd.concat([final_ratios, pd.DataFrame([xbrl_functions.get_gov_debt_coverage(df, report_id)], columns=final_ratios.columns)], ignore_index=True)
    final_ratios = pd.concat([final_ratios, pd.DataFrame([xbrl_functions.get_expenditure_per_capita(df, report_id)], columns=final_ratios.columns)], ignore_index=True)
    final_ratios = pd.concat([final_ratios, pd.DataFrame([xbrl_functions.get_net_asset_growth(df, report_id)], columns=final_ratios.columns)], ignore_index=True)
    final_ratios = pd.concat([final_ratios, pd.DataFrame([xbrl_functions.get_captial_asset_ga(df, report_id)], columns=final_ratios.columns)], ignore_index=True)
    final_ratios = pd.concat([final_ratios, pd.DataFrame([xbrl_functions.get_captial_asset_bta(df, report_id)], columns=final_ratios.columns)], ignore_index=True)
print(final_ratios)


# Define the Dash app
app = dash.Dash(__name__)
# Define the layout of your dashboard
app.layout = html.Div([
    html.H1("Government Financial Ratios", style={'textAlign': 'center'}),
    dcc.Dropdown(
        [value for value in final_ratios['report_entity_name'].unique()],
        'County of Ogemaw',
        id='report-dropdown',
        clearable=False,
        style={'width': '50%', 'margin': 'auto', 'textAlign': 'center'}
    ),
    
    html.Div([    
        html.Div(children=[
            dcc.Graph(id='gauge-plot1', mathjax=True),
            dcc.Markdown(id='gauge-plot1-text', mathjax=True),
            html.Br(),
            dcc.Graph(id='gauge-plot2', mathjax=True),
            dcc.Markdown(id='gauge-plot2-text', mathjax=True),
            html.Br(),
            dcc.Graph(id='gauge-plot3', mathjax=True),
            dcc.Markdown(id='gauge-plot3-text', mathjax=True),
            html.Br(),
            dcc.Graph(id='gauge-plot4', mathjax=True),
            dcc.Markdown(id='gauge-plot4-text', mathjax=True),
        ], style={'padding': 10, 'flex': 1}),

        html.Div(children=[
            dcc.Graph(id='gauge-plot5', mathjax=True),
            dcc.Markdown(id='gauge-plot5-text', mathjax=True),
            html.Br(),
            dcc.Graph(id='gauge-plot6', mathjax=True),
            dcc.Markdown(id='gauge-plot6-text', mathjax=True),
            html.Br(),
            dcc.Graph(id='gauge-plot7', mathjax=True),
            dcc.Markdown(id='gauge-plot7-text', mathjax=True),
            html.Br(),
            dcc.Graph(id='gauge-plot8', mathjax=True),
            dcc.Markdown(id='gauge-plot8-text', mathjax=True),
        ], style={'padding': 10, 'flex': 1})
    ], style={'display': 'flex', 'flexDirection': 'row'})
])

def create_gauge(value, ratio):
    
    # change color: Distance to Target
    data = final_ratios[final_ratios['report_entity_name'] == value].iloc[ratio]
    value = data['value']
    green1 = data['green_start']
    green2 = data['green_end']
    red1 = data['red_start']
    red2 = data['red_end']
    font_color = 'black'
    if (value <= green2) & (value >= green1):
        distance_metric_color = 'lavender'
        font_color = 'blue'
        ref = value
    elif (value < red2) & (value > red1):
        distance_metric_color = 'crimson'
        if(abs(value - green1) < abs(value - green2)):
            ref = green1
        else:
            ref = green2
    else:
        distance_metric_color = 'gold'
        if(abs(value - green1) < abs(value - green2)):
            ref = green1    
        else:
            ref = green2

    fig = go.Figure(go.Indicator(mode="gauge+number+delta",
        value=round(data['value'],3),
        domain={'x': [0, 1], 'y': [0, 1]},
        title={'text': data['ratio'], 'font': {'size': 30}},
        delta={'reference': ref, 'increasing': {'color': distance_metric_color}, 'decreasing': {'color': distance_metric_color}, 'font': {'size': 30}}, # distance metric
        gauge={
            'axis': {'range': [None, max([data['green_end'], data['yellow_end'], data['red_end']])], 'tickwidth': 1, 'tickcolor': "darkblue"},
            'bar': {'color': "black"},
            'bgcolor': "white",
            'borderwidth': 2,
            'bordercolor': "gray",
            'steps': [
                {'range': [data['red_start'], data['red_end']], 'color': 'crimson'},  # red
                {'range': [data['green_start'], data['green_end']], 'color': 'mediumseagreen'},  # green
                {'range': [data['yellow_start'], data['yellow_end']], 'color': 'gold'}], # yellow
            'threshold': {
                'line': {'color': "black", 'width': 4},
                'thickness': 0.75,
                'value': round(data['value'],3)}}))

    fig.update_layout(paper_bgcolor="lavender", font={'color': font_color, 'family': "Arial"})

    return fig

def update_markdown(value, ratio):
    data = final_ratios[final_ratios['report_entity_name'] == value].iloc[ratio]
    return r"""$\text{{Formula}} = \frac{{\text{{ {} }}}}{{\text{{ {} }}}} = \frac{{\text{{ {} }}}}{{\text{{ {} }}}}$""".format(data['var_1_name'], data['var_2_name'], round(data['var_1_value'], 2), round(data['var_2_value'], 2))

@app.callback(
    Output('gauge-plot1', 'figure'),
    [Input('report-dropdown', 'value')]
)
def update_gauge_plot1(value):
    return create_gauge(value, 0)

@app.callback(
    Output('gauge-plot2', 'figure'),
    [Input('report-dropdown', 'value')]
)
def update_gauge_plot2(value):
    return create_gauge(value, 1)

@app.callback(
    Output('gauge-plot3', 'figure'),
    [Input('report-dropdown', 'value')]
)
def update_gauge_plot3(value):
    return create_gauge(value, 2)

@app.callback(
    Output('gauge-plot4', 'figure'),
    [Input('report-dropdown', 'value')]
)
def update_gauge_plot4(value):
    return create_gauge(value, 3)

@app.callback(
    Output('gauge-plot5', 'figure'),
    [Input('report-dropdown', 'value')]
)
def update_gauge_plot5(value):
    return create_gauge(value, 4)

@app.callback(
    Output('gauge-plot6', 'figure'),
    [Input('report-dropdown', 'value')]
)
def update_gauge_plot6(value):
    return create_gauge(value, 5)

@app.callback(
    Output('gauge-plot7', 'figure'),
    [Input('report-dropdown', 'value')]
)
def update_gauge_plot7(value):
    return create_gauge(value, 6)

@app.callback(
    Output('gauge-plot8', 'figure'),
    [Input('report-dropdown', 'value')]
)
def update_gauge_plot8(value):
    return create_gauge(value, 7)

@app.callback(
    Output('gauge-plot1-text', 'children'),
    [Input('report-dropdown', 'value')]
)
def update_gauge_plot1_text(value):
    return update_markdown(value, 0)

@app.callback(
    Output('gauge-plot2-text', 'children'),
    [Input('report-dropdown', 'value')]
)
def update_gauge_plot2_text(value):
    return update_markdown(value, 1)

@app.callback(
    Output('gauge-plot3-text', 'children'),
    [Input('report-dropdown', 'value')]
)
def update_gauge_plot3_text(value):
    return update_markdown(value, 2)

@app.callback(
    Output('gauge-plot4-text', 'children'),
    [Input('report-dropdown', 'value')]
)
def update_gauge_plot4_text(value):
    return update_markdown(value, 3)

@app.callback(
    Output('gauge-plot5-text', 'children'),
    [Input('report-dropdown', 'value')]
)
def update_gauge_plot5_text(value):
    return update_markdown(value, 4)

@app.callback(
    Output('gauge-plot6-text', 'children'),
    [Input('report-dropdown', 'value')]
)
def update_gauge_plot6_text(value):
    return update_markdown(value, 5)

@app.callback(
    Output('gauge-plot7-text', 'children'),
    [Input('report-dropdown', 'value')]
)
def update_gauge_plot7_text(value):
    return update_markdown(value, 6)

@app.callback(
    Output('gauge-plot8-text', 'children'),
    [Input('report-dropdown', 'value')]
)
def update_gauge_plot8_text(value):
    return update_markdown(value, 7)
    

# Run the app
if __name__ == '__main__':
    app.run_server(debug=False, host='0.0.0.0', port = 8080)