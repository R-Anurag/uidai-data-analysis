import streamlit as st
import json
import os
import re
import base64
from datetime import date
import glob
import io
from PIL import Image
import streamlit.components.v1 as components


st.set_page_config(
    page_title="UIDAI Analytics Dashboard",
    page_icon="app/UIDAI_logo.png",
    layout="wide"
)


import base64

def load_font(path):
    with open(path, "rb") as f:
        data = f.read()
    return base64.b64encode(data).decode()

font_base64 = load_font("fonts/Poppins/Poppins-Light.ttf")
font_hindi_base64 = load_font("fonts/Poppins/Poppins-Medium.ttf")

def load_svg_base64(path):
    with open(path, "rb") as f:
        data = f.read()
    return base64.b64encode(data).decode()

svg_base64 = load_svg_base64("app/UIDAI_logo.svg")

st.markdown(f"""
<style>
@font-face {{
    font-family: "CustomFont";
    src: url(data:font/ttf;base64,{font_base64});
}}

@font-face {{
    font-family: "HindiFont";
    src: url(data:font/ttf;base64,{font_hindi_base64});
}}

/* Apply only to text elements */
p, div, h1, h2, h3, h4, h5, h6, label, li, a {{
    font-family: "CustomFont", sans-serif !important;
}}
</style>
""", unsafe_allow_html=True)




