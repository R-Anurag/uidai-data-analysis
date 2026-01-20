# UIDAI Analytics Dashboard

##  Overview
Comprehensive analytics dashboard for UIDAI enrollment data with automatic Jupyter notebook integration.

##  Key Features

- **Auto-Detection**: Automatically finds and loads all notebooks from base directory
- **Smart Rendering**: Only displays sections containing visualizations
- **Plot Selection**: Dropdown to select specific plots with descriptions
- **Team Integration**: All team members properly credited
- **Interactive**: Dynamic plot and section selection

##  Quick Start

```bash
# Navigate to project directory
cd /path_to_your_repo/uidai

# Run dashboard (notebooks auto-detected!)
streamlit run app/dashboard.py
```

Dashboard opens at: `http://localhost:8501`

##  Team Members

| Analyst | Analysis |
|---------|----------|
| **Paras** | Biometric Failure Analysis |
| **Sriyansh Sharma** | Resource Allocation Optimization |
| **Anurag Rai** | Fraud Detection |
| **Shivansh Bhageria** | Rural vs Urban Adoption |
| **Kartikeya Gupta** | District-level Hotspots |

##  Analysis Features

### 1. Biometric Failure Analysis
- Failure pattern detection
- Age group analysis
- Geographic distribution
- Temporal trends

### 2. Resource Allocation Optimization
- Demand forecasting
- Resource distribution analysis
- Efficiency metrics

### 3. Fraud Detection
- Anomaly detection
- Pattern recognition
- Risk scoring

### 4. Rural vs Urban Adoption
- Comparative analysis
- Adoption trends
- Demographic insights

### 5. District-level Hotspots
- Geographic anomalies
- Performance metrics
- Hotspot identification

##  How It Works

1. **Auto-Detection**: Dashboard scans base directory for notebooks
2. **Section Parsing**: Extracts sections containing plots
3. **Smart Display**: Shows only relevant sections with visualizations
4. **Plot Selection**: Dropdown to choose specific plots
5. **Description**: Displays markdown text following each plot

##  Usage

1. **Select Feature** from sidebar dropdown
2. **Choose Section** containing the analysis you want
3. **Select Plot** from available visualizations
4. **Read Description** below the plot

##  Installation

```bash
# Install dependencies
pip install streamlit pandas plotly numpy jupyter

# Run dashboard
streamlit run enhanced_streamlit_dashboard.py
```

##  Data Schema

### Biometric Data
- `date`, `state`, `district`, `pincode`
- `bio_age_5_17`: Biometric enrollments (age 5-17)
- `bio_age_17_`: Biometric enrollments (age 17+)

### Demographic Data
- `date`, `state`, `district`, `pincode`
- `demo_age_5_17`: Demographic enrollments (age 5-17)
- `demo_age_17_`: Demographic enrollments (age 17+)

### Enrollment Data
- `date`, `state`, `district`, `pincode`
- `age_0_5`, `age_5_17`, `age_18_greater`: Age-wise enrollments

##  Dashboard Features

- **Dashboard Overview**: Key metrics and quick insights
- **Auto-Loading**: No manual file uploads needed
- **Plot Dropdown**: Select specific visualizations
- **Section Navigation**: Jump to relevant analysis sections
- **Team Credits**: All analysts properly acknowledged

##  Notes

- Place all `.ipynb` files in the analysys_notebooks directory
- Dashboard automatically detects and loads them
- Only sections with plots are displayed
- Descriptions follow each visualization

##  Support

For issues or questions, contact the team members listed above.

##  License

MIT License

---

**Built with  by the UIDAI Analytics Team**
