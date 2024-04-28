from dash import Dash, html, dcc
from dash.dependencies import Input, Output
import pandas as pd
import plotly.graph_objs as go

df = pd.read_csv('Sem I Res.csv')
pass_criteria_df = pd.read_csv('passCriteria.csv')

# Initialize the app
app = Dash(__name__, suppress_callback_exceptions=True)
app.css.config.serve_locally = True

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
        html.A("Student-Wise Marks", href="/student_wise_marks", className="ele"),
        html.A("Overall Performance", href="/overall_performance", className="ele"),
    ])

def marks_vs_students_page():
    return html.Div([
        html.Div([
            html.A("Marks vs Students", href="/marks_vs_students", className="ele active"),
            html.A("Student-Wise Marks", href="/student_wise_marks", className="ele"),
            html.A("Overall Performance", href="/overall_performance", className="ele"),
        ],
        className="Nav"
        ),
        html.H2("Marks vs Students"),
        dcc.Dropdown(
            id='subject-dropdown0',
            options=[{'label': col.replace('_', ' '), 'value': col} for col in df.columns[2:]],
            value=df.columns[2],
            className="drop",
            clearable=False,
        ),
        dcc.Graph(id='subject-line-graph', className="cont"),
    ])

# Page 2: Student-Wise Marks
def student_wise_marks_page():
    return html.Div([
        html.Div([
            html.A("Marks vs Students", href="/marks_vs_students", className="ele"),
            html.A("Student-Wise Marks", href="/student_wise_marks", className="ele active"),
            html.A("Overall Performance", href="/overall_performance", className="ele"),
        ],
        className="Nav"
        ),
        html.H2("Student-Wise Marks"),
        dcc.Dropdown(
            id='student-dropdown1',
            options=[{'label': uid, 'value': uid} for uid in df['UID']],
            value=df['UID'].iloc[0],
            className="drop",
            clearable=False,
        ),
        dcc.Graph(id='student-bar-graph', className="cont"),
    ])

# Page 3: Overall Performance
def overall_performance_page():
    return html.Div([
        html.Div([
            html.A("Marks vs Students", href="/marks_vs_students", className="ele"),
            html.A("Student-Wise Marks", href="/student_wise_marks", className="ele"),
            html.A("Overall Performance", href="/overall_performance", className="ele active"),
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

# Callback to update the page content based on the current URL
@app.callback(
    Output('page-content', 'children'),
    [Input('url', 'pathname')]
)

def display_page(pathname):
    if pathname == '/marks_vs_students':
        return marks_vs_students_page()  # Render content for this page
    elif pathname == '/student_wise_marks':
        return student_wise_marks_page()  # Render content for this page
    elif pathname == '/overall_performance':
        return overall_performance_page()  # Render content for this page
    else:
        return mainpage()



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
    fig.update_layout(
        # title=f'Marks vs Students for {selected_subject.replace("_", " ")}',
        xaxis_title='Students',
        xaxis=dict(showticklabels=False),
        yaxis_title='Marks',
        plot_bgcolor='#f9f9f9',
        margin=dict(t=50, l=50, r=50, b=50),
    )
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
        title=f'Overall Performance for Student UID {selected_student}',
        polar=dict(
            radialaxis=dict(visible=True, range=[0, 100]),
        ),
        plot_bgcolor='#f9f9f9',
        margin=dict(t=50, l=50, r=50, b=50),
    )
    return fig


# Run the app
if __name__ == "__main__":
    app.run_server(debug=True)
