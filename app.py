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
    fig = go.Figure(data=go.Scatter(x=students, y=marks, mode='lines+markers'))
    fig.update_layout(title=f'Marks vs Students for {selected_subject.replace("_", " ")}', xaxis_title='Students', yaxis_title='Marks', plot_bgcolor='#f9f9f9', margin=dict(t=50, l=50, r=50, b=50))
    fig.update_xaxes(showticklabels=False)
    return fig

# Define callback to update bar graph based on student dropdown selection
@app.callback(
    Output('student-bar-graph', 'figure'),
    [Input('student-dropdown', 'value')]
)
def update_bar_graph(selected_student):
    student_row = df[df['UID'] == selected_student].iloc[0]
    subjects = [col.replace('_', ' ') for col in df.columns[2:]]
    marks = student_row[2:].tolist()
    fig = go.Figure(data=go.Bar(x=subjects, y=marks))
    fig.update_layout(title=f'Marks for Student UID {selected_student}', xaxis_title='Subjects', yaxis_title='Marks', plot_bgcolor='#f9f9f9', margin=dict(t=50, l=50, r=50, b=50))
    return fig

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
