import plotly.graph_objects as go
import pandas as pd

# Create architecture diagram with connections
fig = go.Figure()

# Define component positions and categories
components = {
    # Frontend Portals (top row)
    'Student Portal': {'x': 1, 'y': 4, 'color': '#1FB8CD', 'type': 'Frontend'},
    'College Portal': {'x': 3, 'y': 4, 'color': '#1FB8CD', 'type': 'Frontend'},
    'Org Portal': {'x': 5, 'y': 4, 'color': '#1FB8CD', 'type': 'Frontend'},
    'Public Portal': {'x': 7, 'y': 4, 'color': '#1FB8CD', 'type': 'Frontend'},
    
    # Core Systems (middle row)
    'API Gateway': {'x': 4, 'y': 3, 'color': '#DB4545', 'type': 'Core'},
    'Auth System': {'x': 2, 'y': 3, 'color': '#DB4545', 'type': 'Core'},
    'Database Layer': {'x': 6, 'y': 3, 'color': '#DB4545', 'type': 'Core'},
    
    # Services (bottom middle)
    'Notification': {'x': 1, 'y': 2, 'color': '#2E8B57', 'type': 'Service'},
    'Certificate': {'x': 4, 'y': 2, 'color': '#2E8B57', 'type': 'Service'},
    'Event Mgmt': {'x': 7, 'y': 2, 'color': '#2E8B57', 'type': 'Service'},
    
    # External Services (bottom row)
    'Email/SMS': {'x': 0.5, 'y': 1, 'color': '#5D878F', 'type': 'External'},
    'Cloud Storage': {'x': 2.5, 'y': 1, 'color': '#5D878F', 'type': 'External'},
    'Payment': {'x': 5.5, 'y': 1, 'color': '#5D878F', 'type': 'External'},
    'Social APIs': {'x': 7.5, 'y': 1, 'color': '#5D878F', 'type': 'External'}
}

# Define connections between components
connections = [
    # All portals connect to API Gateway
    ('Student Portal', 'API Gateway'),
    ('College Portal', 'API Gateway'),
    ('Org Portal', 'API Gateway'),
    ('Public Portal', 'API Gateway'),
    
    # API Gateway connects to core systems
    ('API Gateway', 'Auth System'),
    ('API Gateway', 'Database Layer'),
    
    # Core systems connect to services
    ('Auth System', 'Notification'),
    ('Database Layer', 'Certificate'),
    ('Database Layer', 'Event Mgmt'),
    
    # Services connect to external
    ('Notification', 'Email/SMS'),
    ('Certificate', 'Cloud Storage'),
    ('Event Mgmt', 'Social APIs'),
    ('API Gateway', 'Payment')
]

# Add connection lines
for start, end in connections:
    start_pos = components[start]
    end_pos = components[end]
    
    fig.add_trace(go.Scatter(
        x=[start_pos['x'], end_pos['x']],
        y=[start_pos['y'], end_pos['y']],
        mode='lines',
        line=dict(color='lightgray', width=2),
        showlegend=False,
        hoverinfo='skip'
    ))

# Add component nodes by type
for comp_type in ['Frontend', 'Core', 'Service', 'External']:
    comp_names = [name for name, info in components.items() if info['type'] == comp_type]
    x_vals = [components[name]['x'] for name in comp_names]
    y_vals = [components[name]['y'] for name in comp_names]
    colors = [components[name]['color'] for name in comp_names]
    
    fig.add_trace(go.Scatter(
        x=x_vals,
        y=y_vals,
        mode='markers+text',
        marker=dict(size=80, color=colors[0], line=dict(width=2, color='white')),
        text=comp_names,
        textposition='middle center',
        textfont=dict(size=11, color='white'),
        name=comp_type,
        hovertemplate='%{text}<br>Type: ' + comp_type + '<extra></extra>'
    ))

# Update layout
fig.update_layout(
    title='Adhyayan Sathi Architecture',
    xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
    yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
    plot_bgcolor='white',
    legend=dict(orientation='h', yanchor='bottom', y=1.05, xanchor='center', x=0.5)
)

# Save the chart
fig.write_image("architecture_chart.png")
fig.write_image("architecture_chart.svg", format="svg")

fig.show()