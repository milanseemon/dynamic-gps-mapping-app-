import streamlit as st
import pandas as pd
import folium
import io
import zipfile

st.title("GPS Data Visualization Demo")

st.markdown("""
This demo allows uploading a dataset with latitude and longitude columns,
generates an interactive map, and lets you download the map as an HTML file.
""")

uploaded_file = st.file_uploader("Upload Excel or CSV file", type=["xlsx", "csv"])

if uploaded_file:
    if uploaded_file.name.endswith('xlsx'):
        df = pd.read_excel(uploaded_file)
    else:
        df = pd.read_csv(uploaded_file)
    
    st.write("Columns detected:", df.columns.tolist())
    
    # Detect latitude and longitude columns (simple exact match)
    lat_col = 'latitude' if 'latitude' in df.columns.str.lower() else None
    lon_col = 'longitude' if 'longitude' in df.columns.str.lower() else None
    
    if not lat_col or not lon_col:
        st.error("Latitude and longitude columns not found. Please upload a file with 'latitude' and 'longitude' columns.")
    else:
        df = df.dropna(subset=[lat_col, lon_col])
        center = [df[lat_col].median(), df[lon_col].median()]
        
        m = folium.Map(location=center, zoom_start=10)
        
        for _, row in df.iterrows():
            folium.Marker([row[lat_col], row[lon_col]]).add_to(m)
        
        map_html = m.get_root().render()
        
        st.components.v1.html(map_html, height=600)
        
        # Provide download button
        buf = io.BytesIO()
        with zipfile.ZipFile(buf, 'w') as zf:
            zf.writestr("map.html", map_html)
        buf.seek(0)
        
        st.download_button(
            "Download map as ZIP",
            data=buf,
            file_name="gps_map.zip",
            mime="application/zip"
        )
