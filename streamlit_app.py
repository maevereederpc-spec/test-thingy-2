import streamlit as st
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import numpy as np
from datetime import datetime
import io
import zipfile
import tempfile
import os

# Page configuration
st.set_page_config(
    page_title="Telemetry Analysis",
    page_icon="🏎️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for modern, sleek design with wine red accents
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;900&display=swap');
    
    /* Main theme */
    :root {
        --wine-red: #8B1538;
        --wine-red-light: #A01C3A;
        --wine-red-dark: #6B0F2A;
        --wine-red-glow: rgba(139, 21, 56, 0.3);
        --dark-bg: #0A0A0A;
        --card-bg: #141414;
        --border-color: #2A2A2A;
        --text-primary: #FFFFFF;
        --text-secondary: #B0B0B0;
    }
    
    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Main container */
    .stApp {
        background: linear-gradient(135deg, #0A0A0A 0%, #1A0A0F 100%);
        font-family: 'Inter', sans-serif;
    }
    
    /* Headers */
    h1 {
        font-family: 'Inter', sans-serif;
        font-weight: 900;
        color: var(--text-primary);
        text-transform: uppercase;
        letter-spacing: 2px;
        margin-bottom: 0.5rem;
        text-shadow: 0 0 20px var(--wine-red-glow);
    }
    
    h2, h3 {
        font-family: 'Inter', sans-serif;
        color: var(--wine-red-light);
        font-weight: 700;
        letter-spacing: 1px;
        text-transform: uppercase;
        margin-top: 2rem;
    }
    
    /* Sidebar */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, var(--dark-bg) 0%, #1A0A0F 100%);
        border-right: 2px solid var(--wine-red-dark);
    }
    
    [data-testid="stSidebar"] h1, 
    [data-testid="stSidebar"] h2, 
    [data-testid="stSidebar"] h3 {
        color: var(--wine-red-light);
    }
    
    /* Metrics */
    [data-testid="stMetricValue"] {
        font-family: 'Inter', sans-serif;
        font-size: 2rem;
        font-weight: 700;
        color: var(--wine-red-light);
    }
    
    [data-testid="stMetricLabel"] {
        font-family: 'Inter', sans-serif;
        font-size: 0.9rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 1px;
        color: var(--text-secondary);
    }
    
    /* Cards/Containers */
    .element-container {
        background: var(--card-bg);
        border: 1px solid var(--border-color);
        border-radius: 8px;
        padding: 1rem;
        margin: 0.5rem 0;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.3);
    }
    
    /* Buttons */
    .stButton button {
        background: linear-gradient(135deg, var(--wine-red) 0%, var(--wine-red-dark) 100%);
        color: white;
        border: none;
        border-radius: 4px;
        padding: 0.75rem 2rem;
        font-family: 'Inter', sans-serif;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 1px;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px var(--wine-red-glow);
    }
    
    .stButton button:hover {
        background: linear-gradient(135deg, var(--wine-red-light) 0%, var(--wine-red) 100%);
        box-shadow: 0 6px 20px var(--wine-red-glow);
        transform: translateY(-2px);
    }
    
    /* File uploader */
    [data-testid="stFileUploader"] {
        background: var(--card-bg);
        border: 2px dashed var(--wine-red-dark);
        border-radius: 8px;
        padding: 2rem;
    }
    
    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background: var(--card-bg);
        border-radius: 8px;
        padding: 0.5rem;
    }
    
    .stTabs [data-baseweb="tab"] {
        font-family: 'Inter', sans-serif;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 1px;
        background: transparent;
        border: 1px solid var(--border-color);
        border-radius: 4px;
        color: var(--text-secondary);
        padding: 0.75rem 1.5rem;
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, var(--wine-red) 0%, var(--wine-red-dark) 100%);
        color: white;
        border-color: var(--wine-red);
    }
    
    /* Selectbox and inputs */
    .stSelectbox, .stMultiSelect {
        font-family: 'Inter', sans-serif;
    }
    
    /* Dataframe */
    [data-testid="stDataFrame"] {
        background: var(--card-bg);
        border: 1px solid var(--border-color);
        border-radius: 8px;
    }
    
    /* Info boxes */
    .stAlert {
        background: var(--card-bg);
        border-left: 4px solid var(--wine-red);
        font-family: 'Inter', sans-serif;
    }
    
    /* Custom stat card */
    .stat-card {
        background: linear-gradient(135deg, var(--card-bg) 0%, #1A1A1A 100%);
        border: 1px solid var(--wine-red-dark);
        border-radius: 8px;
        padding: 1.5rem;
        text-align: center;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.5);
        transition: all 0.3s ease;
    }
    
    .stat-card:hover {
        transform: translateY(-4px);
        box-shadow: 0 8px 25px var(--wine-red-glow);
        border-color: var(--wine-red);
    }
    
    .stat-value {
        font-family: 'Inter', sans-serif;
        font-size: 2.5rem;
        font-weight: 900;
        color: var(--wine-red-light);
        text-shadow: 0 0 10px var(--wine-red-glow);
    }
    
    .stat-label {
        font-family: 'Inter', sans-serif;
        font-size: 0.9rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 2px;
        color: var(--text-secondary);
        margin-top: 0.5rem;
    }
