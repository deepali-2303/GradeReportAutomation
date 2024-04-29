from dash import Dash, html, dcc
from dash.dependencies import Input, Output
import pandas as pd
import plotly.graph_objs as go
import plotly.express as px
import os

# df = pd.read_csv('Sem I Res.csv')
df = pd.read_csv('./Result/Sem 1 Res.csv')
pass_criteria_df = pd.read_csv('passCriteria.csv')
Merged_df = pd.read_csv('merged_df.csv')

# Initialize the app
app = Dash(__name__, suppress_callback_exceptions=True)
app.css.config.serve_locally = True

def list_csv_files(folder_path):
    csv_files = []
    for file in os.listdir(folder_path):
        if file.endswith('.csv'):
            csv_files.append(file)
    return csv_files


# Load the CSV data
df2 = pd.read_csv('subject_count_data.csv')

# Sort the DataFrame by 'Count' in descending order
df_sorted = df2.sort_values(by='Count', ascending=False)

fig = px.funnel(df_sorted, x='Count', y='Subject', height=800)

def get_status_counts(csv_file):
    # Read the CSV file
    df = pd.read_csv(os.path.join('./Status/Status', csv_file))
    # Extract Status column
    status_counts = df['Status'].value_counts()
    return status_counts, df

# App layout with dcc.Location to track the current URL
app.layout = html.Div([
    dcc.Location(id='url', refresh=False),  # This will track the URL path
    html.Div(id='page-content')  # This is where the content for each page will be displayed
],
className="Main"
)
def mainpage():
    return html.Div([
        html.A("Marks vs Students", href="/marks_vs_students", className="ele"),
        html.A("CGPA vs Semester", href="/cgpVsSem", className="ele"),
        html.A("Overall Performance", href="/overall_performance", className="ele"),
        html.A("Funnel Distribution", href="/funnel_chart", className="ele"),
        html.A("Status Pie Chart", href="/status_pie_chart", className="ele"),
    ])

def marks_vs_students_page():
    return html.Div([
        html.Div([
            html.A("Marks vs Students", href="/marks_vs_students", className="ele active"),
            html.A("CGPA vs Semester", href="/cgpVsSem", className="ele"),
            html.A("Overall Performance", href="/overall_performance", className="ele"),
            html.A("Funnel Distribution", href="/funnel_chart", className="ele"),
            html.A("Status Pie Chart", href="/status_pie_chart", className="ele"),
        ],
        className="Nav"
        ),
        html.H2("Marks vs Students"),
        html.Div([
            dcc.Dropdown(
                id='csv-dropdown',
                options=[{'label': file, 'value': file} for file in list_csv_files('Result')],
                placeholder='Select File',
                className="drop drop2",
                clearable=False,
            ),
            dcc.Dropdown(
                id='subject-dropdown',
                placeholder='Select Subject',
                className="drop drop2",
            ),
            dcc.Dropdown(
                id='plot-type-dropdown',
                options=[
                    {'label': 'Line Chart', 'value': 'line'},
                    {'label': 'Box Plot', 'value': 'box'}
                ],
                value='line',  # Set default value to Line Chart
                className="drop drop2",
                clearable=False,
            ),
            dcc.Dropdown(
                id='sorting-dropdown',
                options=[
                    {'label': 'Ascending', 'value': 'ascending'},
                    {'label': 'Descending', 'value': 'descending'}
                ],
                value='ascending',  # Set default value
                className="drop drop2",
                clearable=False,
            ),
        ], className="Box_drop"),
        dcc.Graph(id='subject-graph', className="cont1"),
    ])

# Page 2: Student-Wise Marks
def cgp_vs_sem():
    return html.Div([
        html.Div([
            html.A("Marks vs Students", href="/marks_vs_students", className="ele"),
            html.A("CGPA vs Semester", href="/cgpVsSem", className="ele active"),
            html.A("Overall Performance", href="/overall_performance", className="ele"),
            html.A("Funnel Distribution", href="/funnel_chart", className="ele"),
            html.A("Status Pie Chart", href="/status_pie_chart", className="ele"),
        ],
        className="Nav"
        ),
        html.H2("CGPA vs Semester Line Graph"),
        dcc.Dropdown(
            id='cgpa-uid-dropdown',
            options=[{'label': uid, 'value': uid} for uid in df['UID']],
            value=df['UID'].iloc[0],
            className='drop'
        ),
        dcc.Graph(id='cgpa-line-graph', className='cont')
    ])

# Page 3: Overall Performance
def overall_performance_page():
    return html.Div([
        html.Div([
            html.A("Marks vs Students", href="/marks_vs_students", className="ele"),
            html.A("CGPA vs Semester", href="/cgpVsSem", className="ele"),
            html.A("Overall Performance", href="/overall_performance", className="ele active"),
            html.A("Funnel Distribution", href="/funnel_chart", className="ele"),
            html.A("Status Pie Chart", href="/status_pie_chart", className="ele"),
        ],
        className="Nav"
        ),
        html.H2("Overall Performance"),
        dcc.Dropdown(
            className="drop",
            id='student-dropdown2',
            options=[{'label': uid, 'value': uid} for uid in df['UID']],
            value=df['UID'].iloc[0],
            clearable=False,
        ),
        dcc.Graph(id='overall-performance-radar-chart', className="cont"),
    ])

