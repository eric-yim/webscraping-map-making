
import glob, os, json
from util.washington_schools_util import WashingtonSchools

SCHOOL_HTMLS = "school_htmls/"
ALL_INFO_SAVE = "washington_schools_info.json"

def get_school_info(fpath):
    
    return WashingtonSchools.get_info(fpath)
    
        
# def save_all(all_info):
#     json.dump(all_info, open(ALL_INFO_SAVE, 'w', indent=2))
#     print(f"Saved to {ALL_INFO_SAVE}")
def save_info(info):
    my_dump = json.dumps(info)
    with open(ALL_INFO_SAVE, 'a') as f:
        f.write(my_dump)
        f.write('\n')

def get_listing():
    return sorted(glob.glob(os.path.join(SCHOOL_HTMLS, "*.html")))
def main():
    listing = get_listing()
    all_info = []
    for item in listing:
        print(f"Processing {item}")
        info = get_school_info(item)
        info['local_file'] = item
        save_info(info)
    # save_all(all_info)
    
if __name__=="__main__":
    main()