import plotly.graph_objects as go

# Define swimlane positions and colors with better contrast
swimlanes = {
    "Student": {"y_pos": 4, "color": "#1FB8CD"},
    "College Admin": {"y_pos": 3, "color": "#DB4545"}, 
    "Alumni": {"y_pos": 2, "color": "#2E8B57"},
    "Organization": {"y_pos": 1, "color": "#5D878F"},
    "System": {"y_pos": 0, "color": "#D2BA4C"}
}

fig = go.Figure()

# Add swimlane background rectangles with better visibility
for i, (role, props) in enumerate(swimlanes.items()):
    fig.add_shape(
        type="rect",
        x0=-1, x1=16,
        y0=props["y_pos"]-0.45, y1=props["y_pos"]+0.45,
        fillcolor=props["color"],
        opacity=0.15,
        layer="below",
        line=dict(color=props["color"], width=2)
    )
    
    # Add swimlane labels with better contrast
    fig.add_annotation(
        x=-0.5, y=props["y_pos"],
        text=role,
        showarrow=False,
        font=dict(size=14, color=props["color"], family="Arial Black"),
        xanchor="center",
        bgcolor="white",
        bordercolor=props["color"],
        borderwidth=1
    )

# All flows data
flows = [
    {
        "name": "Certificate Verification",
        "steps": [
            {"actor": "Student", "text": "Login", "x": 1},
            {"actor": "Student", "text": "Upload Cert", "x": 2},
            {"actor": "System", "text": "Create Request", "x": 3},
            {"actor": "College Admin", "text": "Review", "x": 4},
            {"actor": "College Admin", "text": "Approve/Reject", "x": 5, "decision": True},
            {"actor": "System", "text": "Send Status", "x": 6},
            {"actor": "Organization", "text": "Verify ID", "x": 7}
        ],
        "title_x": 4,
        "title_y": 4.8
    },
    {
        "name": "Notification Flow", 
        "steps": [
            {"actor": "College Admin", "text": "Create Notice", "x": 8},
            {"actor": "System", "text": "Process", "x": 9},
            {"actor": "Student", "text": "Receive", "x": 10}
        ],
        "title_x": 9,
        "title_y": 4.8
    },
    {
        "name": "Event Management",
        "steps": [
            {"actor": "Organization", "text": "Create Event", "x": 11},
            {"actor": "System", "text": "Publish", "x": 12},
            {"actor": "Student", "text": "Register", "x": 13},
            {"actor": "System", "text": "Track", "x": 14}
        ],
        "title_x": 12.5,
        "title_y": 1.8
    },
    {
        "name": "Alumni Mentorship",
        "steps": [
            {"actor": "Alumni", "text": "Set Available", "x": 1.5},
            {"actor": "Student", "text": "Search", "x": 2.5},
            {"actor": "Alumni", "text": "Accept/Decline", "x": 3.5, "decision": True},
            {"actor": "System", "text": "Track Session", "x": 4.5}
        ],
        "title_x": 2.5,
        "title_y": 2.8
    }
]

# Process all flows
for flow in flows:
    steps = flow["steps"]
    
    # Add flow title
    fig.add_annotation(
        x=flow["title_x"], y=flow["title_y"],
        text=flow["name"],
        showarrow=False,
        font=dict(size=12, color="black", family="Arial Bold"),
        xanchor="center",
        bgcolor="rgba(255,255,255,0.8)",
        bordercolor="black",
        borderwidth=1
    )
    
    # Add process boxes and arrows
    for i, step in enumerate(steps):
        y_pos = swimlanes[step["actor"]]["y_pos"]
        color = swimlanes[step["actor"]]["color"]
        
        # Handle decision points with diamond shape
        if step.get("decision", False):
            # Diamond for decision points
            path = f"M {step['x']-0.25} {y_pos} L {step['x']} {y_pos+0.2} L {step['x']+0.25} {y_pos} L {step['x']} {y_pos-0.2} Z"
            fig.add_shape(
                type="path",
                path=path,
                fillcolor=color,
                opacity=0.9,
                line=dict(color="white", width=3)
            )
        else:
            # Rectangle for regular processes
            fig.add_shape(
                type="rect",
                x0=step["x"]-0.35, x1=step["x"]+0.35,
                y0=y_pos-0.18, y1=y_pos+0.18,
                fillcolor=color,
                opacity=0.9,
                line=dict(color="white", width=3)
            )
        
        # Add text with better visibility
        fig.add_annotation(
            x=step["x"], y=y_pos,
            text=step["text"],
            showarrow=False,
            font=dict(size=11, color="white", family="Arial Bold"),
            xanchor="center"
        )
        
        # Add arrows between steps
        if i < len(steps) - 1:
            next_step = steps[i + 1]
            next_y = swimlanes[next_step["actor"]]["y_pos"]
            
            # Calculate arrow position
            start_x = step["x"] + 0.35
            end_x = next_step["x"] - 0.35
            mid_x = (start_x + end_x) / 2
            
            fig.add_annotation(
                x=end_x, y=next_y,
                ax=start_x, ay=y_pos,
                axref="x", ayref="y",
                xref="x", yref="y",
                arrowhead=2,
                arrowsize=1.5,
                arrowwidth=3,
                arrowcolor="#333333"
            )

# Add legend for decision points
fig.add_shape(
    type="path", 
    path="M 15.2 -0.7 L 15.4 -0.5 L 15.2 -0.3 L 15 -0.5 Z",
    fillcolor="#999999",
    opacity=0.8,
    line=dict(color="white", width=2)
)

fig.add_annotation(
    x=15.8, y=-0.5,
    text="Decision Point",
    showarrow=False,
    font=dict(size=10, color="black"),
    xanchor="left"
)

# Configure layout for better presentation
fig.update_layout(
    title=dict(
        text="Adhyayan Platform User Flows",
        font=dict(size=18, color="black", family="Arial Bold"),
        x=0.5,
        xanchor="center"
    ),
    xaxis=dict(
        showgrid=False,
        showticklabels=False,
        range=[-1.5, 16.5],
        fixedrange=True
    ),
    yaxis=dict(
        showgrid=False,
        showticklabels=False,
        range=[-1, 5.2],
        fixedrange=True
    ),
    showlegend=False,
    plot_bgcolor="white",
    paper_bgcolor="white"
)

# Save the chart
fig.write_image("user_flow_diagram.png")
fig.write_image("user_flow_diagram.svg", format="svg")

fig.show()