# ---------------- BACKGROUND + OVERLAY ---------------- #
def set_bg(image_file):
    with open(image_file, "rb") as f:
        data = f.read()
    encoded = base64.b64encode(data).decode()

    st.markdown(
        f"""
        <style>
        .stApp {{
            background-image: url("data:image/png;base64,{encoded}");
            background-size: cover;
            background-position: center;
            background-repeat: no-repeat;
        }}

        /* Default overlay (light mode) */
        .stApp:before {{
            content: "";
            position: fixed;
            inset: 0;
            background: rgba(0,0,0,0.45);
            z-index: -1;
        }}

        /* Dark mode override */
        @media (prefers-color-scheme: dark) {{
            .stApp:before {{
                background: rgba(0,0,0,0.65);
            }}
        }}

        /* Make content readable */
        .block-container {{
            background: rgba(255,255,255,0.90);
            padding: 2rem;
            border-radius: 16px;
        }}

        /* Dark mode content card */
        @media (prefers-color-scheme: dark) {{
            .block-container {{
                background: rgba(20,20,20,0.85);
            }}
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

set_bg("app/background2.jpg")
# ------------------------------------------------------ #

st.markdown("""
<style>
img {
    border: 3px solid gray !important;
    border-radius: 12px !important;
    padding: 6px !important;
    background: white !important;
}
</style>
""", unsafe_allow_html=True)

st.markdown("""
<style>
.uidai-logo {
    display: block;
    margin: auto;
    width: 120px;
    background: transparent !important;
    border: none !important;
    padding: 0 !important;
}
.hindi-headline{
    font-family: "HindiFont", sans-serif !important;     
    margin-bottom: 2rem !important;  
}
</style>
""", unsafe_allow_html=True)



st.markdown("""
<style>
    .notebook-header {color: #1f77b4; text-align: center;}
</style>
""", unsafe_allow_html=True)

# Notebook mapping with descriptions
NOTEBOOK_MAP = {
    "biometric_failure_analysis.ipynb": {
        "name": "Biometric Failure Analysis", 
        "analyst": "Paras",
        "description": "Analyzes biometric capture failures across different demographics, geographic regions, and time periods. Identifies patterns in authentication failures and equipment-related issues to improve enrollment success rates."
    },
    "Resource_Allocation_Optimization.ipynb": {
        "name": "Resource Allocation Optimization", 
        "analyst": "Sriyansh Sharma",
        "description": "Optimizes resource distribution by analyzing enrollment demand patterns across states and districts. Provides insights into population distribution, monthly enrollment rates, and seasonal trends to guide infrastructure planning."
    },
    "fraud_detection_analysis.ipynb": {
        "name": "Fraud Detection", 
        "analyst": "Anurag Rai",
        "description": "Identifies potential fraud patterns and anomalies in enrollment data through advanced statistical analysis. Detects unusual spikes, demographic mismatches, and suspicious enrollment patterns to ensure data integrity."
    },
    "Rural_Urban_Adoption_Analysis.ipynb": {
        "name": "Rural vs Urban Adoption", 
        "analyst": "Shivansh Bhageria",
        "description": "Compares Aadhaar enrollment patterns between rural and urban areas to understand the digital divide. Analyzes demographic trends, biometric authentication rates, and time-series patterns to assess adoption disparities."
    },
    "district_anomaly_detection.ipynb": {
        "name": "District-level Hotspots", 
        "analyst": "Kartikeya Gupta",
        "description": "Identifies geographic hotspots with unusual enrollment patterns at the district level. Detects anomalies in enrollment ratios and provides descriptive statistics to highlight areas requiring policy intervention."
    }
}

def find_notebooks():
    """Auto-detect notebooks in base directory"""
    notebooks = {}
    for filename, info in NOTEBOOK_MAP.items():
        if os.path.exists(f'analysis_notebooks/{filename}'):
            notebooks[info["name"]] = {
                "file": f'analysis_notebooks/{filename}', 
                "analyst": info["analyst"],
                "description": info["description"]
            }
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
                                if 'image/png' in plot_data:
                                    current_section['plots'].append(plot_data)
        
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
            if isinstance(img_data, str):
                img_bytes = base64.b64decode(img_data)
                img = Image.open(io.BytesIO(img_bytes))
                st.image(img, use_container_width=True)
            elif isinstance(img_data, bytes):
                st.image(img_data, use_container_width=True)
            else:
                st.error(f"Unexpected image data type: {type(img_data)}")
    except Exception as e:
        st.error(f"Error rendering plot: {e}")
        import traceback
        st.code(traceback.format_exc())


st.sidebar.title("Analytics Menu")
st.sidebar.markdown("---")

available_notebooks = find_notebooks()

if not available_notebooks:
    st.error("No notebooks found! Please ensure .ipynb files are in the base directory.")
    st.stop()

features = ["Dashboard Overview"] + list(available_notebooks.keys())
feature = st.sidebar.selectbox("Select Analysis Feature:", features)

# Dashboard Overview
if feature == "Dashboard Overview":
    st.markdown(
        f"""
        <div style="text-align:center;">
            <img src="data:image/svg+xml;base64,{svg_base64}" class="uidai-logo">
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        """
        <h2 class="notebook-header" style="text-align:center;">
            UIDAI-Data Analytics Dashboard
        </h2>
        <p class="hindi-headline" style="text-align:center; font-size:2rem; color:gray; margin-top:-8px;">
            डेटा में अवसर, समाधान में क्रांति
        </p>
        """,
        unsafe_allow_html=True
    )

    # --- Metrics Section ---

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Enrollments", "12.5M", "2.3% ↑")
    with col2:
        st.metric("Success Rate", "94.2%", "1.1% ↑")
    with col3:
        st.metric("Active Districts", "742", "5 ↑")
    with col4:
        st.metric("Biometric Quality", "96.8%", "0.5% ↑")

    # --- Insights ---

    st.markdown("### Quick Insights")
    col1, col2 = st.columns(2)
    with col1:
        st.info("**Enrollment Trend**: 15% increase in rural areas")
        st.success("**Top Performer**: Maharashtra with 98.5% success rate")
    with col2:
        st.warning("**Alert**: Biometric failures increased in 3 districts")
        st.error("**Action Required**: Fraud patterns detected in 2 regions")

else:
    notebook_info = available_notebooks[feature]
    st.markdown(f'<h2 class="notebook-header"> {feature}</h2>', unsafe_allow_html=True)
    st.markdown(f"**Analyst: {notebook_info['analyst']}**")
    
    if 'description' in notebook_info:
        st.info(f"**About this analysis:** {notebook_info['description']}")
    
    sections = parse_notebook(notebook_info['file'])
    
    if not sections:
        st.warning("No sections with plots found in this notebook.")
    else:
        section_names = [s['heading'] for s in sections]
        selected_section = st.selectbox("Select Section:", section_names)
        
        section = next(s for s in sections if s['heading'] == selected_section)
        
        if section['plots']:
            st.markdown("### Visualization")
            render_plot(section['plots'][0])
            
            st.markdown("### Description")
            st.markdown(section['text'])
        else:
            st.info("No plots available in this section.")

# Footer
st.markdown("---")
st.markdown("<div style='text-align: center; color: #666666;'><p>UIDAI Analytics Dashboard | Built with Streamlit</p></div>", unsafe_allow_html=True)

# Sidebar team info
st.sidebar.markdown("---")
st.sidebar.markdown("### Team Members")
st.sidebar.markdown("""
- **Paras** - Biometric Failure Analysis
- **Sriyansh Sharma** - Resource Allocation
- **Anurag Rai** - Fraud Detection
- **Shivansh Bhageria** - Rural/Urban Analysis
- **Kartikeya Gupta** - District Hotspots
""")

st.sidebar.markdown("### Available Analyses")
for name, info in available_notebooks.items():
    st.sidebar.success(f"{name}")
