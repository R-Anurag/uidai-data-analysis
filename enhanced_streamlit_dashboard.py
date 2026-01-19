import streamlit as st
import json
import os
import re
import base64
from datetime import date
import glob
import io
from PIL import Image

st.set_page_config(page_title="UIDAI Analytics Dashboard", page_icon="🆔", layout="wide")

st.markdown("""
<style>
    .main-header {font-size: 2.5rem; font-weight: bold; color: #1f77b4; text-align: center; margin-bottom: 2rem;}
</style>
""", unsafe_allow_html=True)

# Notebook mapping with descriptions
NOTEBOOK_MAP = {
    "biometric_failure_analysis.ipynb": {
        "name": "🔍 Biometric Failure Analysis", 
        "analyst": "Paras",
        "description": "Analyzes biometric capture failures across different demographics, geographic regions, and time periods. Identifies patterns in authentication failures and equipment-related issues to improve enrollment success rates."
    },
    "Resource_Allocation_Optimization_with_descriptions.ipynb": {
        "name": "📈 Resource Allocation Optimization", 
        "analyst": "Sriyansh Sharma",
        "description": "Optimizes resource distribution by analyzing enrollment demand patterns across states and districts. Provides insights into population distribution, monthly enrollment rates, and seasonal trends to guide infrastructure planning."
    },
    "fraud_detection_analysis.ipynb": {
        "name": "🚨 Fraud Detection", 
        "analyst": "Anurag Rai",
        "description": "Identifies potential fraud patterns and anomalies in enrollment data through advanced statistical analysis. Detects unusual spikes, demographic mismatches, and suspicious enrollment patterns to ensure data integrity."
    },
    "Rural_Urban_Adoption_Analysis.ipynb": {
        "name": "🏘️ Rural vs Urban Adoption", 
        "analyst": "Shivansh Bhageria",
        "description": "Compares Aadhaar enrollment patterns between rural and urban areas to understand the digital divide. Analyzes demographic trends, biometric authentication rates, and time-series patterns to assess adoption disparities."
    },
    "district_anomaly_detection_with_descriptions.ipynb": {
        "name": "📍 District-level Hotspots", 
        "analyst": "Kartikeya Gupta",
        "description": "Identifies geographic hotspots with unusual enrollment patterns at the district level. Detects anomalies in enrollment ratios and provides descriptive statistics to highlight areas requiring policy intervention."
    }
}

def find_notebooks():
    """Auto-detect notebooks in base directory"""
    notebooks = {}
    for filename, info in NOTEBOOK_MAP.items():
        if os.path.exists(filename):
            notebooks[info["name"]] = {"file": filename, "analyst": info["analyst"]}
    return notebooks

def parse_notebook(notebook_path):
    """Parse notebook and extract sections with visual plots (images only, no tables)"""
    try:
        with open(notebook_path, 'r', encoding='utf-8') as f:
            nb = json.load(f)
        
        sections = []
        current_section = None
        
        for cell in nb.get('cells', []):
            if cell['cell_type'] == 'markdown':
                content = ''.join(cell['source'])
                headings = re.findall(r'^#+\s+(.+)$', content, re.MULTILINE)
                if headings:
                    if current_section and current_section['plots']:
                        sections.append(current_section)
                    current_section = {'heading': headings[0], 'plots': [], 'text': content}
                elif current_section:
                    current_section['text'] += '\n' + content
            
            elif cell['cell_type'] == 'code' and current_section:
                if 'outputs' in cell:
                    for output in cell['outputs']:
                        if output.get('output_type') in ['display_data', 'execute_result']:
                            if 'data' in output:
                                plot_data = output['data']
                                # Only include PNG images (actual visual plots), skip HTML tables
                                if 'image/png' in plot_data:
                                    current_section['plots'].append(plot_data)
                                # Skip text/html as they are usually tables/dataframes
        
        if current_section and current_section['plots']:
            sections.append(current_section)
        
        return sections
    except Exception as e:
        st.error(f"Error parsing notebook: {e}")
        return []

