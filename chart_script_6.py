import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from datetime import datetime, timedelta

# Create comprehensive timeline data with proper tracks
timeline_data = []
start_date = datetime(2024, 1, 1)

# Main Phases
phases = [
    {'Task': 'Planning', 'Start': 0, 'Duration': 4, 'Team': 'PM, BA, Arch', 'Resources': '3 people', 'Type': 'Main Phase'},
    {'Task': 'Design', 'Start': 4, 'Duration': 6, 'Team': 'UI/UX, DB Arch', 'Resources': '3 people', 'Type': 'Main Phase'},
    {'Task': 'Testing & QA', 'Start': 26, 'Duration': 6, 'Team': 'QA, Security', 'Resources': '2 people', 'Type': 'Main Phase'},
    {'Task': 'Deployment', 'Start': 32, 'Duration': 3, 'Team': 'DevOps, Admin', 'Resources': '2 people', 'Type': 'Main Phase'},
    {'Task': 'Post-Launch', 'Start': 35, 'Duration': 8, 'Team': 'Support Team', 'Resources': '3 people', 'Type': 'Ongoing'}
]

# Development Tracks (parallel)
dev_tracks = [
    {'Task': 'Frontend Dev', 'Start': 10, 'Duration': 12, 'Team': 'Frontend Dev', 'Resources': '2 people', 'Type': 'Frontend'},
    {'Task': 'Backend Dev', 'Start': 10, 'Duration': 14, 'Team': 'Backend Dev', 'Resources': '2 people', 'Type': 'Backend'},
    {'Task': 'Database Dev', 'Start': 10, 'Duration': 10, 'Team': 'DB Developer', 'Resources': '1 person', 'Type': 'Database'},
    {'Task': 'Infra Setup', 'Start': 12, 'Duration': 12, 'Team': 'DevOps Eng', 'Resources': '1 person', 'Type': 'Infrastructure'},
    {'Task': 'Integration', 'Start': 22, 'Duration': 4, 'Team': 'Full-Stack', 'Resources': '2 people', 'Type': 'Integration'}
]

# Combine all tasks
all_tasks = phases + dev_tracks

# Convert to DataFrame with proper date calculations
df_data = []
for task in all_tasks:
    start_week = task['Start']
    duration_weeks = task['Duration']
    
    df_data.append({
        'Task': task['Task'],
        'Start': start_date + timedelta(weeks=start_week),
        'Finish': start_date + timedelta(weeks=start_week + duration_weeks),
        'Team': task['Team'],
        'Resources': task['Resources'],
        'Duration': f"{duration_weeks}w" if duration_weeks < 20 else "Ongoing",
        'Type': task['Type']
    })

df = pd.DataFrame(df_data)

# Create Gantt chart
fig = px.timeline(df, 
                  x_start="Start", 
                  x_end="Finish", 
                  y="Task",
                  color="Type",
                  title="Adhyayan Sathi Dev Roadmap",
                  color_discrete_map={
                      'Main Phase': '#1FB8CD',
                      'Frontend': '#DB4545',
                      'Backend': '#2E8B57', 
                      'Database': '#5D878F',
                      'Infrastructure': '#D2BA4C',
                      'Integration': '#B4413C',
                      'Ongoing': '#964325'
                  })

# Add milestone markers as shapes
milestones = [
    {'week': 2, 'name': 'Requirements'},
    {'week': 8, 'name': 'Design Done'},
    {'week': 18, 'name': 'Alpha Ready'},
    {'week': 26, 'name': 'Beta Ready'},
    {'week': 35, 'name': 'Go Live'}
]

for milestone in milestones:
    milestone_date = start_date + timedelta(weeks=milestone['week'])
    fig.add_shape(
        type="line",
        x0=milestone_date,
        x1=milestone_date,
        y0=-0.5,
        y1=len(df)-0.5,
        line=dict(color='#13343B', width=2, dash='dot')
    )
    
    # Add milestone labels at top
    fig.add_annotation(
        x=milestone_date,
        y=len(df)-0.3,
        text=milestone['name'],
        showarrow=False,
        font=dict(size=9, color='#13343B'),
        bgcolor='rgba(255,255,255,0.8)',
        bordercolor='#13343B',
        borderwidth=1
    )

# Update layout
fig.update_layout(
    xaxis_title="Timeline",
    yaxis_title="Tasks & Tracks",
    legend=dict(
        orientation='h',
        yanchor='bottom',
        y=1.02,
        xanchor='center',
        x=0.5
    ),
    yaxis={
        'categoryorder': 'array', 
        'categoryarray': ['Post-Launch', 'Deployment', 'Testing & QA', 
                         'Integration', 'Infra Setup', 'Database Dev',
                         'Backend Dev', 'Frontend Dev', 'Design', 
                         'Planning']
    }
)

# Update traces with better hover info
fig.update_traces(
    cliponaxis=False,
    hovertemplate='<b>%{y}</b><br>' +
                  'Duration: %{customdata[0]}<br>' +
                  'Team: %{customdata[1]}<br>' +
                  'Resources: %{customdata[2]}<br>' +
                  '<extra></extra>',
    customdata=df[['Duration', 'Team', 'Resources']].values
)

# Add duration labels on bars
for i, row in df.iterrows():
    duration_text = row['Duration']
    if duration_text != 'Ongoing':
        fig.add_annotation(
            x=row['Start'] + (row['Finish'] - row['Start'])/2,
            y=i,
            text=duration_text,
            showarrow=False,
            font=dict(size=10, color='white', family='Arial Black'),
            bgcolor='rgba(0,0,0,0.6)'
        )

# Format x-axis 
fig.update_xaxes(
    dtick=14*24*60*60*1000,  # Bi-weekly ticks
    tickformat='Week %V',
    tickangle=0
)

# Save the chart
fig.write_image("roadmap.png")
fig.write_image("roadmap.svg", format="svg")

fig.show()