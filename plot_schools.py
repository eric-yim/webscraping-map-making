import folium
from util.folium_util import FoliumUtil
import json
ALL_INFO_SAVE = "washington_schools_info.json"
NUM_SCHOOLS = 0
SAVE_MAP = "school_map.html"
def score_to_rating(s):
    if s > 82:
        return 6
    elif s > 77:
        return 5
    elif s > 70:
        return 4
    elif s > 60:
        return 3
    elif s > 50:
        return 2
    return 1
    
def construct_marker(line, m):
    global NUM_SCHOOLS
    info = json.loads(line)
    if 'location' in info:
        address = info.get('address','No Address')
        href = info.get('url','')
        scores = info.get('scores',{})
        mean_score = 0
        if len(scores)>0:
            mean_score = sum([float(v.replace('%','')) for v in scores.values()])/float(len(scores))
        rating = score_to_rating(mean_score)
        score_string = json.dumps(scores)
        popup_html = f'<a href="{href}" target="_blank">{address}<br>{scores}</a>'
        folium.Marker(
            location = info['location'],
            popup = folium.Popup(popup_html, max_width=300),
            icon=FoliumUtil.get_colored_icon(rating)
        ).add_to(m)
        NUM_SCHOOLS +=1


def main():
    global NUM_SCHOOLS
    # Create a map centered on a location (you can choose any location)
    map_center = [47.6062, -122.3321]  # seattle
    m = folium.Map(location=map_center, zoom_start=10)

    with open(ALL_INFO_SAVE, 'r') as f:
        # Read the first line from the file
        line = f.readline()
        
        # Check if we've reached the end of the file
        while line:
            marker = construct_marker(line.strip(), m)
            
            # Read the next line
            line = f.readline()

    # Save the map to an HTML file
    m.save(SAVE_MAP)
    print(f"Saved {NUM_SCHOOLS} schools to {SAVE_MAP}")
    

if __name__=='__main__':
    main()