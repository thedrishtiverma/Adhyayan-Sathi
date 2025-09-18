import plotly.graph_objects as go
import numpy as np

# Define entities with complete attributes and better positioning
entities_data = {
    "Users": {
        "type": "User Management", 
        "color": "#1FB8CD", 
        "position": (3, 8),
        "attributes": [
            "user_id (PK)",
            "email", 
            "password_hash", 
            "user_type", 
            "created_at", 
            "updated_at", 
            "is_active"
        ]
    },
    "Students": {
        "type": "Academic", 
        "color": "#2E8B57", 
        "position": (1, 6),
        "attributes": [
            "student_id (PK)",
            "user_id (FK)", 
            "university_id (FK)", 
            "enrollment_no", 
            "course", 
            "year", 
            "grad_status"
        ]
    },
    "Alumni": {
        "type": "Academic", 
        "color": "#2E8B57", 
        "position": (5, 6),
        "attributes": [
            "alumni_id (PK)",
            "user_id (FK)", 
            "university_id (FK)", 
            "grad_year", 
            "degree", 
            "company", 
            "expertise"
        ]
    },
    "Universities": {
        "type": "Institution", 
        "color": "#5D878F", 
        "position": (3, 4),
        "attributes": [
            "university_id (PK)",
            "name", 
            "code", 
            "state", 
            "region", 
            "affiliation_no", 
            "admin_user_id (FK)"
        ]
    },
    "Organizations": {
        "type": "External", 
        "color": "#DB4545", 
        "position": (7, 8),
        "attributes": [
            "org_id (PK)",
            "name", 
            "industry", 
            "website", 
            "admin_user_id (FK)", 
            "verify_status"
        ]
    },
    "Certificates": {
        "type": "Academic", 
        "color": "#2E8B57", 
        "position": (1, 2),
        "attributes": [
            "cert_id (PK)",
            "student_id (FK)", 
            "university_id (FK)", 
            "cert_type", 
            "file_path", 
            "status", 
            "upload_date"
        ]
    },
    "Events": {
        "type": "Activity", 
        "color": "#D2BA4C", 
        "position": (7, 6),
        "attributes": [
            "event_id (PK)",
            "org_id (FK)", 
            "title", 
            "description", 
            "date_time", 
            "location", 
            "max_participants"
        ]
    },
    "Notifications": {
        "type": "Communication", 
        "color": "#B4413C", 
        "position": (5, 8),
        "attributes": [
            "notif_id (PK)",
            "sender_id (FK)", 
            "title", 
            "content", 
            "target_audience", 
            "sent_at", 
            "status"
        ]
    },
    "Enrollments": {
        "type": "Academic", 
        "color": "#2E8B57", 
        "position": (3, 2),
        "attributes": [
            "enroll_id (PK)",
            "student_id (FK)", 
            "university_id (FK)", 
            "enroll_date", 
            "course_code", 
            "status"
        ]
    },
    "Mentorships": {
        "type": "Activity", 
        "color": "#D2BA4C", 
        "position": (5, 2),
        "attributes": [
            "mentor_id (PK)",
            "alumni_id (FK)", 
            "student_id (FK)", 
            "start_date", 
            "status", 
            "session_count"
        ]
    }
}

# Define relationships with proper cardinality
relationships = [
    {"from": "Users", "to": "Students", "cardinality": "1:1"},
    {"from": "Users", "to": "Alumni", "cardinality": "1:1"},
    {"from": "Universities", "to": "Students", "cardinality": "1:M"},
    {"from": "Students", "to": "Certificates", "cardinality": "1:M"},
    {"from": "Organizations", "to": "Events", "cardinality": "1:M"},
    {"from": "Alumni", "to": "Mentorships", "cardinality": "1:M"},
    {"from": "Students", "to": "Enrollments", "cardinality": "1:M"},
    {"from": "Universities", "to": "Certificates", "cardinality": "1:M"},
    {"from": "Universities", "to": "Enrollments", "cardinality": "1:M"},
    {"from": "Students", "to": "Mentorships", "cardinality": "1:M"}
]

# Create the figure
fig = go.Figure()

# Add relationship lines
entity_positions = {name: info["position"] for name, info in entities_data.items()}

for rel in relationships:
    from_pos = entity_positions[rel["from"]]
    to_pos = entity_positions[rel["to"]]
    
    # Add relationship line
    fig.add_trace(go.Scatter(
        x=[from_pos[0], to_pos[0]],
        y=[from_pos[1], to_pos[1]],
        mode='lines',
        line=dict(color='#333333', width=2),
        showlegend=False,
        hoverinfo='skip'
    ))
    
    # Add cardinality label
    mid_x = (from_pos[0] + to_pos[0]) / 2
    mid_y = (from_pos[1] + to_pos[1]) / 2
    
    fig.add_trace(go.Scatter(
        x=[mid_x],
        y=[mid_y],
        mode='text',
        text=rel["cardinality"],
        textfont=dict(size=14, color='black', family='Arial Black'),
        textposition="middle center",
        showlegend=False,
        hoverinfo='skip'
    ))

# Add entity boxes with attributes
box_width = 1.6
box_height = 1.2

for entity_name, entity_info in entities_data.items():
    x, y = entity_info["position"]
    color = entity_info["color"]
    
    # Add entity box background
    fig.add_shape(
        type="rect",
        x0=x - box_width/2, y0=y - box_height/2,
        x1=x + box_width/2, y1=y + box_height/2,
        fillcolor=color,
        line=dict(color="black", width=2)
    )
    
    # Add entity name header
    fig.add_trace(go.Scatter(
        x=[x],
        y=[y + 0.35],
        mode='text',
        text=f"<b>{entity_name}</b>",
        textfont=dict(size=16, color='white', family='Arial Black'),
        textposition="middle center",
        name=entity_info["type"],
        showlegend=True,
        hoverinfo='skip'
    ))
    
    # Create attributes text with proper formatting
    attrs_formatted = []
    for attr in entity_info["attributes"]:
        if "(PK)" in attr:
            attrs_formatted.append(f"<b>{attr}</b>")
        elif "(FK)" in attr:
            attrs_formatted.append(f"<i>{attr}</i>")
        else:
            attrs_formatted.append(attr)
    
    # Split attributes into two columns for better fit
    attrs_text = "<br>".join(attrs_formatted)
    
    fig.add_trace(go.Scatter(
        x=[x],
        y=[y - 0.1],
        mode='text',
        text=attrs_text,
        textfont=dict(size=10, color='white'),
        textposition="middle center",
        showlegend=False,
        hoverinfo='skip'
    ))

# Remove duplicate legend entries
legend_names = []
for trace in fig.data:
    if hasattr(trace, 'name') and trace.name and trace.showlegend:
        if trace.name in legend_names:
            trace.showlegend = False
        else:
            legend_names.append(trace.name)

# Update layout
fig.update_layout(
    title="Adhyayan Sathi Platform ERD",
    xaxis=dict(
        range=[0, 8],
        showgrid=False, 
        zeroline=False, 
        showticklabels=False
    ),
    yaxis=dict(
        range=[0.5, 9],
        showgrid=False, 
        zeroline=False, 
        showticklabels=False
    ),
    plot_bgcolor='white',
    paper_bgcolor='white',
    legend=dict(
        orientation='h',
        yanchor='bottom',
        y=1.02,
        xanchor='center',
        x=0.5,
        title="Entity Types"
    )
)

fig.update_traces(cliponaxis=False)

# Save the chart
fig.write_image("erd_diagram.png")
fig.write_image("erd_diagram.svg", format="svg")

fig.show()