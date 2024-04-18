import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.graph_objects as go
import pandas as pd
import xbrl_functions
import warnings

# Silence all warnings
warnings.filterwarnings("ignore")

# Load data
df = pd.read_csv('xbrl_data.csv')
report_ids = df['report.id'].unique().tolist()

# Create the `final_ratios` DataFrame
final_ratios = pd.DataFrame(columns= ['report_id', 'report_entity_name', 'ratio', 'value', 'green_start', 'green_end', 'yellow_start', 'yellow_end', 'red_start', 'red_end', 'var_1_name', 'var_1_value', 'var_2_name', 'var_2_value'])

# Add the ratios to the `final_ratios` DataFrame
for report_id in report_ids:
    final_ratios = pd.concat([final_ratios, pd.DataFrame([xbrl_functions.get_short_run(df, report_id)], columns=final_ratios.columns)], ignore_index=True) # gauge-plot1
    final_ratios = pd.concat([final_ratios, pd.DataFrame([xbrl_functions.get_days_cash_on_hand(df, report_id)], columns=final_ratios.columns)], ignore_index=True) # gauge-plot2
    final_ratios = pd.concat([final_ratios, pd.DataFrame([xbrl_functions.get_liquidity(df, report_id)], columns=final_ratios.columns)], ignore_index=True) # gauge-plot3
    final_ratios = pd.concat([final_ratios, pd.DataFrame([xbrl_functions.get_gov_debt_coverage(df, report_id)], columns=final_ratios.columns)], ignore_index=True) # gauge-plot4
    final_ratios = pd.concat([final_ratios, pd.DataFrame([xbrl_functions.get_expenditure_per_capita(df, report_id)], columns=final_ratios.columns)], ignore_index=True) # gauge-plot5
    final_ratios = pd.concat([final_ratios, pd.DataFrame([xbrl_functions.get_net_asset_growth(df, report_id)], columns=final_ratios.columns)], ignore_index=True) # gauge-plot6
    final_ratios = pd.concat([final_ratios, pd.DataFrame([xbrl_functions.get_captial_asset_ga(df, report_id)], columns=final_ratios.columns)], ignore_index=True) # gauge-plot7
    final_ratios = pd.concat([final_ratios, pd.DataFrame([xbrl_functions.get_captial_asset_bta(df, report_id)], columns=final_ratios.columns)], ignore_index=True) # gauge-plot8
    final_ratios = pd.concat([final_ratios, pd.DataFrame([xbrl_functions.get_own_source_rev(df, report_id)], columns=final_ratios.columns)], ignore_index=True) # gauge-plot9
    
    # # # NOTE: UNCOMMENT TO ADD ADDITIONAL RATIOS TO THE DATAFRAME
    # final_ratios = pd.concat([final_ratios, pd.DataFrame([xbrl_functions.INSERT_FUNCTION_NAME(df, report_id)], columns=final_ratios.columns)], ignore_index=True) # gauge-plot10

# print(final_ratios)


# Define the Dash app
app = dash.Dash(__name__)

