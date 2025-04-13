# Import required libraries
import pandas as pd
import dash
from dash import html
from dash import dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Read the SpaceX data into pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")

# Get the min and max payload values
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

# Create a dash application
app = dash.Dash(__name__)

# Create an app layout
app.layout = html.Div(children=[
    html.H1('SpaceX Launch Records Dashboard',
            style={'textAlign': 'center', 'color': '#503D36', 'font-size': 40}),
    
    # TASK 1: Add a dropdown list to enable Launch Site selection
    dcc.Dropdown(id='site-dropdown',
                 options=[{'label': 'All Sites', 'value': 'ALL'}] + 
                         [{'label': site, 'value': site} for site in spacex_df['Launch Site'].unique()],
                 value='ALL',
                 placeholder="Select a Launch Site here",
                 searchable=True),
    
    html.Br(),
    
    # TASK 2: Add a pie chart to show the total successful launches count for all sites
    html.Div(dcc.Graph(id='success-pie-chart')),
    html.Br(),
    
    # TASK 3: Add a slider to select payload range
    html.P("Payload range (Kg):"),
    dcc.RangeSlider(
        id='payload-slider',
        min=int(min_payload),  # Convert to integer
        max=int(max_payload),  # Convert to integer
        step=1000,  # Adjust step size as needed
        marks={i: str(i) for i in range(int(min_payload), int(max_payload) + 1, 5000)},  # Convert to integer
        value=[int(min_payload), int(max_payload)],  # Default range (from min to max)
    ),
    
    # TASK 4: Add a scatter chart to show the correlation between payload and launch success
    html.Div(dcc.Graph(id='success-payload-scatter-chart')),
])

# TASK 2 Callback: Update pie chart based on launch site selection and payload range
@app.callback(
    Output(component_id='success-pie-chart', component_property='figure'),
    [Input(component_id='site-dropdown', component_property='value'),
     Input(component_id='payload-slider', component_property='value')]
)
def update_pie_chart(selected_site, selected_payload_range):
    # Filter by selected launch site
    if selected_site == 'ALL':
        filtered_df = spacex_df
    else:
        filtered_df = spacex_df[spacex_df['Launch Site'] == selected_site]
    
    # Filter by selected payload range
    min_payload, max_payload = selected_payload_range
    filtered_df = filtered_df[(filtered_df['Payload Mass (kg)'] >= min_payload) & 
                               (filtered_df['Payload Mass (kg)'] <= max_payload)]
    
    # Create the pie chart
    if selected_site == 'ALL':
        fig = px.pie(filtered_df[filtered_df['class'] == 1],
                     names='Launch Site',
                     title='Total Successful Launches by Site')
    else:
        fig = px.pie(filtered_df,
                     names='class',
                     title=f'Total Success vs Failure for site {selected_site}',
                     hole=0.3,
                     labels={0: 'Failure', 1: 'Success'})
    return fig

# TASK 4 Callback: Update scatter chart based on selected site and payload range
@app.callback(
    Output(component_id='success-payload-scatter-chart', component_property='figure'),
    [Input(component_id='site-dropdown', component_property='value'),
     Input(component_id='payload-slider', component_property='value')]
)
def update_scatter_chart(selected_site, selected_payload_range):
    # Filter by selected launch site
    if selected_site == 'ALL':
        filtered_df = spacex_df
    else:
        filtered_df = spacex_df[spacex_df['Launch Site'] == selected_site]
    
    # Filter by selected payload range
    min_payload, max_payload = selected_payload_range
    filtered_df = filtered_df[(filtered_df['Payload Mass (kg)'] >= min_payload) & 
                               (filtered_df['Payload Mass (kg)'] <= max_payload)]
    
    # Create the scatter plot
    fig = px.scatter(filtered_df, 
                     x='Payload Mass (kg)', 
                     y='class', 
                     color='class',
                     title=f'Payload vs Launch Success for {selected_site if selected_site != "ALL" else "All Sites"}',
                     labels={'class': 'Launch Success', 'Payload Mass (kg)': 'Payload Mass (kg)'},
                     category_orders={'class': [0, 1]})  # Ensures the classes are ordered as Failure(0) and Success(1)
    return fig

# Run the app
if __name__ == '__main__':
    app.run(debug=True)

