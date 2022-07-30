# Import required libraries
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import dash
from dash import html
from dash import dcc
from dash.dependencies import Input, Output

# Read the airline data into pandas dataframe
spacex_df = pd.read_csv('https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBM-DS0321EN-SkillsNetwork/datasets/spacex_launch_dash.csv')
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

# Create a dash application
app = dash.Dash(__name__)
                               
app.layout = html.Div(children=[
    #TITLE
    html.H1(
            'SpaceX Launch Records Dashboard', 
            style = {'textAlign': 'center', 'color': '#503D36', 'font-size': 40}
            ),
    #DROPDOWN CREATION
    dcc.Dropdown(
        id = 'site-dropdown', 
        options = [{'label': 'All Sites', 'value': 'ALL'},
                    {'label': 'CCAFS LC-40', 'value': 'CCAFS LC-40'},
                    {'label': 'VAFB SLC-4E', 'value': 'VAFB SLC-4E'},
                    {'label': 'KSC LC-39A', 'value': 'KSC LC-39A'},
                    {'label': 'CCAFS SLC-40', 'value': 'CCAFS SLC-40'}],
        value = 'ALL',
        placeholder = 'Select a launch site...',
        searchable = True,
        style = {'width':'80%', 'padding':'3px', 'font-size':'20px', 'textAlign':'left'}
        ),
    html.Br(),
    html.Br(),
    #PIE CHART
    html.Div(dcc.Graph(id='success-pie-chart')),

    #PAYLOAD SLIDER
    html.P("Payload range (Kg):"),
    dcc.RangeSlider(id='payload-slider',
                    min=0,
                    max=10000,
                    step=1000,
                    value=[min_payload, max_payload] #declared eariler
                    ),

    #SCATTER PLOT
    html.Div(dcc.Graph(id='success-payload-scatter-chart'))
])

#CALLBACK FOR PIE CHART (INPUT: DROPDOWN LIST, OUTPUT: PIE CHART)
@app.callback(Output(component_id='success-pie-chart', component_property='figure'),
              Input(component_id='site-dropdown', component_property='value'))

# Add computation to callback function and return graph
def get_pie_chart(entered_site):
    filtered_df = spacex_df
    if entered_site == 'ALL':
        fig = px.pie(filtered_df, values='class', 
        names='Launch Site', 
        title='Success Count for all launch sites')
        return fig
    else:
        # return the outcomes piechart for a selected site
        filtered_df = spacex_df[spacex_df['Launch Site']== entered_site]
        filtered_df = filtered_df.groupby(['Launch Site','class']).size().reset_index(name='class count')
        fig = px.pie(filtered_df,values='class count',names='class',title=f"Total Successful Launches: {entered_site}")
        return fig

#CALLBACK FOR PAYLOAD SLIDER (INPUT: DROPDOWN LIST & SLIDER, OUTPUT: SCATTERPLOT)
@app.callback(Output(component_id='success-payload-scatter-chart',component_property='figure'),
                [Input(component_id='site-dropdown',component_property='value'),
                Input(component_id='payload-slider',component_property='value')])

def get_scatter(entered_site, payload):
    filtered_df = spacex_df[spacex_df['Payload Mass (kg)'].between(payload[0],payload[1])]
    
    if entered_site=='ALL':
        fig=px.scatter(filtered_df, x='Payload Mass (kg)', y='class', color='Booster Version Category', title='Success count w/ Payload mass for all sites')
        return fig
    else:
        fig=px.scatter(filtered_df[filtered_df['Launch Site']==entered_site], x='Payload Mass (kg)', y='class', color='Booster Version Category', title=f"Success count w/ Payload mass for site {entered_site}")
        return fig

# Run the app
if __name__ == '__main__':
    app.run_server()