# Defines the layout of the dashboard:
formula_size = 30
app.layout = html.Div([
    html.Meta(name="viewport", content="width=device-width, initial-scale=0.75"),
    html.H1("Government Financial Ratios", style={'textAlign': 'center'}),
    dcc.Dropdown(
        options=[{'label': value, 'value': value} for value in final_ratios['report_entity_name'].unique()],
        value='County of Ogemaw',
        id='report-dropdown',
        clearable=False,
        style={'width': '50%', 'margin': 'auto', 'textAlign': 'center'}
    ), # dropdown menu
    
    html.Br(),
    html.Br(),
    html.Br(),

    html.Div([    
        html.Div(style={'flex': 0.25}),  # empty div for spacing on the left

        html.Div(children=[
            html.Div(children=[
            dcc.Graph(id='gauge-plot1', mathjax=True),
            dcc.Markdown(id='gauge-plot1-text', mathjax=True, style={'fontSize': formula_size, 'textAlign': 'center'}),
            ], style={'border': '3px solid black', 'padding': '20px', 'background-color': 'lavender'}),
            
            html.Br(),
            html.Br(),
            html.Br(),
            
            html.Div(children=[
            dcc.Graph(id='gauge-plot2', mathjax=True),
            dcc.Markdown(id='gauge-plot2-text', mathjax=True, style={'fontSize': formula_size, 'textAlign': 'center'}),
            ], style={'border': '3px solid black', 'padding': '20px', 'background-color': 'lavender'}),
            
            html.Br(),
            html.Br(),
            html.Br(),
            
            html.Div(children=[
            dcc.Graph(id='gauge-plot3', mathjax=True),
            dcc.Markdown(id='gauge-plot3-text', mathjax=True, style={'fontSize': formula_size, 'textAlign': 'center'}),
            ], style={'border': '3px solid black', 'padding': '20px', 'background-color': 'lavender'}),
            
            html.Br(),
            html.Br(),
            html.Br(),

            html.Div(children=[
            dcc.Graph(id='gauge-plot4', mathjax=True),
            dcc.Markdown(id='gauge-plot4-text', mathjax=True, style={'fontSize': formula_size, 'textAlign': 'center'}),
            ], style={'border': '3px solid black', 'padding': '20px', 'background-color': 'lavender'}),
            
            html.Br(),
            html.Br(),
            html.Br(),

            html.Div(children=[
            dcc.Graph(id='gauge-plot9', mathjax=True),
            dcc.Markdown(id='gauge-plot9-text', mathjax=True, style={'fontSize': formula_size, 'textAlign': 'center'}),
            ], style={'border': '3px solid black', 'padding': '20px', 'background-color': 'lavender'}),

            # # # NOTE: UNCOMMENT TO DISPLAY ADDITIONAL GAUGE PLOTS ON THE DASHBOARD (1ST COLUMN)
            # html.Br(),
            # html.Br(),
            # html.Br(),

            # html.Div(children=[
            # dcc.Graph(id='gauge-plot**', mathjax=True), # change `**` to the respective gauge plot number in the `final_ratios` DataFrame
            # dcc.Markdown(id='gauge-plot**-text', mathjax=True, style={'fontSize': formula_size, 'textAlign': 'center'}), # change `**` to the respective gauge plot number in the `final_ratios` DataFrame
            # ], style={'border': '3px solid black', 'padding': '20px', 'background-color': 'lavender'}),

        ], style={'padding': 10, 'flex': 0.5, 'textAlign': 'center'}), # 1st column of gauges & formulas

        html.Div(style={'flex': 0.25}),  # narrow column of space between the two divs

        html.Div(children=[
            html.Div(children=[
            dcc.Graph(id='gauge-plot5', mathjax=True),
            dcc.Markdown(id='gauge-plot5-text', mathjax=True, style={'fontSize': formula_size, 'textAlign': 'center'}),
            ], style={'border': '3px solid black', 'padding': '20px', 'background-color': 'lavender'}),
            
            html.Br(),
            html.Br(),
            html.Br(),
            
            html.Div(children=[
            dcc.Graph(id='gauge-plot6', mathjax=True),
            dcc.Markdown(id='gauge-plot6-text', mathjax=True, style={'fontSize': formula_size, 'textAlign': 'center'}),
            ], style={'border': '3px solid black', 'padding': '20px', 'background-color': 'lavender'}),
            
            html.Br(),
            html.Br(),
            html.Br(),
            
            html.Div(children=[
            dcc.Graph(id='gauge-plot7', mathjax=True),
            dcc.Markdown(id='gauge-plot7-text', mathjax=True, style={'fontSize': formula_size, 'textAlign': 'center'}),
            ], style={'border': '3px solid black', 'padding': '20px', 'background-color': 'lavender'}),
            
            html.Br(),
            html.Br(),
            html.Br(),
            
            html.Div(children=[
            dcc.Graph(id='gauge-plot8', mathjax=True),
            dcc.Markdown(id='gauge-plot8-text', mathjax=True, style={'fontSize': formula_size, 'textAlign': 'center'}),
            ], style={'border': '3px solid black', 'padding': '20px', 'background-color': 'lavender'}),
            
            # # # NOTE: UNCOMMENT TO DISPLAY ADDITIONAL GAUGE PLOTS ON THE DASHBOARD (2ND COLUMN)
            # html.Br(),
            # html.Br(),
            # html.Br(),

            # html.Div(children=[
            # dcc.Graph(id='gauge-plot**', mathjax=True), # change `**` to the respective gauge plot number in the `final_ratios` DataFrame
            # dcc.Markdown(id='gauge-plot**-text', mathjax=True, style={'fontSize': formula_size, 'textAlign': 'center'}), # change `**` to the respective gauge plot number in the `final_ratios` DataFrame
            # ], style={'border': '3px solid black', 'padding': '20px', 'background-color': 'lavender'}),
            
        ], style={'padding': 10, 'flex': 1}), # 2nd column of gauges & formulas

        html.Div(style={'flex': 0.25})  # empty div for spacing on the right
    ], style={'display': 'flex', 'flexDirection': 'row'})
]) # end of layout


