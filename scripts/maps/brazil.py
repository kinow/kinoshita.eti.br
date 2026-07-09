import json
import folium
from branca.element import Element
import os
import shutil
import unicodedata

# -------------------------------------------------------------------
# Config
# -------------------------------------------------------------------

SPAIN_REGIONS_GEOJSON = "spain_comunidades_autonomas.geojson"
SPAIN_CITIES_GEOJSON = "spain_cities.geojson"
DESTINATION_DIR = "../../static/maps/"

# Colors
COLOR_COMUNIDAD_VISITED = "#2ecc71"
COLOR_CITY_VISITED = "#89FF00"
COLOR_COMUNIDAD_DEFAULT = "#ecf0f1"
COLOR_BORDER = "#555"

# -------------------------------------------------------------------
# Load data
# -------------------------------------------------------------------

def norm(s):
    s = s.strip().lower()
    s = ''.join(c for c in unicodedata.normalize('NFD', s)
                if unicodedata.category(c) != 'Mn')
    return s

with open(SPAIN_REGIONS_GEOJSON, encoding="utf-8") as f:
    regions_data = json.load(f)

with open(SPAIN_CITIES_GEOJSON, encoding="utf-8") as f:
    cities_data = json.load(f)

print(sorted({f["fields"]["admin1_code"] for f in cities_data["features"]}))

ADMIN1_TO_COMUNIDAD = {
    "51": "Andalucía",
    "52": "Aragón",
    "34": "Asturias",
    "53": "Islas Baleares",
    "54": "Canarias",
    "32": "Cantabria",
    "55": "Castilla y León",
    "56": "Cataluña",
    "60": "Comunidad Valenciana",
    "57": "Extremadura",
    "58": "Galicia",
    "29": "Comunidad de Madrid",
    "31": "Murcia",
    "39": "Navarra",
    "59": "País Vasco",
    "27": "La Rioja",
    "54": "Castilla-La Mancha",
    "CE": "Ceuta",
    "ML": "Melilla",
}

TOTAL_COMUNIDADES = len(regions_data["features"])
TOTAL_CITIES = len(cities_data["features"])

TOTAL_POSSIBLE = TOTAL_COMUNIDADES + TOTAL_CITIES

# -------------------------------------------------------------------
# Function to create the maps
# -------------------------------------------------------------------