def render_plot(plot_data):
    """Render a single plot (PNG images only)"""
    try:
        if 'image/png' in plot_data:
            img_data = plot_data['image/png']
            # Handle both base64 string and bytes
            if isinstance(img_data, str):
                # Already base64 encoded string
                img_bytes = base64.b64decode(img_data)
                img = Image.open(io.BytesIO(img_bytes))
                st.image(img, use_container_width=True)
            elif isinstance(img_data, bytes):
                # Already decoded bytes
                st.image(img_data, use_container_width=True)
            else:
                st.error(f"Unexpected image data type: {type(img_data)}")
    except Exception as e:
        st.error(f"Error rendering plot: {e}")
        # Show more detailed error info
        import traceback
        st.code(traceback.format_exc())

# Main UI
st.markdown('<h1 class="main-header">🆔 UIDAI Analytics Dashboard</h1>', unsafe_allow_html=True)

st.sidebar.title("📊 Analytics Menu")
st.sidebar.markdown("---")

# Auto-detect notebooks
available_notebooks = find_notebooks()

if not available_notebooks:
    st.error("No notebooks found! Please ensure .ipynb files are in the base directory.")
    st.stop()

# Feature selection
features = ["🏠 Dashboard Overview"] + list(available_notebooks.keys())
feature = st.sidebar.selectbox("Select Analysis Feature:", features)

# st.sidebar.markdown("### 🔧 Common Filters")
# date_range = st.sidebar.date_input("Select Date Range:", value=(date(2025, 1, 1), date(2025, 12, 31)))
# states = st.sidebar.multiselect("Select States:", ["All States", "Uttar Pradesh", "Maharashtra", "Bihar", "West Bengal"], default=["All States"])

# Dashboard Overview
if feature == "🏠 Dashboard Overview":
    st.markdown("## 📊 Dashboard Overview")
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Enrollments", "12.5M", "2.3% ↑")
    with col2:
        st.metric("Success Rate", "94.2%", "1.1% ↑")
    with col3:
        st.metric("Active Districts", "742", "5 ↑")
    with col4:
        st.metric("Biometric Quality", "96.8%", "0.5% ↑")
    
    st.markdown("### 🎯 Quick Insights")
    col1, col2 = st.columns(2)
    with col1:
        st.info("📈 **Enrollment Trend**: 15% increase in rural areas")
        st.success("✅ **Top Performer**: Maharashtra with 98.5% success rate")
    with col2:
        st.warning("⚠️ **Alert**: Biometric failures increased in 3 districts")
        st.error("🚨 **Action Required**: Fraud patterns detected in 2 regions")

# Notebook Analysis
else:
    notebook_info = available_notebooks[feature]
    st.markdown(f"## {feature}")
    st.markdown(f"**Analyst: {notebook_info['analyst']}**")
    
    # Display analysis description
    if 'description' in notebook_info:
        st.info(f"📝 **About this analysis:** {notebook_info['description']}")
    
    sections = parse_notebook(notebook_info['file'])
    
    if not sections:
        st.warning("No sections with plots found in this notebook.")
    else:
        # Section selector
        section_names = [s['heading'] for s in sections]
        selected_section = st.selectbox("📋 Select Section:", section_names)
        
        # Find selected section
        section = next(s for s in sections if s['heading'] == selected_section)
        

# Footer
st.markdown("---")
st.markdown("<div style='text-align: center; color: #666666;'><p>🆔 UIDAI Analytics Dashboard | Built with Streamlit</p></div>", unsafe_allow_html=True)

# Sidebar team info
st.sidebar.markdown("---")
st.sidebar.markdown("### 👥 Team Members")
st.sidebar.markdown("""
- **Paras** - Biometric Failure Analysis
- **Sriyansh Sharma** - Resource Allocation
- **Anurag Rai** - Fraud Detection
- **Shivansh Bhageria** - Rural/Urban Analysis
- **Shivansh Bhageria** - Rural/Urban Analysis
- **Kartikeya Gupta** - District Hotspots
""")

st.sidebar.markdown("### 📊 Available Analyses")
for name, info in available_notebooks.items():
    st.sidebar.success(f"✅ {name}")
