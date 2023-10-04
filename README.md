## Scrape Data from Web and Display it in a Map

### Installation
```
pip install folium
pip install selenium
pip install bs4
```

Folium is for maps. Selenium and bs4 are for scraping

### Running
```
python3 create_school_map_for_state.py --grade GRADELEVEL --state YOURSTATE
```

YOURSTATE is a US state.

GRADELEVEL can be
- elementary
- middle
- high

Example:

```
python3 create_school_map_for_state.py --grade elementary --state washington
```

### Running with Big States

Texas map got laggy when including all schools. You can split up the maps by providing a json with city name and longitutde, latitude.
```
python3 create_school_map_for_state.py --grade elementary --state texas --multi_map_config texas_cities.json
```
