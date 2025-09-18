import plotly.graph_objects as go
import numpy as np
import pandas as pd

# Parse the data
data = {
    "user_roles": ["Public User", "Student", "Alumni", "College Admin", "Organization"],
    "features": [
        {"name": "Profile Management", "access": {"Public User": "View Only", "Student": "Read/Write", "Alumni": "Read/Write", "College Admin": "Admin", "Organization": "Read/Write"}},
        {"name": "Certificate Upload", "access": {"Public User": "No Access", "Student": "Upload", "Alumni": "Upload", "College Admin": "No Access", "Organization": "No Access"}},
        {"name": "Certificate Verification", "access": {"Public User": "No Access", "Student": "View Own", "Alumni": "View Own", "College Admin": "Approve/Reject", "Organization": "Verify Others"}},
        {"name": "Event Creation", "access": {"Public User": "View Only", "Student": "No Access", "Alumni": "No Access", "College Admin": "Create", "Organization": "Create"}},
        {"name": "Event Participation", "access": {"Public User": "View Only", "Student": "Register", "Alumni": "Register", "College Admin": "Manage", "Organization": "Manage"}},
        {"name": "Notifications", "access": {"Public User": "No Access", "Student": "Receive", "Alumni": "Receive", "College Admin": "Send/Receive", "Organization": "Send/Receive"}},
        {"name": "Mentorship Program", "access": {"Public User": "No Access", "Student": "Request", "Alumni": "Mentor", "College Admin": "Monitor", "Organization": "No Access"}},
        {"name": "University Search", "access": {"Public User": "Full Access", "Student": "Full Access", "Alumni": "Full Access", "College Admin": "Full Access", "Organization": "Full Access"}},
        {"name": "Analytics/Reports", "access": {"Public User": "No Access", "Student": "Personal", "Alumni": "Personal", "College Admin": "Institution", "Organization": "Own Events"}},
        {"name": "User Management", "access": {"Public User": "No Access", "Student": "No Access", "Alumni": "No Access", "College Admin": "Students Only", "Organization": "No Access"}},
        {"name": "Credit System", "access": {"Public User": "No Access", "Student": "View Own", "Alumni": "View Own", "College Admin": "Award Credits", "Organization": "No Access"}},
        {"name": "ERP Integration", "access": {"Public User": "No Access", "Student": "Access", "Alumni": "No Access", "College Admin": "Manage", "Organization": "No Access"}}
    ]
}

# Create access level mapping
access_mapping = {
    "No Access": 0,
    "View Only": 1,
    "View Own": 2,
    "Personal": 2,
    "Access": 2,
    "Upload": 2,
    "Register": 2,
    "Receive": 2,
    "Request": 2,
    "Read/Write": 3,
    "Full Access": 3,
    "Create": 3,
    "Mentor": 3,
    "Verify Others": 3,
    "Own Events": 3,
    "Admin": 4,
    "Manage": 4,
    "Send/Receive": 4,
    "Monitor": 4,
    "Approve/Reject": 4,
    "Institution": 4,
    "Students Only": 4,
    "Award Credits": 4
}

# Color mapping for access levels
colors = ['#FFFFFF', '#D2BA4C', '#5D878F', '#2E8B57', '#1FB8CD']  # White, Yellow, Cyan, Green, Strong Cyan
access_labels = ['No Access', 'View Only', 'Basic Access', 'Full Access', 'Admin Access']

# Abbreviate feature names to fit 15 character limit
feature_abbreviations = {
    "Profile Management": "Profile Mgmt",
    "Certificate Upload": "Cert Upload", 
    "Certificate Verification": "Cert Verify",
    "Event Creation": "Event Create",
    "Event Participation": "Event Particip",
    "Notifications": "Notifications",
    "Mentorship Program": "Mentorship",
    "University Search": "Univ Search",
    "Analytics/Reports": "Analytics",
    "User Management": "User Mgmt",
    "Credit System": "Credit System",
    "ERP Integration": "ERP Integr"
}

# Create matrix data
user_roles = data["user_roles"]
features = [feature_abbreviations[f["name"]] for f in data["features"]]
access_text = []
access_values = []

for feature_data in data["features"]:
    row_text = []
    row_values = []
    for role in user_roles:
        access = feature_data["access"][role]
        row_text.append(access)
        row_values.append(access_mapping[access])
    access_text.append(row_text)
    access_values.append(row_values)

# Create heatmap
fig = go.Figure(data=go.Heatmap(
    z=access_values,
    x=user_roles,
    y=features,
    text=access_text,
    texttemplate="%{text}",
    textfont={"size": 10},
    colorscale=[[0, colors[0]], [0.25, colors[1]], [0.5, colors[2]], [0.75, colors[3]], [1, colors[4]]],
    showscale=False,
    hoverongaps=False,
    hovertemplate="<b>%{y}</b><br>%{x}: %{text}<extra></extra>"
))

# Update layout
fig.update_layout(
    title="Adhyayan Sathi Feature Access Matrix",
    xaxis_title="User Roles",
    yaxis_title="Features",
    font=dict(size=12),
)

# Update axes
fig.update_xaxes(side="bottom", tickangle=45)
fig.update_yaxes(autorange="reversed")

# Save the charts
fig.write_image("feature_matrix.png")
fig.write_image("feature_matrix.svg", format="svg")