def create_travel_map(filename, regiones, ciudades):
    # Build a lookup: normalized GeoJSON name -> actual GeoJSON name
    geojson_region_names = {norm(f["properties"]["name"]): f["properties"]["name"]
                            for f in regions_data["features"]}

    # Match user-passed names to exact GeoJSON names
    visited_regions_norm = set()
    for r in regiones:
        n = norm(r)
        if n in geojson_region_names:
            visited_regions_norm.add(n)  # normalized name

    # --- Cities ---
    visited_cities_norm = {(norm(c), norm(r)) for c, r in ciudades}

    # --- The "Focus" Crop ---
    # Spain bounds
    map_bounds = [[35.5, -10.5], [44.5, 4.5]]

    m = folium.Map(
        location=[40.0, -3.5],
        zoom_start=6,
        tiles="cartodbpositron",
        max_bounds=True,
    )

    m.fit_bounds(map_bounds)

    # Comunidades Autónomas
    folium.GeoJson(
        regions_data,
        style_function=lambda f: {
            "fillColor": COLOR_COMUNIDAD_VISITED
            if norm(f["properties"]["name"]) in visited_regions_norm
            else COLOR_COMUNIDAD_DEFAULT,
            "color": COLOR_BORDER,
            "weight": 1,
            "fillOpacity": 0.75,
        },
        tooltip=folium.GeoJsonTooltip(
            fields=["name"],
            aliases=["Comunidad:"],
        ),
    ).add_to(m)

    # Precompute a set of tuples: (normalized city name, admin1_code)
    visited_cities_set = {(norm(c), norm(r)) for c, r in ciudades}

    # Cities
    for feature in cities_data["features"]:
        fields = feature.get("fields", {})  # <-- correct for your dataset
        geometry = feature.get("geometry")

        city = fields.get("name")
        admin1 = fields.get("admin1_code")

        if not city or not admin1 or not geometry:
            print(f"⚠ Skipping unknown city: {city} / admin1: {admin1}")
            continue

        region = ADMIN1_TO_COMUNIDAD.get(str(admin1))
        if not region:
            print(f"⚠ Unknown admin1_code: {admin1} for city {city}")
            continue

        coords = geometry["coordinates"][::-1]  # [lat, lon]

        # Correct matching using normalized names
        if (norm(city), norm(region)) in visited_cities_set:
            folium.CircleMarker(
                location=coords,
                radius=6,
                color=COLOR_CITY_VISITED,
                weight=2,
                fill=True,
                fill_color=COLOR_CITY_VISITED,
                fill_opacity=1,
                tooltip=f"{city} ({region})",
            ).add_to(m)

    # Municipalities, cities...
    manual_cities = {
        "Garraf": {"region": "Cataluña", "coords": [41.2547363, 1.9000556]},  # lat, lon
        "Villadecans": {"region": "Cataluña", "coords": [41.3149068, 1.9951859]},  # lat, lon
    }

    for city_name, info in manual_cities.items():
        region_norm = norm(info["region"])
        if (norm(city_name), region_norm) in visited_cities_norm:
            folium.CircleMarker(
                location=info["coords"],
                radius=6,
                color=COLOR_CITY_VISITED,
                weight=2,
                fill=True,
                fill_color=COLOR_CITY_VISITED,
                fill_opacity=1,
                tooltip=f"{city_name} ({info['region']})",
            ).add_to(m)

    # Updated Stats Box with Percentage
    total_visited = len(regiones) + len(ciudades)
    percentage = (total_visited / TOTAL_POSSIBLE) * 100

    stat_html = f"""
    <div style="position: fixed; bottom: 30px; left: 30px; width: 230px;
                background: white; border:2px solid {COLOR_BORDER}; z-index:9999;
                padding: 12px; border-radius: 8px; font-family: Arial, sans-serif;
                box-shadow: 2px 2px 10px rgba(0,0,0,0.2);">
        <b style="font-size: 14px;">Spain Travel Progress</b><br>
        <hr style="margin: 8px 0;">
        <b>Visited:</b> {total_visited} / {TOTAL_POSSIBLE}<br>
        <b>Coverage:</b> {percentage:.1f}%<br>
        <hr style="margin: 8px 0;">
        <b>Comunidades:</b> {len(regiones)} / {TOTAL_COMUNIDADES}<br>
        <b>Cities:</b> {len(ciudades)} / {TOTAL_CITIES}
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
map_1_comunidades = {
    "Comunidad de Madrid",
    "Comunidad Valenciana",
    "Cataluña",
    "Andalucía"
}

map_1_cities = {
    ("Madrid", "Comunidad de Madrid"),
    ("Valencia", "Comunidad Valenciana"),
    ("Badalona", "Cataluña"),
    ("Barcelona", "Cataluña"),
    ("Girona", "Cataluña"),
    ("Villadecans", "Cataluña"),
    ("Castelldefels", "Cataluña"),
    ("Tarragona", "Cataluña"),
    ("Garraf", "Cataluña"),
    ("Sitges", "Cataluña"),
    ("Blanes", "Cataluña"),
    ("Roses", "Cataluña"),
    ("Canet de Mar", "Cataluña"),
    ("Sant Pol de Mar", "Cataluña"),
    ("Montcada i Reixac", "Cataluña"),
    ("Figueres", "Cataluña"),
    ("Granada", "Andalucía"),
    ("Cordoba", "Andalucía"),
    ("Sevilla", "Andalucía"),
}

# Map 2
map_2_comunidades = map_1_comunidades

map_2_cities = map_1_cities

# -------------------------------------------------------------------
# Generate Both
# -------------------------------------------------------------------

create_travel_map(
    "map_1_spain.html",
    map_1_comunidades,
    map_1_cities,
)

create_travel_map(
    "map_2_spain.html",
    map_2_comunidades,
    map_2_cities,
)