def status_pie_chart():
    return html.Div([
        html.Div([
            html.A("Marks vs Students", href="/marks_vs_students", className="ele"),
            html.A("CGPA vs Semester", href="/cgpVsSem", className="ele"),
            html.A("Overall Performance", href="/overall_performance", className="ele"),
            html.A("Funnel Distribution", href="/funnel_chart", className="ele"),
            html.A("Status Pie Chart", href="/status_pie_chart", className="ele active"),
        ],
        className="Nav"
        ),
        html.H2('Status Pie Chart'),
        dcc.Dropdown(
            id='csv-dropdown',
            options=[{'label': file, 'value': file} for file in list_csv_files('./Status/Status')],
            value=list_csv_files('./Status/Status')[0],  # Select the first CSV file by default
            placeholder='Select CSV File',
            style={'width': '50%', 'margin-bottom': '20px'}
        ),
        html.Div([
            dcc.Graph(id='status-pie-chart'),
            html.Div(id='popup')
        ], className="Big_box")
    ], className="Big_Big_box")

def funnel():
    return html.Div([
        html.Div([
            html.A("Marks vs Students", href="/marks_vs_students", className="ele"),
            html.A("CGPA vs Semester", href="/cgpVsSem", className="ele"),
            html.A("Overall Performance", href="/overall_performance", className="ele"),
            html.A("Funnel Distribution", href="/funnel_chart", className="ele active"),
            html.A("Status Pie Chart", href="/status_pie_chart", className="ele"),
        ],
        className="Nav"
        ),
        html.H2('Subject Funnel Distribution'),
        dcc.Graph(id='funnel-chart', figure=fig)
    ])

# Callback to update the page content based on the current URL
@app.callback(
    Output('page-content', 'children'),
    [Input('url', 'pathname')]
)

def display_page(pathname):
    if pathname == '/marks_vs_students':
        return marks_vs_students_page()  # Render content for this page
    elif pathname == '/cgpVsSem':
        return cgp_vs_sem()  # Render content for this page
    elif pathname == '/overall_performance':
        return overall_performance_page()  # Render content for this page
    elif pathname == '/funnel_chart':
        return funnel()
    elif pathname == '/status_pie_chart':
        return status_pie_chart()
    else:
        return mainpage()


@app.callback(
    [Output('subject-dropdown', 'options'),
     Output('subject-dropdown', 'value')],  # Set default value
    [Input('csv-dropdown', 'value')]
)
def update_subject_dropdown(csv_file):
    if csv_file:
        # Read the CSV file
        df = pd.read_csv(os.path.join('Result', csv_file))
        # Extract subject names from the CSV file
        subjects = df.columns[2:]
        options = [{'label': subject.replace('_', ' '), 'value': subject} for subject in subjects]
        default_value = subjects[0]  # Set default value to the first subject
        return options, default_value
    else:
        return [], None
    

# Define callback to update graph based on plot type selection
@app.callback(
    Output('subject-graph', 'figure'),
    [Input('plot-type-dropdown', 'value'),
     Input('csv-dropdown', 'value'),
     Input('subject-dropdown', 'value'),
     Input('sorting-dropdown', 'value')]
)
def update_graph(plot_type, csv_file, subject, sorting_order):
    if csv_file:
        # Read the CSV file
        df = pd.read_csv(os.path.join('Result', csv_file))
        # Sort the data based on marks and sorting order
        if sorting_order == 'ascending':
            df.sort_values(by=subject, ascending=True, inplace=True)
        elif sorting_order == 'descending':
            df.sort_values(by=subject, ascending=False, inplace=True)
        if plot_type == 'line':
            # Plot the line graph for the selected subject
            fig = go.Figure(data=go.Scatter(x=df['Name'], y=df[subject], mode='lines+markers'))
            fig.update_layout(title=f'{subject.replace("_", " ").title()} vs Students for {csv_file[:-4]}', yaxis_title='Marks', plot_bgcolor='#f9f9f9', margin=dict(t=50, l=50, r=50, b=50))
            fig.update_xaxes(showticklabels=False)
        elif plot_type == 'box':
            # Plot the vertical box plot for the selected subject
            fig = go.Figure(data=go.Box(y=df[subject], orientation='v'))
            fig.update_layout(title=f'{subject.replace("_", " ").title()} Box Plot for {csv_file[:-4]}', yaxis_title='Marks', plot_bgcolor='#f9f9f9', margin=dict(t=50, l=50, r=50, b=50))
        return fig
    else:
        return {}


# Define callback to update CGPA line graph based on dropdown selection
@app.callback(
    Output('cgpa-uid-dropdown', 'options'),
    [Input('student-dropdown', 'value')]
)
def update_cgpa_uid_dropdown(selected_subject):
    # Read the CGPA data from CSV
    cgpa_df = pd.read_csv('cgpa_data.csv')
    
    # Get all unique UIDs
    all_uids = cgpa_df['UID'].unique()
    
    # Create options for dropdown
    options = [{'label': uid, 'value': uid} for uid in all_uids]
    
    return options

