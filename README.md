# Geomap Project

Geomap is a web-based mapping and reporting application built with Flask, Folium, Plotly, and MySQL. It provides interactive maps, data visualization, and reporting features for agricultural and field data, supporting both RCM and iFarm databases.

## Features
- Interactive maps with markers and polygons
- Filtering by region, province, municipality, and barangay
- Field and farmer data visualization
- Dynamic reports and charts using Plotly
- Integration with MySQL databases

## Project Structure
```
geomap/
├── app.py                  # Main Flask application with routes and views
├── app_default.py          # Default Flask app (Hello World)
├── connect_to_mysql.py     # Database connection and query functions
├── create_data_frame.py    # DataFrame creation and data processing
├── create_map_markers.py   # Map marker creation with Folium
├── create_map_polygon.py   # Polygon and track segment mapping
├── create_reports.py       # Plotly report and chart generation
├── parse_map_filters.py    # Map filter parsing and SQL query builder
├── views.py                # (Reserved for additional views)
├── requirements.txt        # Python dependencies
├── start_flask             # (Script to start the Flask app)
├── templates/              # HTML templates for rendering
│   ├── fields.html
│   ├── filter_map.html
│   ├── filter_reports.html
│   ├── index.html
│   ├── map.html
│   └── reports.html
└── __pycache__/            # Python bytecode cache (ignored)
```

## Getting Started
1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
2. **Configure your MySQL database credentials** in `connect_to_mysql.py`.
3. **Run the Flask app:**
   ```bash
   python app.py
   ```
4. **Access the app:** Open your browser at `http://localhost:5000`

## Notes
- The `.venv` and `__pycache__/` directories are ignored by git (see `.gitignore`).
- All classes and functions are documented with docstrings for auto documentation tools.

## License
Specify your license here.
