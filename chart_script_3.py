import plotly.graph_objects as go
import pandas as pd

# Parse the wireframe data
data = {
    "wireframes": [
        {
            "name": "Student Dashboard",
            "sections": [
                {"header": "Top Navigation", "elements": ["Logo", "Home", "Profile", "Certificates", "Notifications", "ERP", "Logout"]},
                {"sidebar": "Quick Links", "elements": ["My Profile", "Certificate Manager", "Credit Sheet", "Notifications", "ERP Portal", "Help & Support"]},
                {"main_content": "Dashboard Overview", "widgets": ["Welcome Message", "Recent Notifications", "Certificate Status", "Credit Score", "Quick Actions", "Upcoming Events"]},
                {"footer": "Footer Links", "elements": ["About", "Contact", "Privacy Policy"]}
            ]
        },
        {
            "name": "Alumni Dashboard",
            "sections": [
                {"header": "Top Navigation", "elements": ["Logo", "Home", "Profile", "Mentorship", "Network", "Events", "Logout"]},
                {"sidebar": "Alumni Menu", "elements": ["Complete Profile", "Mentorship Program", "Alumni Network", "Career Services", "Events", "Give Back"]},
                {"main_content": "Alumni Hub", "widgets": ["Profile Completion Bar", "Mentorship Requests", "Network Connections", "Upcoming Alumni Events", "Industry News", "Success Stories"]},
                {"footer": "Connect", "elements": ["LinkedIn", "Social Links", "Alumni Directory"]}
            ]
        },
        {
            "name": "College Admin Dashboard",
            "sections": [
                {"header": "Admin Navigation", "elements": ["Logo", "Dashboard", "Students", "Certificates", "Notifications", "Analytics", "Settings"]},
                {"sidebar": "Admin Panel", "elements": ["Student Management", "Certificate Approvals", "Create Notifications", "View Reports", "System Settings", "User Management"]},
                {"main_content": "Admin Overview", "widgets": ["Pending Approvals", "Student Statistics", "Certificate Requests", "System Alerts", "Quick Actions", "Recent Activities"]},
                {"footer": "Admin Tools", "elements": ["Documentation", "Support", "System Status"]}
            ]
        },
        {
            "name": "Organization Dashboard",
            "sections": [
                {"header": "Org Navigation", "elements": ["Logo", "Dashboard", "Recruitment", "Events", "Verification", "Collaborations", "Profile"]},
                {"sidebar": "Organization Menu", "elements": ["Job Postings", "Event Management", "Certificate Verification", "University Partnerships", "Analytics", "Settings"]},
                {"main_content": "Organization Hub", "widgets": ["Active Job Posts", "Upcoming Events", "Verification Requests", "Partnership Opportunities", "Performance Metrics", "Recent Applications"]},
                {"footer": "Organization Info", "elements": ["About Us", "Contact", "Terms of Service"]}
            ]
        }
    ]
}

# Prepare data for stacked horizontal bar chart
chart_data = []
colors = ['#1FB8CD', '#DB4545', '#2E8B57', '#5D878F']
section_colors = {
    'header': '#1FB8CD',
    'sidebar': '#DB4545', 
    'main_content': '#2E8B57',
    'footer': '#5D878F'
}

# Create traces for each section type
section_types = ['header', 'sidebar', 'main_content', 'footer']
section_names = {
    'header': 'Header',
    'sidebar': 'Sidebar', 
    'main_content': 'Main Content',
    'footer': 'Footer'
}

dashboards = []
header_counts = []
sidebar_counts = []
main_counts = []
footer_counts = []

for wireframe in data["wireframes"]:
    dashboard_name = wireframe["name"].replace(" Dashboard", "")
    dashboards.append(dashboard_name)
    
    # Initialize counts
    h_count = s_count = m_count = f_count = 0
    
    for section in wireframe["sections"]:
        section_key = list(section.keys())[0]
        elements_key = list(section.keys())[1]
        element_count = len(section[elements_key])
        
        if section_key == 'header':
            h_count = element_count
        elif section_key == 'sidebar':
            s_count = element_count
        elif section_key == 'main_content':
            m_count = element_count
        elif section_key == 'footer':
            f_count = element_count
    
    header_counts.append(h_count)
    sidebar_counts.append(s_count)
    main_counts.append(m_count)
    footer_counts.append(f_count)

# Create the stacked horizontal bar chart
fig = go.Figure()

# Add traces for each section type
fig.add_trace(go.Bar(
    name='Header',
    y=dashboards,
    x=header_counts,
    orientation='h',
    marker_color='#1FB8CD',
    hovertemplate='%{y}<br>Header: %{x} items<extra></extra>'
))

fig.add_trace(go.Bar(
    name='Sidebar',
    y=dashboards,
    x=sidebar_counts,
    orientation='h',
    marker_color='#DB4545',
    hovertemplate='%{y}<br>Sidebar: %{x} items<extra></extra>'
))

fig.add_trace(go.Bar(
    name='Main Content',
    y=dashboards,
    x=main_counts,
    orientation='h',
    marker_color='#2E8B57',
    hovertemplate='%{y}<br>Main Content: %{x} items<extra></extra>'
))

fig.add_trace(go.Bar(
    name='Footer',
    y=dashboards,
    x=footer_counts,
    orientation='h',
    marker_color='#5D878F',
    hovertemplate='%{y}<br>Footer: %{x} items<extra></extra>'
))

# Update layout
fig.update_layout(
    barmode='stack',
    title='Adhyayan Sathi UI Components by Section',
    xaxis_title='Component Count',
    yaxis_title='Dashboard Type',
    legend=dict(orientation='h', yanchor='bottom', y=1.05, xanchor='center', x=0.5)
)

# Update axes
fig.update_xaxes(showgrid=True, gridwidth=1, gridcolor='lightgray')
fig.update_yaxes(showgrid=False)

# Save the chart
fig.write_image("wireframe_structure.png")
fig.write_image("wireframe_structure.svg", format="svg")

fig.show()