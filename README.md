## Scrape Data from Web and Display it in a Map

### Installation
```
pip install folium
pip install selenium
pip install bs4
```

Folium is for maps. Selenium and bs4 are for scraping

### Order of Operations

I ran the files in this order:

Download the file links on a number of pages
```
download_html.py
```
Go to each school link and download the page
```
download_html_each_school.py
```
Get info about each school (address, scores).
```
read_school_info.py
```
Create a map
```
plot_schools.py
```
