# Import packages
from dash import Dash, html, dcc, callback_context
from dash.dependencies import Input, Output
import pandas as pd
import plotly.graph_objs as go

# Incorporate data
df = pd.read_csv('Sem I Res.csv')

# Initialize the app
app = Dash(__name__)

# App layout
app.layout = html.Div([
    html.Div(children='Marks vs Students Line Graph', style={'font-size': '24px', 'margin-bottom': '20px', 'text-align': 'center'}),
    dcc.Dropdown(
        id='subject-dropdown',
        options=[{'label': col.replace('_', ' '), 'value': col} for col in df.columns[2:]],
        value=df.columns[2],
        style={'width': '50%', 'margin-bottom': '20px'}
    ),
    dcc.Graph(id='subject-line-graph', style={'height': '600px', 'margin-bottom': '20px', 'border': '1px solid #ddd', 'padding': '20px', 'border-radius': '10px'}),
    html.Div([
        html.Div(children='Student-wise Marks Bar Graph', style={'font-size': '24px', 'margin-bottom': '20px', 'text-align': 'center'}),
        dcc.Dropdown(
            id='student-dropdown',
            options=[{'label': uid, 'value': uid} for uid in df['UID']],
            value=df['UID'].iloc[0],
            style={'width': '50%', 'margin-bottom': '20px'}
        ),
        dcc.Graph(id='student-bar-graph', style={'height': '600px', 'margin-bottom': '20px', 'border': '1px solid #ddd', 'padding': '20px', 'border-radius': '10px'})
    ])
])

# Define callback to update line graph based on dropdown selection
@app.callback(
    Output('subject-line-graph', 'figure'),
    [Input('subject-dropdown', 'value')]
)
def update_line_graph(selected_subject):
    marks = df[selected_subject].tolist()
    students = df['Name'].tolist()
    
    # Combine student names and marks into a list of tuples
    data = list(zip(students, marks))
    
    # Sort the data based on marks (ascending order)
    # To sort in descending order, set reverse=True
    data.sort(key=lambda x: x[1], reverse=False)  # Change reverse=True for descending order
    
    # Unzip the sorted data
    sorted_students, sorted_marks = zip(*data)
    
    # Plot the line graph with sorted data
    fig = go.Figure(data=go.Scatter(x=sorted_students, y=sorted_marks, mode='lines+markers'))
    fig.update_layout(title=f'Marks vs Students for {selected_subject.replace("_", " ")}', xaxis_title='Students', yaxis_title='Marks', plot_bgcolor='#f9f9f9', margin=dict(t=50, l=50, r=50, b=50))
    fig.update_xaxes(showticklabels=False)
    return fig


# Define callback to update bar graph based on student dropdown selection
@app.callback(
    Output('student-bar-graph', 'figure'),
    [Input('student-dropdown', 'value')]
)
def update_bar_graph(selected_student):
    # Get the row corresponding to the selected student
    student_row = df[df['UID'] == selected_student].iloc[0]
    
    # Extract subject names and marks
    subjects = [col.replace('_', ' ') for col in df.columns[2:]]
    marks = student_row[2:].tolist()
    
    # Read the pass criteria from passCriteria.csv
    pass_criteria_df = pd.read_csv('passCriteria.csv')
    
    # Initialize colors list for bars
    colors = []
    
    # Iterate over each subject's mark and check if it is below the pass criteria
    for subject, mark in zip(subjects, marks):
        # Check if the subject exists in pass_criteria_df
        if subject in pass_criteria_df['Subject'].values:
            pass_criteria = pass_criteria_df[pass_criteria_df['Subject'] == subject]['Pass Marks'].values[0]
            # Convert pass_criteria to integer
            pass_criteria = int(pass_criteria)
            mark = int(mark)
            if mark < pass_criteria:
                colors.append('red')  # Mark failed subject bars as red
            else:
                colors.append('green')  # Mark passed subject bars as green
        else:
            # If subject not found in pass_criteria_df, mark it as gray
            colors.append('gray')
    
    # Create bar graph with colors
    fig = go.Figure(data=go.Bar(x=subjects, y=marks, marker_color=colors))
    fig.update_layout(title=f'Marks for Student UID {selected_student}', xaxis_title='Subjects', yaxis_title='Marks', plot_bgcolor='#f9f9f9', margin=dict(t=50, l=50, r=50, b=50))
    return fig


# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
