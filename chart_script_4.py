import plotly.express as px
import pandas as pd

# Parse the technology stack data
tech_data = {
    "technology_stack": {
        "frontend": {
            "web": ["React.js", "Redux", "Material-UI", "Axios"],
            "mobile": ["React Native", "Flutter"],
            "tools": ["Webpack", "Babel", "ESLint"]
        },
        "backend": {
            "runtime": ["Node.js", "Express.js"],
            "apis": ["RESTful APIs", "GraphQL", "Socket.io"],
            "authentication": ["JWT", "OAuth 2.0", "Passport.js"]
        },
        "database": {
            "primary": ["PostgreSQL", "MongoDB"],
            "cache": ["Redis", "Memcached"],
            "search": ["Elasticsearch"]
        },
        "infrastructure": {
            "cloud": ["AWS", "Azure", "Google Cloud"],
            "containers": ["Docker", "Kubernetes"],
            "cdn": ["CloudFlare", "AWS CloudFront"]
        },
        "external_services": {
            "communication": ["SendGrid", "Twilio", "Firebase"],
            "payments": ["Stripe", "PayPal", "Razorpay"],
            "file_storage": ["AWS S3", "Google Drive API"]
        },
        "dev_tools": {
            "version_control": ["Git", "GitHub"],
            "ci_cd": ["Jenkins", "GitHub Actions"],
            "testing": ["Jest", "Cypress", "Postman"]
        },
        "monitoring": {
            "logging": ["Winston", "ELK Stack"],
            "monitoring": ["New Relic", "Datadog"],
            "security": ["Helmet.js", "SSL/TLS", "Rate Limiting"]
        }
    }
}

# Flatten the data for treemap
treemap_data = []

for category, subcategories in tech_data["technology_stack"].items():
    # Abbreviate category names to fit 15 char limit
    category_short = {
        "frontend": "Frontend",
        "backend": "Backend", 
        "database": "Database",
        "infrastructure": "Infrastructure",
        "external_services": "Ext Services",
        "dev_tools": "Dev Tools",
        "monitoring": "Monitoring"
    }.get(category, category)
    
    for subcat, technologies in subcategories.items():
        # Abbreviate subcategory names
        subcat_short = {
            "web": "Web",
            "mobile": "Mobile",
            "tools": "Tools",
            "runtime": "Runtime",
            "apis": "APIs", 
            "authentication": "Auth",
            "primary": "Primary DB",
            "cache": "Cache",
            "search": "Search",
            "cloud": "Cloud",
            "containers": "Containers",
            "cdn": "CDN",
            "communication": "Communication",
            "payments": "Payments",
            "file_storage": "File Storage",
            "version_control": "Version Ctrl",
            "ci_cd": "CI/CD",
            "testing": "Testing",
            "logging": "Logging",
            "monitoring": "Monitoring",
            "security": "Security"
        }.get(subcat, subcat)
        
        for tech in technologies:
            # Abbreviate technology names to fit 15 char limit
            tech_short = tech
            if len(tech) > 15:
                tech_short = {
                    "Material-UI": "Material-UI",
                    "React Native": "React Native",
                    "Express.js": "Express.js",
                    "RESTful APIs": "REST APIs",
                    "OAuth 2.0": "OAuth 2.0",
                    "Passport.js": "Passport.js",
                    "PostgreSQL": "PostgreSQL",
                    "Memcached": "Memcached",
                    "Elasticsearch": "Elasticsearch",
                    "Google Cloud": "Google Cloud",
                    "Kubernetes": "Kubernetes",
                    "CloudFlare": "CloudFlare",
                    "AWS CloudFront": "CloudFront",
                    "Google Drive API": "Drive API",
                    "GitHub Actions": "GH Actions",
                    "New Relic": "New Relic",
                    "Rate Limiting": "Rate Limit",
                    "SSL/TLS": "SSL/TLS"
                }.get(tech, tech[:15])
            
            treemap_data.append({
                "Layer": category_short,
                "Category": subcat_short,
                "Technology": tech_short,
                "Value": 1
            })

# Create DataFrame
df = pd.DataFrame(treemap_data)

# Create treemap
fig = px.treemap(
    df,
    path=['Layer', 'Category', 'Technology'],
    values='Value',
    title="Adhyayan Sathi Tech Stack Architecture",
    color_discrete_sequence=[
        '#1FB8CD', '#DB4545', '#2E8B57', '#5D878F', '#D2BA4C',
        '#B4413C', '#964325', '#944454', '#13343B', '#DB4545'
    ]
)

# Update layout
fig.update_layout(
    font=dict(size=12),
    uniformtext_minsize=10,
    uniformtext_mode='hide'
)

# Save the charts
fig.write_image("tech_stack_diagram.png")
fig.write_image("tech_stack_diagram.svg", format="svg")

fig.show()