import json
import folium
from branca.element import Element
import os
import shutil

# -------------------------------------------------------------------
# Config
# -------------------------------------------------------------------

COUNTRIES_GEOJSON = "ne_110m_admin_0_countries.geojson"
MAP_UNITS_GEOJSON = "ne_10m_admin_0_map_units.geojson"
DESTINATION_DIR = "../../static/maps/"

# -------------------------------
# Visited regions
# -------------------------------
# Use (admin, name) tuples for precision
visited_map_units = {"England", "Northern Ireland"}

# ISO A3 country codes (rock-solid, no naming issues)
# https://en.wikipedia.org/wiki/ISO_3166-1_alpha-3
visited_countries = {
    "ARG",  # Argentina
    "AUS",  # Australia
    "BEL",  # Belgium
    "BRA",  # Brazil
    "DEU",  # Germany
    "ESP",  # Spain
    "FJI",  # Fiji
    "FRA",  # France
    "IRL",  # Ireland
    "ITA",  # Italy
    "JPN",  # Japan
    "NLD",  # The Netherlands
    "NZL",  # New Zealand
    "PRT",  # Portugal
    "USA",  # United States of America
    "ZAF",  # South Africa
}

# Colors
COLOR_COUNTRY_VISITED = "#2ecc71"
COLOR_REGION_VISITED = "#2ecc71"
COLOR_COUNTRY_DEFAULT = "#ecf0f1"
COLOR_BORDER = "#555"

# -------------------------------------------------------------------
# Load data
# -------------------------------------------------------------------

with open("ne_110m_admin_0_countries.geojson") as f:
    countries_data = json.load(f)

with open("ne_10m_admin_0_map_units.geojson") as f:
    map_units_data = json.load(f)

# -------------------------------------------------------------------
# Function to create the maps
# -------------------------------------------------------------------

def create_travel_map(filename, countries_list, units_list):
    # --- The "Focus" Crop ---
    # South: -60 (cuts Antarctica)
    # North: 72  (shows Canada/Alaska, cuts most of northern Greenland/Arctic)
    # West/East: -170 to 170 (removes the empty edges of the Pacific)
    map_bounds = [[-60, -170], [72, 170]]

    # Create the base map
    m = folium.Map(
        location=[15, 0],      # Slightly lower center for a better balance
        zoom_start=2,
        min_zoom=2,            # Prevent zooming out to see 3 copies of the world
        max_bounds=True,       # Enable the boundary logic
        min_lat=-60,           # Hard South limit
        max_lat=72,            # Hard North limit (The "Greenland Cut")
        tiles="cartodbpositron"
    )

    # Force the map to stay within these coordinates
    m.fit_bounds(map_bounds)

    # Colors
    COLOR_VISITED = "#2ecc71"
    COLOR_DEFAULT = "#ecf0f1"
    COLOR_BORDER = "#555"

    # Add Countries Layer
    folium.GeoJson(
        countries_data,
        style_function=lambda f: {
            "fillColor": COLOR_VISITED if f["properties"].get("iso_a3") in countries_list else COLOR_DEFAULT,
            "color": COLOR_BORDER,
            "weight": 0.5,
            "fillOpacity": 0.8,
        }
    ).add_to(m)

    # Add Map Units Layer (UK/etc)
    folium.GeoJson(
        map_units_data,
        style_function=lambda f: {
            "fillColor": COLOR_VISITED if f["properties"].get("GEOUNIT") in units_list else "transparent",
            "color": COLOR_VISITED if f["properties"].get("GEOUNIT") in units_list else "transparent",
            "weight": 1.5,
            "fillOpacity": 0.7,
        }
    ).add_to(m)

    # --- Stats Calculation ---
    total_visited = len(countries_list) + len(units_list)
    total_possible = 195
    percentage = (total_visited / total_possible) * 100

    # Updated Stats Box with Percentage
    stat_html = f"""
    <div style="position: fixed; bottom: 30px; left: 30px; width: 180px;
                background: white; border:2px solid #555; z-index:9999;
                padding: 12px; border-radius: 8px; font-family: Arial, sans-serif;
                box-shadow: 2px 2px 10px rgba(0,0,0,0.2);">
        <b style="font-size: 14px;">Travel Progress</b><br>
        <hr style="margin: 8px 0; border: 0; border-top: 1px solid #eee;">
        <b>Visited:</b> {total_visited} / {total_possible}<br>
        <b>Coverage:</b> {percentage:.1f}%
    </div>
    """
    m.get_root().html.add_child(Element(stat_html))

    # Save
    m.save(filename)

    # Move to Hugo static folder
    target_path = os.path.join(DESTINATION_DIR, filename)
    shutil.move(filename, target_path)
    print(f"✔ Generated and moved to: {target_path}")

    print(f"✔ Saved: {filename}")


# Map 1
map_1_countries = {"ARG", "AUS", "BEL", "BRA", "DEU", "ESP", "FJI", "FRA", "IRL", "ITA", "JPN", "NLD", "NZL", "PRT", "USA", "ZAF"}
map1_units = {"England", "Northern Ireland"}

# Map 2
map_2_countries = map_1_countries - {"BEL", "NLD", "USA", "ZAF"}
map_2_units = map1_units

# -------------------------------------------------------------------
# Generate Both
# -------------------------------------------------------------------

create_travel_map("map_1_countries.html", map_1_countries, map1_units)
create_travel_map("map_2_countries.html", map_2_countries, map_2_units)