</style>
""", unsafe_allow_html=True)

# Plotly theme for wine red accents
def get_plotly_layout(**kwargs):
    """Get plotly layout with wine red theme"""
    layout = {
        'paper_bgcolor': '#0A0A0A',
        'plot_bgcolor': '#141414',
        'font': {'color': '#FFFFFF', 'family': 'Inter'},
        'xaxis': {
            'gridcolor': '#2A2A2A',
            'zerolinecolor': '#2A2A2A',
            'color': '#B0B0B0'
        },
        'yaxis': {
            'gridcolor': '#2A2A2A',
            'zerolinecolor': '#2A2A2A',
            'color': '#B0B0B0'
        },
        'colorway': ['#8B1538', '#A01C3A', '#FF6B8A', '#FF9BB5', '#4A90E2', '#50C878']
    }
    
    # Add title styling if title is provided
    if 'title' in kwargs:
        layout['title'] = {
            'text': kwargs['title'],
            'font': {'family': 'Inter', 'size': 20, 'color': '#A01C3A'}
        }
        del kwargs['title']
    
    # Merge with any additional kwargs
    layout.update(kwargs)
    return layout

# Sample data generator for demo purposes
def generate_sample_data(num_laps=5):
    """Generate sample telemetry data for demonstration"""
    data_frames = []
    cumulative_time = 0.0
    
    for lap in range(1, num_laps + 1):
        # Generate distance points
        distance = np.linspace(0, 5000, 1000)  # 5km track
        
        # Generate realistic telemetry
        base_speed = 180 + np.random.randn() * 10
        speed = base_speed + 50 * np.sin(distance / 300) + np.random.randn(1000) * 5
        speed = np.clip(speed, 0, 320)
        
        throttle = np.clip((speed - 50) / 200, 0, 1) + np.random.randn(1000) * 0.05
        throttle = np.clip(throttle, 0, 1)
        
        brake = np.zeros(1000)
        brake_zones = [(200, 300), (800, 900), (1500, 1600), (2200, 2300), (3500, 3600), (4500, 4600)]
        for start, end in brake_zones:
            brake[int(start):int(end)] = 0.8 + np.random.randn() * 0.1
        brake = np.clip(brake, 0, 1)
        
        steering = 0.3 * np.sin(distance / 200) + np.random.randn(1000) * 0.1
        steering = np.clip(steering, -1, 1)
        
        # Tire temperatures
        tire_fl = 80 + 15 * (throttle + brake) + np.random.randn(1000) * 2
        tire_fr = 80 + 15 * (throttle + brake) + np.random.randn(1000) * 2
        tire_rl = 75 + 15 * (throttle + brake) + np.random.randn(1000) * 2
        tire_rr = 75 + 15 * (throttle + brake) + np.random.randn(1000) * 2
        
        gear = np.clip(np.floor(speed / 40) + 1, 1, 6).astype(int)
        
        # RPM
        rpm = speed * 50 + gear * 500 + np.random.randn(1000) * 100
        rpm = np.clip(rpm, 1000, 8500)
        
        # Time - make it continuous across laps
        dt = distance / (speed / 3.6)  # Convert km/h to m/s
        dt[0] = 0
        lap_time_increments = np.cumsum(np.diff(np.concatenate([[0], dt])))
        time = cumulative_time + lap_time_increments
        
        # Update cumulative time for next lap
        lap_time = time[-1] - cumulative_time
        cumulative_time = time[-1]
        
        df = pd.DataFrame({
            'Lap': lap,
            'Distance': distance,
            'Time': time,
            'Speed': speed,
            'Throttle': throttle,
            'Brake': brake,
            'Steering': steering,
            'Gear': gear,
            'RPM': rpm,
            'TireFL': tire_fl,
            'TireFR': tire_fr,
            'TireRL': tire_rl,
            'TireRR': tire_rr,
            'LapTime': lap_time
        })
        
        data_frames.append(df)
    
    return pd.concat(data_frames, ignore_index=True)

def calculate_lap_times(df):
    """Calculate lap times from time differences between lap starts"""
    lap_times = {}
    
    # Check if Time column exists
    if 'Time' not in df.columns:
        # Try to fall back to LapTime column
        if 'LapTime' in df.columns:
            try:
                for lap in df['Lap'].unique():
                    lap_data = df[df['Lap'] == lap]
                    lap_time = pd.to_numeric(lap_data['LapTime'].iloc[0], errors='coerce')
                    if not pd.isna(lap_time):
                        lap_times[lap] = lap_time
            except:
                pass
        return lap_times
    
    try:
        # Get unique laps
        laps = sorted(df['Lap'].unique())
        
        for i, lap in enumerate(laps):
            # Get the first time value for this lap
            lap_start_time = df[df['Lap'] == lap]['Time'].min()
            
            # If there's a next lap, calculate time difference
            if i + 1 < len(laps):
                next_lap = laps[i + 1]
                next_lap_start_time = df[df['Lap'] == next_lap]['Time'].min()
                lap_time = next_lap_start_time - lap_start_time
            else:
                # For the last lap, use max time - min time of that lap
                lap_time = df[df['Lap'] == lap]['Time'].max() - lap_start_time
            
            lap_times[lap] = lap_time
    except Exception as e:
        # Fallback to LapTime column if available
        if 'LapTime' in df.columns:
            for lap in df['Lap'].unique():
                lap_data = df[df['Lap'] == lap]
                try:
                    lap_time = pd.to_numeric(lap_data['LapTime'].iloc[0], errors='coerce')
                    if not pd.isna(lap_time):
                        lap_times[lap] = lap_time
                except:
                    pass
    
    return lap_times

def parse_pytelemetry_csv(file_content):
    """Parse pyTelemetry/Telemetrick CSV format"""
    lines = file_content.decode('utf-8').split('\n')
    
    # Extract metadata from first 9 rows
    metadata = {}
    for i in range(min(9, len(lines))):
        if ',' in lines[i]:
            parts = lines[i].split(',', 1)
            if len(parts) == 2:
                key = parts[0].strip()
                value = parts[1].strip()
                metadata[key] = value
    
    # Find the header row (should be around line 19-20)
    header_row = None
    for i, line in enumerate(lines):
        if 'time,' in line.lower() and 'lap number' in line.lower():
            header_row = i
            break
    
    if header_row is None:
        return None, metadata
    
    # Read CSV starting from header row
    csv_content = '\n'.join(lines[header_row:])
    df = pd.read_csv(io.StringIO(csv_content))
    
    return df, metadata

def load_telemetry_data(uploaded_file):
    """Load telemetry data from uploaded file"""
    metadata = {}
    
    try:
        # Handle ZIP files
        if uploaded_file.name.endswith('.zip'):
            with zipfile.ZipFile(uploaded_file, 'r') as zip_ref:
                # Find CSV file in ZIP
                csv_files = [f for f in zip_ref.namelist() if f.endswith('.csv')]
                
                if not csv_files:
                    st.error("No CSV file found in ZIP archive.")
                    return None
                
                # Use first CSV file
                csv_filename = csv_files[0]
                st.info(f"📦 Extracting: {csv_filename}")
                
                with zip_ref.open(csv_filename) as csv_file:
                    file_content = csv_file.read()
                    
                    # Try to parse as pyTelemetry format
                    df, metadata = parse_pytelemetry_csv(file_content)
                    
                    if df is not None:
                        st.success("✅ Detected pyTelemetry/Telemetrick format!")
        
        elif uploaded_file.name.endswith('.csv'):
            # Read file content
            file_content = uploaded_file.read()
            uploaded_file.seek(0)  # Reset for potential re-reading
            
            # Check if it's pyTelemetry format
            first_line = file_content.decode('utf-8').split('\n')[0]
            if 'AC pyTelemetry CSV' in first_line or 'Format,' in first_line:
                df, metadata = parse_pytelemetry_csv(file_content)
                if df is not None:
                    st.success("✅ Detected pyTelemetry/Telemetrick format!")
            else:
                # Try standard CSV formats
                df = None
                errors = []
                
                # Strategy 1: Standard CSV read
                try:
                    uploaded_file.seek(0)
                    df = pd.read_csv(uploaded_file)
                except Exception as e1:
                    errors.append(f"Standard CSV: {str(e1)}")
                    
                    # Strategy 2: Try with different delimiter
                    try:
                        uploaded_file.seek(0)
                        df = pd.read_csv(uploaded_file, sep=None, engine='python')
                    except Exception as e2:
                        errors.append(f"Auto-delimiter: {str(e2)}")
                        
                        # Strategy 3: Try semicolon delimiter
                        try:
                            uploaded_file.seek(0)
                            df = pd.read_csv(uploaded_file, sep=';')
                        except Exception as e3:
                            errors.append(f"Semicolon delimiter: {str(e3)}")
                            
                            # Strategy 4: Try tab delimiter
                            try:
                                uploaded_file.seek(0)
                                df = pd.read_csv(uploaded_file, sep='\t')
                            except Exception as e4:
                                errors.append(f"Tab delimiter: {str(e4)}")
                                
                                # Strategy 5: Skip bad lines
                                try:
                                    uploaded_file.seek(0)
                                    df = pd.read_csv(uploaded_file, on_bad_lines='skip')
                                    st.warning("⚠️ Some lines in the CSV were skipped due to formatting issues.")
                                except Exception as e5:
                                    errors.append(f"Skip bad lines: {str(e5)}")
                
                if df is None:
                    st.error("❌ Could not parse CSV file. Errors encountered:")
                    for i, err in enumerate(errors, 1):
                        st.text(f"{i}. {err}")
                    st.info("💡 **Tip:** Ensure your CSV has:\n- A header row with column names\n- Consistent number of columns in each row\n- Proper comma separation")
                    return None
                    
        elif uploaded_file.name.endswith(('.xls', '.xlsx')):
            try:
                df = pd.read_excel(uploaded_file)
            except Exception as e:
                st.error(f"Error reading Excel file: {str(e)}")
                return None
        else:
            st.error("Unsupported file format. Please upload CSV, Excel, or ZIP files.")
            return None
        
        if df is None:
            return None
        
        # Display metadata if available
        if metadata:
            with st.expander("📋 Session Metadata", expanded=False):
                col1, col2 = st.columns(2)
                with col1:
                    if 'Driver' in metadata:
                        st.info(f"**Driver:** {metadata['Driver']}")
                    if 'Vehicle' in metadata:
                        st.info(f"**Vehicle:** {metadata['Vehicle']}")
                    if 'Venue' in metadata:
                        st.info(f"**Track:** {metadata['Venue']}")
                with col2:
                    if 'Log Date' in metadata:
                        st.info(f"**Date:** {metadata['Log Date']}")
                    if 'Log Time' in metadata:
                        st.info(f"**Time:** {metadata['Log Time']}")
                    if 'Sample Rate' in metadata:
                        st.info(f"**Sample Rate:** {metadata['Sample Rate']} Hz")
        
        # Clean column names (remove whitespace and normalize)
        df.columns = df.columns.str.strip()
        
        # Map pyTelemetry columns to expected format
        column_mapping = {
            'Lap Number': 'Lap',
            'Lap Distance': 'Distance',
            'Ground Speed': 'Speed',
            'Throttle Pos': 'Throttle',
            'Brake Pos': 'Brake',
            'Steering Angle': 'Steering',
            'Engine RPM': 'RPM',
            'Tire Temp Core FL': 'TireFL',
            'Tire Temp Core FR': 'TireFR',
            'Tire Temp Core RL': 'TireRL',
            'Tire Temp Core RR': 'TireRR',
            'Lap Time': 'LapTime',
            'time': 'Time'
        }
        
        # Apply column mapping
        for old_name, new_name in column_mapping.items():
            if old_name in df.columns:
                df = df.rename(columns={old_name: new_name})
                st.info(f"🔄 Mapped '{old_name}' → '{new_name}'")
        
        # Try to map similar column names (case-insensitive)
        required_cols = ['Lap', 'Distance', 'Speed']
        missing_cols = [col for col in required_cols if col not in df.columns]
        
        if missing_cols:
            st.warning(f"⚠️ File missing required columns: {missing_cols}")
            
            for req_col in missing_cols:
                # Look for similar column names (case-insensitive)
                for col in df.columns:
                    if req_col.lower() in col.lower():
                        df = df.rename(columns={col: req_col})
                        st.info(f"🔄 Mapping '{col}' → '{req_col}'")
                        break
            
            missing_cols = [col for col in required_cols if col not in df.columns]
            
            if missing_cols:
                st.error(f"❌ Still missing required columns: {missing_cols}. Using sample data instead.")
                st.info("💡 **Required columns:** Lap (int), Distance (m), Speed (km/h)")
                return generate_sample_data()
        
        # Convert columns to appropriate types
        try:
            # Clean up Lap column (remove any decimal points)
            if 'Lap' in df.columns:
                df['Lap'] = pd.to_numeric(df['Lap'], errors='coerce')
                df['Lap'] = df['Lap'].ffill().astype('Int64')
            
            df['Distance'] = pd.to_numeric(df['Distance'], errors='coerce')
            df['Speed'] = pd.to_numeric(df['Speed'], errors='coerce')
            
            # Convert optional columns
            optional_conversions = {
                'Throttle': lambda x: pd.to_numeric(x, errors='coerce') / 100.0,  # Convert from % to 0-1
                'Brake': lambda x: pd.to_numeric(x, errors='coerce') / 100.0,     # Convert from % to 0-1
                'Steering': lambda x: pd.to_numeric(x, errors='coerce'),
                'Gear': lambda x: pd.to_numeric(x, errors='coerce').astype('Int64'),
                'RPM': lambda x: pd.to_numeric(x, errors='coerce'),
                'TireFL': lambda x: pd.to_numeric(x, errors='coerce'),
                'TireFR': lambda x: pd.to_numeric(x, errors='coerce'),
                'TireRL': lambda x: pd.to_numeric(x, errors='coerce'),
                'TireRR': lambda x: pd.to_numeric(x, errors='coerce'),
                'Time': lambda x: pd.to_numeric(x, errors='coerce')
            }
            
            for col, converter in optional_conversions.items():
                if col in df.columns:
                    df[col] = converter(df[col])
            
            # Calculate lap time if not present
            if 'LapTime' not in df.columns and 'Time' in df.columns:
                df['LapTime'] = df.groupby('Lap')['Time'].transform('max')
            
            # Remove rows with NaN in required columns
            before_len = len(df)
            df = df.dropna(subset=['Lap', 'Distance', 'Speed'])
            after_len = len(df)
            
            if before_len != after_len:
                st.warning(f"⚠️ Removed {before_len - after_len} rows with invalid data")
            
            if len(df) == 0:
                st.error("No valid data rows found after cleaning. Using sample data.")
                return generate_sample_data()
            
            # Ensure Time column exists for lap time calculation
            if 'Time' not in df.columns and 'time' in df.columns:
                df['Time'] = df['time']
            
            # Sort by Lap and Distance to ensure proper ordering
            df = df.sort_values(['Lap', 'Distance']).reset_index(drop=True)
            
            # Display success message
            st.success(f"✅ File loaded successfully! Found {len(df):,} data points across {df['Lap'].nunique()} laps")
            st.info(f"📋 Columns detected: {', '.join(df.columns.tolist())}")
                
        except Exception as e:
            st.error(f"Error converting data types: {str(e)}. Using sample data.")
            return generate_sample_data()
        
        return df
        
    except Exception as e:
        st.error(f"❌ Unexpected error loading file: {str(e)}")
        st.info("Using sample data instead.")
        return generate_sample_data()

def create_speed_trace(df, selected_laps, lap_times_dict):
    """Create speed trace comparison plot"""
    fig = go.Figure()
    
    for lap in selected_laps:
        lap_data = df[df['Lap'] == lap].copy()
        
        # Sort by distance to ensure proper line drawing
        lap_data = lap_data.sort_values('Distance')
        
        # Get lap time for this lap
        lap_time = lap_times_dict.get(lap, 0)
        lap_time_str = f"{lap_time:.3f}s" if lap_time > 0 else "N/A"
        
        fig.add_trace(go.Scatter(
            x=lap_data['Distance'],
            y=lap_data['Speed'],
            name=f'Lap {lap} ({lap_time_str})',
            mode='lines',
            line=dict(width=2),
            hovertemplate='Distance: %{x:.0f}m<br>Speed: %{y:.1f} km/h<extra></extra>'
        ))
    
    fig.update_layout(
        **get_plotly_layout(
            title='Speed Trace Comparison',
            xaxis_title='Distance (m)',
            yaxis_title='Speed (km/h)',
            hovermode='x unified',
            height=500
        )
    )
    
    return fig

def create_input_analysis(df, lap):
    """Create throttle, brake, and steering input analysis"""
    lap_data = df[df['Lap'] == lap]
    
    fig = make_subplots(
        rows=3, cols=1,
        subplot_titles=('Throttle Input', 'Brake Input', 'Steering Input'),
        vertical_spacing=0.1,
        shared_xaxes=True
    )
    
    # Throttle
    fig.add_trace(go.Scatter(
        x=lap_data['Distance'],
        y=lap_data['Throttle'] * 100,
        name='Throttle',
        fill='tozeroy',
        line=dict(color='#50C878', width=2),
        hovertemplate='Distance: %{x:.0f}m<br>Throttle: %{y:.1f}%<extra></extra>'
    ), row=1, col=1)
    
    # Brake
    fig.add_trace(go.Scatter(
        x=lap_data['Distance'],
        y=lap_data['Brake'] * 100,
        name='Brake',
        fill='tozeroy',
        line=dict(color='#8B1538', width=2),
        hovertemplate='Distance: %{x:.0f}m<br>Brake: %{y:.1f}%<extra></extra>'
    ), row=2, col=1)
    
    # Steering
    fig.add_trace(go.Scatter(
        x=lap_data['Distance'],
        y=lap_data['Steering'] * 100,
        name='Steering',
        line=dict(color='#4A90E2', width=2),
        hovertemplate='Distance: %{x:.0f}m<br>Steering: %{y:.1f}%<extra></extra>'
    ), row=3, col=1)
    
    fig.update_layout(
        **get_plotly_layout(
            title=f'Driver Input Analysis - Lap {lap}',
            height=700,
            showlegend=False
        )
    )
    
    fig.update_xaxes(title_text='Distance (m)', row=3, col=1)
    fig.update_yaxes(title_text='%', row=1, col=1)
    fig.update_yaxes(title_text='%', row=2, col=1)
    fig.update_yaxes(title_text='%', row=3, col=1)
    
    return fig

def create_tire_temp_plot(df, lap):
    """Create tire temperature visualization"""
    lap_data = df[df['Lap'] == lap]
    
    fig = go.Figure()
    
    tires = [
        ('Front Left', 'TireFL', '#FF6B8A'),
        ('Front Right', 'TireFR', '#FF9BB5'),
        ('Rear Left', 'TireRL', '#A01C3A'),
        ('Rear Right', 'TireRR', '#8B1538')
    ]
    
    for name, col, color in tires:
        fig.add_trace(go.Scatter(
            x=lap_data['Distance'],
            y=lap_data[col],
            name=name,
            mode='lines',
            line=dict(color=color, width=2),
            hovertemplate=f'{name}<br>Distance: %{{x:.0f}}m<br>Temp: %{{y:.1f}}°C<extra></extra>'
        ))
    
    # Add optimal temperature range
    fig.add_hrect(y0=85, y1=95, fillcolor='rgba(80, 200, 120, 0.1)', 
                  line_width=0, annotation_text="Optimal Range", 
                  annotation_position="right")
    
    fig.update_layout(
        **get_plotly_layout(
            title=f'Tire Temperature Analysis - Lap {lap}',
            xaxis_title='Distance (m)',
            yaxis_title='Temperature (°C)',
            hovermode='x unified',
            height=500
        )
    )
    
    return fig

def create_gear_usage_plot(df, selected_laps):
    """Create gear usage comparison"""
    gear_data = []
    
    for lap in selected_laps:
        lap_df = df[df['Lap'] == lap]
        for gear in range(1, 7):
            time_in_gear = len(lap_df[lap_df['Gear'] == gear]) / len(lap_df) * 100
            gear_data.append({'Lap': f'Lap {lap}', 'Gear': f'Gear {gear}', 'Percentage': time_in_gear})
    
    gear_df = pd.DataFrame(gear_data)
    
    fig = px.bar(gear_df, x='Lap', y='Percentage', color='Gear',
                 title='Gear Usage Distribution',
                 labels={'Percentage': 'Time in Gear (%)'},
                 color_discrete_sequence=['#8B1538', '#A01C3A', '#FF6B8A', '#FF9BB5', '#4A90E2', '#50C878'])
    
    fig.update_layout(
        **get_plotly_layout(
            title='Gear Usage Distribution',
            height=500,
            barmode='stack'
        )
    )
    
    return fig

def create_speed_heatmap(df, lap):
    """Create track position speed heatmap"""
    lap_data = df[df['Lap'] == lap]
    
    # Simulate X, Y coordinates based on distance
    angle = lap_data['Distance'] / 5000 * 2 * np.pi * 3  # 3 loops
    x = np.cos(angle) * (1000 + lap_data['Distance'] / 50)
    y = np.sin(angle) * (1000 + lap_data['Distance'] / 50)
    
    fig = go.Figure(data=go.Scatter(
        x=x,
        y=y,
        mode='markers',
        marker=dict(
            size=8,
            color=lap_data['Speed'],
            colorscale=[[0, '#8B1538'], [0.5, '#FFD700'], [1, '#50C878']],
            showscale=True,
            colorbar=dict(
                title=dict(text='Speed<br>(km/h)', side='right'),
                len=0.7,
                thickness=15
            )
        ),
        text=lap_data['Speed'],
        hovertemplate='Speed: %{text:.1f} km/h<extra></extra>'
    ))
    
    fig.update_layout(
        **get_plotly_layout(
            title=f'Track Speed Heatmap - Lap {lap}',
            xaxis=dict(showgrid=False, zeroline=False, showticklabels=False, title=''),
            yaxis=dict(showgrid=False, zeroline=False, showticklabels=False, title=''),
            height=600,
            width=600
        )
    )
    
    return fig

def create_rpm_power_plot(df, lap):
    """Create RPM and speed correlation plot"""
    lap_data = df[df['Lap'] == lap]
    
    fig = make_subplots(specs=[[{"secondary_y": True}]])
    
    fig.add_trace(go.Scatter(
        x=lap_data['Distance'],
        y=lap_data['RPM'],
        name='RPM',
        line=dict(color='#A01C3A', width=2),
        hovertemplate='Distance: %{x:.0f}m<br>RPM: %{y:.0f}<extra></extra>'
    ), secondary_y=False)
    
    fig.add_trace(go.Scatter(
        x=lap_data['Distance'],
        y=lap_data['Speed'],
        name='Speed',
        line=dict(color='#4A90E2', width=2),
        hovertemplate='Distance: %{x:.0f}m<br>Speed: %{y:.1f} km/h<extra></extra>'
    ), secondary_y=True)
    
    fig.update_layout(
        **get_plotly_layout(
            title=f'RPM & Speed Profile - Lap {lap}',
            hovermode='x unified',
            height=500
        )
    )
    
    fig.update_xaxes(title_text='Distance (m)')
    fig.update_yaxes(title_text='RPM', secondary_y=False, color='#A01C3A')
    fig.update_yaxes(title_text='Speed (km/h)', secondary_y=True, color='#4A90E2')
    
    return fig

def calculate_performance_metrics(df, lap, lap_times_dict):
    """Calculate key performance metrics for a lap"""
    lap_data = df[df['Lap'] == lap]
    
    # Get lap time from calculated lap times
    lap_time = lap_times_dict.get(lap, 0.0)
    
    metrics = {
        'lap_time': lap_time,
        'avg_speed': lap_data['Speed'].mean(),
        'max_speed': lap_data['Speed'].max(),
        'min_speed': lap_data['Speed'].min(),
        'avg_throttle': 0.0,
        'avg_brake': 0.0,
        'max_rpm': 0.0,
        'avg_tire_temp': 0.0
    }
    
    # Add throttle/brake if available
    if 'Throttle' in lap_data.columns:
        metrics['avg_throttle'] = lap_data['Throttle'].mean() * 100
    
    if 'Brake' in lap_data.columns:
        metrics['avg_brake'] = lap_data['Brake'].mean() * 100
    
    # Add RPM if available
    if 'RPM' in lap_data.columns:
        metrics['max_rpm'] = lap_data['RPM'].max()
    
    # Add tire temps if available
    if all(col in lap_data.columns for col in ['TireFL', 'TireFR', 'TireRL', 'TireRR']):
        metrics['avg_tire_temp'] = (lap_data['TireFL'].mean() + lap_data['TireFR'].mean() + 
                                    lap_data['TireRL'].mean() + lap_data['TireRR'].mean()) / 4
    
    return metrics

# Main app
def main():
    # Header
    st.markdown("""
        <h1 style='text-align: center; font-size: 3rem; margin-bottom: 0;'>
            🏎️ TELEMETRY ANALYSIS
        </h1>
        <p style='text-align: center; color: #B0B0B0; font-size: 1.1rem; margin-top: 0; letter-spacing: 3px;'>
            RACING DATA VISUALIZATION & INSIGHTS
        </p>
    """, unsafe_allow_html=True)
    
    # Sidebar
    with st.sidebar:
        st.markdown("## ⚙️ DATA SOURCE")
        
        use_sample = st.checkbox("Use Sample Data", value=True, 
                                help="Toggle to use demo data or upload your own")
        
        uploaded_file = None
        if not use_sample:
            uploaded_file = st.file_uploader(
                "Upload Telemetry Data",
                type=['csv', 'xlsx', 'xls', 'zip'],
                help="Upload CSV, Excel, or ZIP file with telemetry data (supports pyTelemetry/Telemetrick format)"
            )
        
        st.markdown("---")
        st.markdown("## 📊 FILE FORMAT")
        st.info("""
        **Supported Formats:**
        - ✅ **pyTelemetry/Telemetrick** (ZIP or CSV)
        - CSV (comma, semicolon, or tab separated)
        - Excel (.xlsx, .xls)
        
        **Required Columns:**
        - `Lap` (or `Lap Number`): Lap number
        - `Distance` (or `Lap Distance`): Distance from start (m)
        - `Speed` (or `Ground Speed`): Vehicle speed (km/h)
        
        **Optional Columns:**
        - `Time`, `Throttle Pos`, `Brake Pos`, `Steering Angle`
        - `Gear`, `Engine RPM`
        - `Tire Temp Core FL/FR/RL/RR`
        
        **pyTelemetry Notes:**
        - Upload the ZIP file directly
        - Metadata will be automatically extracted
        - All columns mapped automatically
        """)
        
        # Download template button
        if st.button("📥 Download CSV Template"):
            template_df = generate_sample_data(2)
            csv_template = template_df.to_csv(index=False)
            st.download_button(
                label="💾 Save Template",
                data=csv_template,
                file_name="telemetry_template.csv",
                mime="text/csv",
                help="Download a sample CSV with correct formatting"
            )
        
        if uploaded_file is not None:
            st.markdown("---")
            st.markdown("## 📄 UPLOADED FILE")
            st.text(f"Name: {uploaded_file.name}")
            st.text(f"Size: {uploaded_file.size / 1024:.1f} KB")
        
        st.markdown("---")
        st.markdown("## 📖 FEATURES")
        st.markdown("""
        - **Speed Trace Analysis**
        - **Driver Input Telemetry**
        - **Tire Temperature**
        - **Gear Usage Statistics**
        - **Track Speed Heatmap**
        - **RPM/Power Analysis**
        - **Performance Metrics**
        - **Multi-Lap Comparison**
        """)
    
    # Load data
    if use_sample or uploaded_file is None:
        df = generate_sample_data(5)
        if use_sample:
            st.info("📊 Using sample telemetry data. Toggle 'Use Sample Data' to upload your own.")
    else:
        df = load_telemetry_data(uploaded_file)
        if df is None:
            st.stop()
    
    if df is None or len(df) == 0:
        st.error("No data available. Please upload a valid telemetry file.")
        st.stop()
    
    # Show data preview option
    with st.expander("🔍 Preview Data", expanded=False):
        st.markdown("### First 10 rows of loaded data:")
        st.dataframe(df.head(10), use_container_width=True)
        
        st.markdown("### Data Summary:")
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total Rows", f"{len(df):,}")
        with col2:
            st.metric("Columns", len(df.columns))
        with col3:
            st.metric("Unique Laps", df['Lap'].nunique() if 'Lap' in df.columns else 'N/A')
    
    st.markdown("---")
    
    # Session Overview
    st.markdown("## 🎯 SESSION OVERVIEW")
    
    # Calculate lap times from time differences
    lap_times_dict = calculate_lap_times(df)
    
    if len(lap_times_dict) == 0:
        st.warning("⚠️ Could not calculate lap times. Ensure your data has a 'Time' column with elapsed time in seconds.")
    
    # Get unique laps
    available_laps = sorted(df['Lap'].unique())
    
    # Performance metrics for all laps
    cols = st.columns(4)
    
    # Calculate best lap with proper type handling
    try:
        if len(lap_times_dict) > 0:
            # Find lap with minimum time
            best_lap = min(lap_times_dict, key=lap_times_dict.get)
            best_time = lap_times_dict[best_lap]
        else:
            st.warning("⚠️ Could not calculate lap times from data")
            best_lap = available_laps[0] if available_laps else 1
            best_time = 0.0
    except Exception as e:
        st.warning(f"⚠️ Could not calculate best lap time: {str(e)}")
        best_lap = available_laps[0] if available_laps else 1
        best_time = 0.0
    
    with cols[0]:
        st.markdown(f"""
        <div class='stat-card'>
            <div class='stat-value'>{len(available_laps)}</div>
            <div class='stat-label'>Total Laps</div>
        </div>
        """, unsafe_allow_html=True)
    
    with cols[1]:
        if best_time > 0:
            st.markdown(f"""
            <div class='stat-card'>
                <div class='stat-value'>{best_time:.3f}s</div>
                <div class='stat-label'>Best Lap Time</div>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class='stat-card'>
                <div class='stat-value'>--:--</div>
                <div class='stat-label'>Best Lap Time</div>
            </div>
            """, unsafe_allow_html=True)
    
    with cols[2]:
        avg_speed = df['Speed'].mean()
        st.markdown(f"""
        <div class='stat-card'>
            <div class='stat-value'>{avg_speed:.1f}</div>
            <div class='stat-label'>Avg Speed (km/h)</div>
        </div>
        """, unsafe_allow_html=True)
    
    with cols[3]:
        max_speed = df['Speed'].max()
        st.markdown(f"""
        <div class='stat-card'>
            <div class='stat-value'>{max_speed:.1f}</div>
            <div class='stat-label'>Max Speed (km/h)</div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Analysis Tabs
    tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
        "🏁 SPEED TRACE", 
        "🎮 DRIVER INPUTS", 
        "🔥 TIRE TEMPS", 
        "⚙️ GEAR USAGE",
        "🗺️ TRACK MAP",
        "📈 RPM ANALYSIS"
    ])
    
    # Tab 1: Speed Trace
    with tab1:
        st.markdown("### Speed Trace Comparison")
        st.markdown("Compare speed profiles across multiple laps to identify braking points and acceleration zones.")
        
        selected_laps = st.multiselect(
            "Select Laps to Compare",
            available_laps,
            default=available_laps[:3] if len(available_laps) >= 3 else available_laps,
            key='speed_trace_laps'
        )
        
        if selected_laps:
            fig = create_speed_trace(df, selected_laps, lap_times_dict)
            st.plotly_chart(fig, use_container_width=True)
            
            # Lap time comparison table
            st.markdown("#### Lap Time Comparison")
            try:
                lap_time_data = []
                for lap in selected_laps:
                    if lap in lap_times_dict:
                        lap_time_data.append({'Lap': lap, 'Lap Time (s)': lap_times_dict[lap]})
                
                if lap_time_data:
                    lap_times_df = pd.DataFrame(lap_time_data)
                    lap_times_df['Delta (s)'] = lap_times_df['Lap Time (s)'] - lap_times_df['Lap Time (s)'].min()
                    st.dataframe(lap_times_df, use_container_width=True, hide_index=True)
                else:
                    st.info("Lap time data not available for selected laps")
            except Exception as e:
                st.warning(f"Could not generate lap time comparison: {str(e)}")
        else:
            st.warning("Please select at least one lap to display.")
    
    # Tab 2: Driver Inputs
    with tab2:
        st.markdown("### Driver Input Telemetry")
        st.markdown("Analyze throttle, brake, and steering inputs to refine driving technique.")
        
        input_lap = st.selectbox("Select Lap", available_laps, key='input_lap')
        
        if 'Throttle' in df.columns and 'Brake' in df.columns:
            fig = create_input_analysis(df, input_lap)
            st.plotly_chart(fig, use_container_width=True)
            
            # Input statistics
            lap_data = df[df['Lap'] == input_lap]
            col1, col2, col3 = st.columns(3)
            
            with col1:
                avg_throttle = lap_data['Throttle'].mean() * 100
                st.metric("Avg Throttle", f"{avg_throttle:.1f}%")
            
            with col2:
                avg_brake = lap_data['Brake'].mean() * 100
                st.metric("Avg Brake", f"{avg_brake:.1f}%")
            
            with col3:
                if 'Steering' in df.columns:
                    max_steering = lap_data['Steering'].abs().max() * 100
                    st.metric("Max Steering", f"{max_steering:.1f}%")
        else:
            st.warning("Throttle and Brake data not available in the dataset.")
    
    # Tab 3: Tire Temperatures
    with tab3:
        st.markdown("### Tire Temperature Analysis")
        st.markdown("Monitor tire temperatures to optimize pressure and driving style.")
        
        tire_lap = st.selectbox("Select Lap", available_laps, key='tire_lap')
        
        if all(col in df.columns for col in ['TireFL', 'TireFR', 'TireRL', 'TireRR']):
            fig = create_tire_temp_plot(df, tire_lap)
            st.plotly_chart(fig, use_container_width=True)
            
            # Tire statistics
            lap_data = df[df['Lap'] == tire_lap]
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric("Front Left", f"{lap_data['TireFL'].mean():.1f}°C")
            with col2:
                st.metric("Front Right", f"{lap_data['TireFR'].mean():.1f}°C")
            with col3:
                st.metric("Rear Left", f"{lap_data['TireRL'].mean():.1f}°C")
            with col4:
                st.metric("Rear Right", f"{lap_data['TireRR'].mean():.1f}°C")
            
            st.info("💡 **Optimal tire temperature range: 85-95°C**")
        else:
            st.warning("Tire temperature data not available in the dataset.")
    
    # Tab 4: Gear Usage
    with tab4:
        st.markdown("### Gear Usage Analysis")
        st.markdown("Understand gear selection patterns and optimize shift points.")
        
        gear_laps = st.multiselect(
            "Select Laps to Compare",
            available_laps,
            default=available_laps[:3] if len(available_laps) >= 3 else available_laps,
            key='gear_laps'
        )
        
        if gear_laps and 'Gear' in df.columns:
            fig = create_gear_usage_plot(df, gear_laps)
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.warning("Please select laps or gear data not available.")
    
    # Tab 5: Track Map
    with tab5:
        st.markdown("### Track Speed Heatmap")
        st.markdown("Visualize speed distribution across the track layout.")
        
        map_lap = st.selectbox("Select Lap", available_laps, key='map_lap')
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            fig = create_speed_heatmap(df, map_lap)
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.markdown("#### Track Sectors")
            st.info("Track divided into sectors based on distance")
            
            # Calculate sector times
            lap_data = df[df['Lap'] == map_lap]
            total_distance = lap_data['Distance'].max()
            
            sectors = [
                (0, total_distance/3, "Sector 1"),
                (total_distance/3, 2*total_distance/3, "Sector 2"),
                (2*total_distance/3, total_distance, "Sector 3")
            ]
            
            for start, end, name in sectors:
                sector_data = lap_data[(lap_data['Distance'] >= start) & (lap_data['Distance'] < end)]
                avg_speed = sector_data['Speed'].mean()
                st.metric(name, f"{avg_speed:.1f} km/h")
    
    # Tab 6: RPM Analysis
    with tab6:
        st.markdown("### RPM & Speed Profile")
        st.markdown("Analyze engine RPM and speed correlation for optimal power delivery.")
        
        rpm_lap = st.selectbox("Select Lap", available_laps, key='rpm_lap')
        
        if 'RPM' in df.columns:
            fig = create_rpm_power_plot(df, rpm_lap)
            st.plotly_chart(fig, use_container_width=True)
            
            # RPM statistics
            lap_data = df[df['Lap'] == rpm_lap]
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric("Max RPM", f"{lap_data['RPM'].max():.0f}")
            with col2:
                st.metric("Avg RPM", f"{lap_data['RPM'].mean():.0f}")
            with col3:
                st.metric("Min RPM", f"{lap_data['RPM'].min():.0f}")
        else:
            st.warning("RPM data not available in the dataset.")
    
    # Performance Insights Section
    st.markdown("---")
    st.markdown("## 💡 PERFORMANCE INSIGHTS")
    
    insights_lap = st.selectbox("Analyze Lap", available_laps, key='insights_lap')
    metrics = calculate_performance_metrics(df, insights_lap, lap_times_dict)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 📊 Lap Statistics")
        if metrics['lap_time'] > 0:
            st.metric("Lap Time", f"{metrics['lap_time']:.3f} s")
        else:
            st.metric("Lap Time", "N/A")
        st.metric("Average Speed", f"{metrics['avg_speed']:.1f} km/h")
        st.metric("Maximum Speed", f"{metrics['max_speed']:.1f} km/h")
        st.metric("Minimum Speed", f"{metrics['min_speed']:.1f} km/h")
    
    with col2:
        st.markdown("### 🎯 Driver Inputs")
        if metrics['avg_throttle'] > 0:
            st.metric("Avg Throttle", f"{metrics['avg_throttle']:.1f}%")
        else:
            st.metric("Avg Throttle", "N/A")
        
        if metrics['avg_brake'] > 0:
            st.metric("Avg Brake", f"{metrics['avg_brake']:.1f}%")
        else:
            st.metric("Avg Brake", "N/A")
        
        if 'RPM' in df.columns and metrics['max_rpm'] > 0:
            st.metric("Max RPM", f"{metrics['max_rpm']:.0f}")
        
        if all(col in df.columns for col in ['TireFL', 'TireFR', 'TireRL', 'TireRR']) and metrics['avg_tire_temp'] > 0:
            st.metric("Avg Tire Temp", f"{metrics['avg_tire_temp']:.1f}°C")
    
    # AI-style insights
    st.markdown("### 🤖 Key Insights")
    
    try:
        delta_to_best = metrics['lap_time'] - best_time
        
        if abs(delta_to_best) < 0.001:  # Essentially zero
            st.success(f"🏆 **Excellent!** This is your best lap with a time of {metrics['lap_time']:.3f}s")
        elif delta_to_best < 0.1:
            st.success(f"🏆 **Excellent!** Within {delta_to_best:.3f}s of your best lap")
        elif delta_to_best < 0.5:
            st.info(f"⚡ **Strong Performance!** Only {delta_to_best:.3f}s off your best lap. Focus on late braking zones.")
        else:
            st.warning(f"📈 **Room for Improvement** - {delta_to_best:.3f}s slower than best. Analyze speed trace for opportunities.")
    except Exception as e:
        st.info("💡 Compare with other laps to find improvement areas")
    
    if 'Throttle' in df.columns and metrics['avg_throttle'] < 60:
        st.warning("⚠️ Low average throttle application. Consider carrying more speed through corners.")
    
    if all(col in df.columns for col in ['TireFL', 'TireFR', 'TireRL', 'TireRR']):
        if metrics['avg_tire_temp'] < 80:
            st.warning("🧊 Tire temperatures below optimal range. Push harder or adjust tire pressure.")
        elif metrics['avg_tire_temp'] > 100:
            st.warning("🔥 Tire temperatures too high. Risk of excessive wear and reduced grip.")
        else:
            st.success("✅ Tire temperatures in optimal range (85-95°C)")

if __name__ == "__main__":
    main()
