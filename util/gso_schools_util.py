from bs4 import BeautifulSoup
from util.geo_util import OpenStreetMap
import urllib.parse
class GsoSchools:
    @staticmethod
    def get_url(soup):
        canonical_link = soup.find('link', {'rel': 'canonical'})
        # Check if a canonical link was found and print its href attribute
        assert canonical_link
        canonical_href = canonical_link.get('href')
        assert canonical_href is not None, "Cant find link"
        return canonical_href
    @staticmethod
    def get_street_address(soup):
        # Get address
        target_divs = soup.find_all('div', class_='contact-row small-text')
        assert len(target_divs)==1, "Cant find address"
        span_items = target_divs[0].find_all('span')
        address = ', '.join([span.text for span in span_items])
        return address
    @staticmethod
    def get_scores(soup):

        # Find scores
        bar_graph_unified_divs = soup.find_all('div', class_='bar-graph-unified')

        # Loop through and print the text of each matching div
        SUBJECTS = {'English', 'Math', 'Science'}
        scores = {}
        for div in bar_graph_unified_divs:
            spans = div.find_all('span')
            subject = None
            for span in spans:
                if span.text in SUBJECTS:
                    subject = span.text
                    break
            if subject is None:
                continue
            perc_divs = div.find_all('div', class_ = 'percentage')
            assert len(perc_divs)==1
            scores[subject]=perc_divs[0].text
        assert len(scores)==len(SUBJECTS), "Cant find scores"
        return scores
    @staticmethod
    def get_info(fpath):
        address = urllib.parse.unquote(os.path.split(fpath)[1])

        with open(fpath, 'r') as f:
            html_content = f.read()
        soup = BeautifulSoup(html_content, 'html.parser')
        info = {}
        try:
            url = GsoSchools.get_url(soup)
            info['url']=url
        except:
            print(f"Unable to find URL for {fpath}")
        
        # try:
        #     address = GsoSchools.get_street_address(soup)
        #     info['address']=address
        # except:
        #     print(f"Unable to find Address for {fpath}")

        try:
            scores = GsoSchools.get_scores(soup)
            info['scores']=scores
        except:
            print(f"Unable to find Scores for {fpath}")

        if 'address' in info:
            try:
                location = OpenStreetMap.get_location_from_address(info['address'])
                info['location']=location
            except:
                print(f"Unable to find location for {address}")

        return info