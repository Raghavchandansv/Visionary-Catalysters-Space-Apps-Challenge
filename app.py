import streamlit as st
import xarray as xr
import glob
import os
import numpy as np
import re
from datetime import datetime

# --- CONFIGURATION ---
DATA_FOLDER = r"C:\Users\ragha\NASA_Space_Apps\nasa-data\NASA TROPOMONI"
# Use the confirmed variable name
NO2_VARIABLE_NAME = 'Tropospheric_NO2' 
# ---------------------

# --- Diagnostic Function ---
def preprocess_tempo_data(ds):
    """
    Diagnostic function to check for variable existence and return data.
    """
    source_file = ds.encoding.get('source', 'UnknownFile')

    # 1. Check for NO2 Variable
    if NO2_VARIABLE_NAME in ds.data_vars:
        # Check for coordinates
        if 'Longitude' in ds.coords and 'Latitude' in ds.coords:
            st.success(f"File OK: {os.path.basename(source_file)}")
            return ds[[NO2_VARIABLE_NAME, 'Longitude', 'Latitude']]
        else:
            st.warning(f"File has NO2 but MISSING COORDS: {os.path.basename(source_file)}")
            return None
    else:
        st.warning(f"File MISSING NO2 VARIABLE: {os.path.basename(source_file)}")
        return None 


# --- MAIN APP EXECUTION ---
@st.cache_data(show_spinner=False)
def load_and_combine_data(folder_path):
    data_path = os.path.join(folder_path, '*.nc4')
    file_paths = glob.glob(data_path)

    if not file_paths:
        st.error(f"Error: No files found in: {folder_path}")
        return None

    clean_datasets = []
    
    for file_path in file_paths:
        try:
            with xr.open_dataset(file_path, engine='h5netcdf') as ds:
                # RUNNING THE DIAGNOSTIC CHECK
                processed_ds = preprocess_tempo_data(ds)
                
                if processed_ds is not None:
                    # Manually add the time dimension to the temporary structure
                    time_coverage_start = ds.attrs.get('time_coverage_start', '2000-01-01')
                    time_value = np.datetime64(time_coverage_start.split('T')[0])
                    processed_ds = processed_ds.expand_dims(time=1)
                    processed_ds['time'] = ('time', [time_value])

                    clean_datasets.append(processed_ds)
        except Exception as e:
            st.error(f"FATAL ERROR during File Processing: {os.path.basename(file_path)}. Error: {e}")
            continue

    if not clean_datasets:
        return None

    # This part should combine the successful files
    try:
        combined_data = xr.concat(clean_datasets, dim='time', combine_attrs='drop')
        
        # Rename coordinates for final output consistency (required for plotting later)
        combined_data = combined_data.rename({
            'Longitude': 'lon', 
            'Latitude': 'lat', 
            NO2_VARIABLE_NAME: 'no2_concentration'
        })
        
        return combined_data.chunk({'time': 1})
    except Exception as e:
        st.error(f"FATAL COMBINATION ERROR: {e}")
        return None


# --- STREAMLIT FRONTEND (Simplified to find crash) ---
st.set_page_config(layout="wide")
st.title("Data Pipeline Diagnostic")
st.markdown("---")

with st.spinner("Diagnosing data files..."):
    all_data = load_and_combine_data(DATA_FOLDER)

if all_data is not None:
    st.header("SUCCESS! All Usable Data Combined")
    st.write(f"Total time steps combined: {len(all_data['time'].compute())}")
    st.subheader("Final Dataset Preview:")
    st.code(all_data.__repr__())
    
    # Force a calculation to check Dask
    mean_no2 = all_data['no2_concentration'].mean().compute()
    st.metric("Overall Mean NO₂", f"{mean_no2.item():.2e} mol/cm²")
else:
    st.error("Data loading failed. Check error messages above.")