# This function creates a gauge plot for a given entity name and ratio index. It returns the gauge plot.
def create_gauge(value, ratio):
    
    # Determines referenece value to calculate `Distance to Target` metric
    # Automates color change for `Distance to Target` metric, based on target ranges
    data = final_ratios[final_ratios['report_entity_name'] == value].iloc[ratio]
    ratio_value = data['value']
    green1 = data['green_start']
    green2 = data['green_end']
    red1 = data['red_start']
    red2 = data['red_end']
    font_color = 'black'
    if (ratio_value <= green2) & (ratio_value >= green1): # green target range
        distance_metric_color = 'lavender' # hides `Distance to Target` metric
        font_color = 'darkgreen' # changes overall font color
        ref = ratio_value
    elif (ratio_value <= red2) & (ratio_value >= red1): # red range
        distance_metric_color = 'crimson'
        if(abs(ratio_value - green1) < abs(ratio_value - green2)):
            ref = green1
        else:
            ref = green2
    else: # yellow/orange range
        distance_metric_color = 'darkorange'
        if(abs(ratio_value - green1) < abs(ratio_value - green2)):
            ref = green1    
        else:
            ref = green2

    # Create the gauge plot
    fig = go.Figure(go.Indicator(mode="gauge+number+delta",
        value=round(data['value'],3), # Ratio value
        domain={'x': [0, 1], 'y': [0, 1]},
        title={'text': data['ratio'], 'font': {'size': 26, 'color': font_color, 'family': 'Courier'}}, # graph title
        delta={'reference': ref, 'increasing': {'color': distance_metric_color}, 'decreasing': {'color': distance_metric_color}, 'font': {'size': 30}, 'position': "bottom"}, # `Distance to Target` metric
        gauge={
            'axis': {'range': [None, max([data['green_end'], data['yellow_end'], data['red_end']])], 'tickwidth': 1, 'tickcolor': "black"}, # sets axis range
            'bar': {'color': "black"},
            'bgcolor': "white",
            'borderwidth': 2,
            'bordercolor': "gray",
            'steps': [
                {'range': [data['red_start'], data['red_end']], 'color': 'crimson'},  # red range
                {'range': [data['green_start'], data['green_end']], 'color': 'mediumseagreen'},  # green target range
                {'range': [data['yellow_start'], data['yellow_end']], 'color': 'gold'}], # yellow/orange range
            'threshold': {
                'line': {'color': "black", 'width': 4},
                'thickness': 0.75,
                'value': data['value'] # tick marked on the gauge plot
            }
        }
    ))


    fig.update_layout(paper_bgcolor="lavender", font={'color': font_color, 'family': 'Courier New', 'size': 18}) # overall background color, font color + style

    return fig
# end of create_gauge

# This function updates the markdown text for each gauge plot. It takes in the selected entity name and ratio index.
# It returns a string in LaTeX format that represents the formula for the ratio.
def update_markdown(value, ratio):
    data = final_ratios[final_ratios['report_entity_name'] == value].iloc[ratio]
    return r"""$\text{{Formula}} = \frac{{\text{{ {} }}}}{{\text{{ {} }}}} = \frac{{\text{{ {} }}}}{{\text{{ {} }}}}$""".format(data['var_1_name'], data['var_2_name'], round(data['var_1_value'], 2), round(data['var_2_value'], 2))

# Define the callback functions to update the gauge plots based on the selected entity name
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
    Output('gauge-plot9', 'figure'),
    [Input('report-dropdown', 'value')]
)
def update_gauge_plot9(value):
    return create_gauge(value, 8)

# Define the callback functions to update the markdown text (formula) for each gauge plot based on the selected entity name
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

@app.callback(
    Output('gauge-plot9-text', 'children'),
    [Input('report-dropdown', 'value')]
)
def update_gauge_plot9_text(value):
    return update_markdown(value, 8)

# # # NOTE: UNCOMMENT TO ADD CALLBACKS FOR ADDITIONAL GAUGE PLOTS
# @app.callback(
#     Output('gauge-plot**', 'figure'), # change `**` to the respective gauge plot number in the `final_ratios` DataFrame
#     [Input('report-dropdown', 'value')]
# )

# def update_gauge_plot**(value): # change `**` to the respective gauge plot number in the `final_ratios` DataFrame
#     return create_gauge(value, **) # change `**` to the respective gauge plot number in the `final_ratios` DataFrame
    
# @app.callback(
#     Output('gauge-plot**-text', 'children'), # change `**` to the respective gauge plot number in the `final_ratios` DataFrame
#     [Input('report-dropdown', 'value')]
# )

# def update_gauge_plot**_text(value): # change `**` to the respective gauge plot number in the `final_ratios` DataFrame
#     return update_markdown(value, **) # change `**` to the respective gauge plot number in the `final_ratios` DataFrame

# Run the dash app
if __name__ == '__main__':
    app.run_server(debug=False, host='0.0.0.0', port = 8080)
