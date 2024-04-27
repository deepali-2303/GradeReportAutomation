# Import packages
from dash import Dash, html, dcc
from dash.dependencies import Input, Output
import pandas as pd
import plotly.graph_objs as go
import plotly.express as px  # Ensure you import Plotly Express

# Incorporate data
df = pd.read_csv('Sem I Res.csv')
pass_criteria_df = pd.read_csv('passCriteria.csv')


# Initialize the app
app = Dash(__name__)

# App layout with Tabs
app.layout = html.Div([
    dcc.Tabs([
        dcc.Tab(label='Marks vs Students', style={'border-radius': '10px'}, children=[
            dcc.Dropdown(
                id='subject-dropdown0',
                options=[{'label': col.replace('_', ' '), 'value': col} for col in df.columns[2:]],
                value=df.columns[2],
                style={'width': '50%', 'margin-bottom': '20px'}
            ),
            dcc.Graph(id='subject-line-graph', style={'height': '100vh', 'border': '1px solid #ddd', 'padding': '20px', 'border-radius': '10px'}),
        ]),

        dcc.Tab(label='Student-wise Marks', style={'border-radius': '10px'}, children=[
            dcc.Dropdown(
                id='student-dropdown1',
                options=[{'label': uid, 'value': uid} for uid in df['UID']],
                value=df['UID'].iloc[0],
                style={'width': '50%', 'margin-bottom': '20px'}
            ),
            dcc.Graph(id='student-bar-graph', style={'height': '100vh', 'border': '1px solid #ddd', 'padding': '20px', 'border-radius': '10px'}),
        ]),

        dcc.Tab(label='Overall Performance Radar Chart', style={'border-radius': '10px'}, children=[
          dcc.Dropdown(
              id='student-dropdown2',
              options=[{'label': uid, 'value': uid} for uid in df['UID']],
              value=df['UID'].iloc[0],
              style={'width': '50%', 'margin-bottom': '20px'}
            ),
            dcc.Graph(id='overall-performance-radar-chart', style={'height': '100vh', 'margin-bottom': '20px', 'border': '1px solid #ddd', 'padding': '20px', 'border-radius': '10px'})
        ]),
    ])
])

# Callback to update the line graph based on the subject dropdown
@app.callback(
    Output('subject-line-graph', 'figure'),
    [Input('subject-dropdown0', 'value')]
)
def update_line_graph(selected_subject):
    marks = df[selected_subject].tolist()
    students = df['Name'].tolist()

    data = list(zip(students, marks))
    data.sort(key=lambda x: x[1], reverse=False)

    sorted_students, sorted_marks = zip(*data)

    fig = go.Figure(data=go.Scatter(x=sorted_students, y=sorted_marks, mode='lines+markers'))
    fig.update_layout(title=f'Marks vs Students for {selected_subject.replace("_", " ")}', xaxis_title='Students', yaxis_title='Marks', plot_bgcolor='#f9f9f9', margin=dict(t=50, l=50, r=50, b=50))
    fig.update_xaxes(showticklabels=False)
    return fig

# Callback to update the bar graph based on the student dropdown
@app.callback(
    Output('student-bar-graph', 'figure'),
    [Input('student-dropdown1', 'value')]
)
def update_bar_graph(selected_student):
    student_row = df[df['UID'] == selected_student].iloc[0]

    subjects = [col.replace('_', ' ') for col in df.columns[2:]]
    marks = student_row[2:].tolist()

    pass_criteria_df = pd.read_csv('passCriteria.csv')

    colors = []
    for subject, mark in zip(subjects, marks):
        if subject in pass_criteria_df['Subject'].values:
            pass_criteria = pass_criteria_df[pass_criteria_df['Subject'] == subject]['Pass Marks'].values[0]
            pass_criteria = int(pass_criteria)
            mark = int(mark)
            if mark < pass_criteria:
                colors.append('red')
            else:
                colors.append('green')
        else:
            colors.append('gray')

    fig = go.Figure(data=go.Bar(x=subjects, y=marks, marker_color=colors))
    fig.update_layout(title=f'Marks for Student UID {selected_student}', xaxis_title='Subjects', yaxis_title='Marks', plot_bgcolor='#f9f9f9', margin=dict(t=50, l=50, r=50, b=50))
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
    fig.update_layout(title=f'Overall Performance for Student UID {selected_student}', polar=dict(radialaxis=dict(visible=True, range=[0, 100])), plot_bgcolor='#f9f9f9', margin=dict(t=50, l=50, r=50, b=50))
    return fig


# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