@app.callback(
    Output('cgpa-line-graph', 'figure'),
    [Input('cgpa-uid-dropdown', 'value')]
)
def update_cgpa_line_graph(selected_uid):
    # Read the CGPA data from CSV
    cgpa_df = pd.read_csv('cgpa_data.csv')
    
    # Filter data for the selected UID
    selected_student_cgpa = cgpa_df[cgpa_df['UID'] == selected_uid]
    
    # Get the semester and CGPA columns
    semesters = selected_student_cgpa.columns[1:]
    cgpa_values = selected_student_cgpa.iloc[0, 1:].tolist()
    
    # Plot the CGPA line graph
    fig = go.Figure(data=go.Scatter(x=semesters, y=cgpa_values, mode='lines+markers'))
    fig.update_layout(title=f'Student UID: {selected_uid}', xaxis_title='Semester', yaxis_title='CGPA', plot_bgcolor='#f9f9f9', margin=dict(t=50, l=50, r=50, b=50))
    # fig.update_yaxes(range=[0, 10])  # Set y-axis range from 0 to 10
    return fig


@app.callback(
    Output('student-bar-graph', 'figure'),
    [Input('student-dropdown1', 'value')]
)
def update_bar_graph(selected_student):
    student_row = df[df['UID'] == selected_student].iloc[0]

    subjects = [col.replace('_', ' ') for col in df.columns[2:]]
    marks = student_row[2:].tolist()

    colors = []
    pass_criteria_df = pd.read_csv('passCriteria.csv')

    for subject, mark in zip(subjects, marks):
        if subject in pass_criteria_df['Subject'].values:
            pass_criteria = pass_criteria_df[pass_criteria_df['Subject'] == subject]['Pass Marks'].values[0]
            pass_criteria = int(pass_criteria)
            if int(mark) < pass_criteria:
                colors.append('red')
            else:
                colors.append('green')
        else:
            colors.append('gray')

    fig = go.Figure(data=go.Bar(x=subjects, y=marks, marker_color=colors))
    fig.update_layout(
        title=f'Marks for Student UID {selected_student}',
        xaxis_title='Subjects',
        yaxis_title='Marks',
        plot_bgcolor='#f9f9f9',
        margin=dict(t=50, l=50, r=50, b=50),
    )
    return fig

@app.callback(
    Output('overall-performance-radar-chart', 'figure'),
    [Input('student-dropdown2', 'value')]
)
def update_radar_chart(selected_student):
    student_row = df[df['UID'] == selected_student].iloc[0]
    subjects = [col.replace('_', ' ') for col in df.columns[2:]]
    marks = student_row[2:].tolist()
    fig = go.Figure(data=go.Scatterpolar(r=marks, theta=subjects, fill='toself'))
    fig.update_layout(
        title=f'Student UID: {selected_student}',
        polar=dict(
            radialaxis=dict(visible=True, range=[0, 100]),
        ),
        plot_bgcolor='#f9f9f9',
        margin=dict(t=50, l=50, r=50, b=50),
    )
    return fig

# Define callback to update pie chart based on CSV file selection
@app.callback(
    Output('status-pie-chart', 'figure'),
    [Input('csv-dropdown', 'value')]
)
def update_pie_chart(csv_file):
    if csv_file:
        # Get status counts and dataframe
        status_counts, df = get_status_counts(csv_file)
        
        # Define colors for pie slices
        colors = ['#1f77b4', '#ff7f0e', '#2ca02c']  # Blue, Orange, Green
        
        # Create pie chart data
        pie_data = [
            go.Pie(labels=status_counts.index, values=status_counts.values, marker=dict(colors=colors))
        ]
        
        # Create pie chart layout
        pie_layout = go.Layout(
            title=f'Status Distribution for {csv_file}',
            plot_bgcolor='#f9f9f9',
            margin=dict(t=50, l=50, r=50, b=50)
        )
        
        # Create pie chart figure
        pie_fig = go.Figure(data=pie_data, layout=pie_layout)
        
        return pie_fig
    else:
        return {}

# Define callback to display UIDs in a popup when pie chart slice is clicked
@app.callback(
    Output('popup', 'children'),
    [Input('status-pie-chart', 'clickData'),
     Input('csv-dropdown', 'value')]
)
def display_uids(click_data, csv_file):
    if click_data is not None and csv_file:
        # Get status and corresponding UIDs
        status = click_data['points'][0]['label']
        df = pd.read_csv(os.path.join('./Status/Status', csv_file))
        uids = df[df['Status'] == status]['UID'].tolist()
        
        # Create popup with UIDs
        popup_content = html.Div([
            html.H3(f'UIDs for {status}:'),
            html.Ul([html.Li(uid, className="list_ele") for uid in uids], className='list')
        ])
        
        return popup_content
    else:
        return html.Div()



# Run the app
if __name__ == "__main__":
    app.run_server(debug=True)