import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

# Security architecture data
security_data = {
    "security_layers": {
        "perimeter_security": {
            "components": ["Web Application Firewall (WAF)", "DDoS Protection", "Rate Limiting", "IP Whitelisting"],
            "description": "First line of defense against external threats"
        },
        "authentication_layer": {
            "components": ["Multi-Factor Authentication (2FA)", "JWT Tokens", "OAuth 2.0", "Social Login Integration", "Password Policies"],
            "description": "User identity verification and access management"
        },
        "authorization_layer": {
            "components": ["Role-Based Access Control (RBAC)", "Permission Management", "API Access Control", "Resource-level Permissions"],
            "description": "Controlling what authenticated users can access"
        },
        "application_security": {
            "components": ["Input Validation", "SQL Injection Protection", "XSS Prevention", "CSRF Protection", "Secure Headers"],
            "description": "Protecting against application-level attacks"
        },
        "data_protection": {
            "components": ["Encryption at Rest (AES-256)", "Encryption in Transit (TLS 1.3)", "Data Masking", "Secure Key Management", "Database Security"],
            "description": "Protecting sensitive data and privacy"
        },
        "infrastructure_security": {
            "components": ["VPC Network Isolation", "Security Groups", "Container Security", "Regular Security Updates", "Backup Encryption"],
            "description": "Securing the underlying infrastructure"
        },
        "monitoring_compliance": {
            "components": ["Security Logs", "Audit Trail", "GDPR Compliance", "Data Privacy Controls", "Incident Response Plan", "Regular Security Audits"],
            "description": "Continuous monitoring and regulatory compliance"
        }
    }
}

# Prepare data for horizontal bar chart
layers = []
components = []
component_counts = []
colors_list = []

# Brand colors
brand_colors = ["#1FB8CD", "#DB4545", "#2E8B57", "#5D878F", "#D2BA4C", "#B4413C", "#964325"]

# Layer name mappings (abbreviated to fit 15 char limit)
layer_names = {
    "perimeter_security": "Perimeter Sec",
    "authentication_layer": "Authentication", 
    "authorization_layer": "Authorization",
    "application_security": "App Security",
    "data_protection": "Data Protect",
    "infrastructure_security": "Infrastructure",
    "monitoring_compliance": "Monitor & Comp"
}

# Component abbreviations
component_abbrevs = {
    "Web Application Firewall (WAF)": "WAF",
    "DDoS Protection": "DDoS",
    "Rate Limiting": "Rate Limit",
    "IP Whitelisting": "IP Whitelist",
    "Multi-Factor Authentication (2FA)": "2FA", 
    "JWT Tokens": "JWT",
    "OAuth 2.0": "OAuth 2.0",
    "Social Login Integration": "Social Login",
    "Password Policies": "Password Pol",
    "Role-Based Access Control (RBAC)": "RBAC",
    "Permission Management": "Permissions",
    "API Access Control": "API Control", 
    "Resource-level Permissions": "Resource Perm",
    "Input Validation": "Input Valid",
    "SQL Injection Protection": "SQL Protect",
    "XSS Prevention": "XSS Prevent",
    "CSRF Protection": "CSRF",
    "Secure Headers": "Sec Headers",
    "Encryption at Rest (AES-256)": "Encrypt Rest",
    "Encryption in Transit (TLS 1.3)": "Encrypt Trans", 
    "Data Masking": "Data Mask",
    "Secure Key Management": "Key Mgmt",
    "Database Security": "DB Security",
    "VPC Network Isolation": "VPC Network",
    "Security Groups": "Sec Groups",
    "Container Security": "Container Sec",
    "Regular Security Updates": "Sec Updates",
    "Backup Encryption": "Backup Enc",
    "Security Logs": "Sec Logs",
    "Audit Trail": "Audit Trail", 
    "GDPR Compliance": "GDPR",
    "Data Privacy Controls": "Privacy Ctrl",
    "Incident Response Plan": "Incident Resp",
    "Regular Security Audits": "Sec Audits"
}

# Create data for each component across layers
fig = go.Figure()

color_idx = 0
layer_order = ["perimeter_security", "authentication_layer", "authorization_layer", 
               "application_security", "data_protection", "infrastructure_security", 
               "monitoring_compliance"]

y_positions = []
layer_labels = []

for i, layer_key in enumerate(layer_order):
    layer_data = security_data["security_layers"][layer_key]
    layer_name = layer_names[layer_key]
    layer_labels.append(layer_name)
    y_positions.append(i)
    
    # Add components as separate bars for this layer
    x_offset = 0
    for j, component in enumerate(layer_data["components"]):
        component_abbrev = component_abbrevs.get(component, component[:14])
        
        fig.add_trace(go.Bar(
            x=[1],
            y=[i],
            orientation='h',
            name=component_abbrev,
            marker_color=brand_colors[color_idx % len(brand_colors)],
            text=component_abbrev,
            textposition='inside',
            textfont=dict(size=10),
            hovertemplate=f'<b>{component_abbrev}</b><br>Layer: {layer_name}<extra></extra>',
            offsetgroup=j,
            base=x_offset,
            showlegend=False
        ))
        x_offset += 1
        color_idx += 1

# Update layout
fig.update_layout(
    title="Security Architecture Layers",
    xaxis_title="Components",
    yaxis_title="Security Layers",
    barmode='stack',
    yaxis=dict(
        tickmode='array',
        tickvals=y_positions,
        ticktext=layer_labels
    ),
    xaxis=dict(showticklabels=False),
    showlegend=False
)

fig.update_traces(cliponaxis=False)

# Save as PNG and SVG
fig.write_image("security_architecture.png")
fig.write_image("security_architecture.svg", format="svg")

fig.show()