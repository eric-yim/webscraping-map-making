import argparse
from util.usa_util import USA_UTIL
from util.greatschoolsorg_util import GSO_Util
from util.gso_schools_util import GsoSchools
from util.scraper_util import Scraper
import folium
import os, glob, json
def argparse_args():
    # Create an ArgumentParser object
    parser = argparse.ArgumentParser()

    # Add arguments
    parser.add_argument('--data_paginations', default='school_paginations', help='save location for pagination htmls')
    parser.add_argument('--max_paginations', default='120', type=int, help='max paginations to view')
    parser.add_argument('--data_school_pages', default='school_htmls', help='save location for each schools page')
    parser.add_argument('--data_school_info', default='school_info', help='save location for each schools info')
    parser.add_argument('--data_maps', default='saved_maps', help='save location for maps')
    parser.add_argument('--grade', default='elementary', type=str, choices = ['elementary','middle','high'])
    parser.add_argument('--state', required=True, help='A US State')
    

    # Parse the command-line arguments
    return parser.parse_args()
def download_page(base_paginations, page, url):
    save_location = os.path.join(base_paginations, str(page).zfill(4) + ".html")
    return Scraper.download_page(url, save_location)
def download_paginations(args):
    USA_UTIL.assert_state(args.state)
    base_paginations = os.path.join(args.data_paginations,args.state)
    
    os.makedirs(base_paginations, exist_ok=True)
    # Iterate through 100 pages. if failed, break
    for page in range(1,args.max_paginations):
        url = GSO_Util.get_url(args.state, args.grade, page)
        if not (download_page(base_paginations, page, url)):
            print(f"Failed at page {page}. Stopping.")
            break
    print("="*40)
    print("Completed operation: download_paginations")
    print("="*40)
    return base_paginations
def download_school_pages(args, base_paginations):
    listing = sorted(glob.glob(os.path.join(base_paginations, "*.html")))
    base_school_pages = os.path.join(args.data_school_pages, args.state)
    os.makedirs(base_school_pages, exist_ok=True)
    j = 0
    for item in listing:
        school_links = GSO_Util.get_school_links_in_html(item, args.state)
        for school_link in school_links:
            save_location = os.path.join(base_school_pages , str(j).zfill(6) + '.html')
            if not Scraper.download_page(url, save_location):
                print(f"Failed on {url}")
            j+=1
    print("="*40)
    print(f"Completed operation: download_school_pages | {j} pages downloaded")
    print("="*40)
    return base_school_pages
def save_info(info_file, info):
    my_dump = json.dumps(info)
    with open(info_file, 'a') as f:
        f.write(my_dump)
        f.write('\n')
def read_school_info(args, base_school_pages):
    listing = sorted(glob.glob(os.path.join(base_school_pages, "*.html")))
    os.makedirs(args.data_school_info)
    info_file = os.path.join(args.data_school_info,f'{args.state}.json')
    os.remove(info_file)
    all_info = []
    for item in listing:
        print(f"Processing {item}")
        info = GsoSchools.get_info(fpath)
        info['local_file'] = item
        save_info(info_file, info)
    print("="*40)
    print(f"Completed operation: Read School Info")
    print("="*40)
    return info_file

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
    
def construct_marker(line, m, num_schools):
    
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
        num_schools+=1
    return num_schools


def save_map(args, info_file):
    map_name = os.path.join(args.data_maps, f'{args.state.lower()}_{args.grade.lower()}.html')
    num_schools = 0
    location = USA_UTIL.get_location_by_state(args.state)
    map_center = [location['latitude'], location['longitude']]
    m = folium.Map(location=map_center, zoom_start=10)

    with open(info_file, 'r') as f:
        # Read the first line from the file
        line = f.readline()
        
        # Check if we've reached the end of the file
        while line:
            num_schools = construct_marker(line.strip(), m, num_schools)
            
            # Read the next line
            line = f.readline()

    # Save the map to an HTML file
    m.save(map_name)
    print(f"Saved {num_schools} schools to {map_name}")
    print("="*40)
    print(f"Completed operation: save map")
    print("="*40)

def main(args):
    base_paginations = download_paginations(args)
    base_school_pages = download_school_pages(args, base_paginations)
    info_file = read_school_info(args, base_school_pages)
    save_map(args, info_file)
if __name__=='__main__':
    args = argparse_args()
    main(args)