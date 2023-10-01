import folium
"""
Possible Colors 
{'purple', 'green', 'lightblue', 
'blue', 'gray', 'beige', 
'lightgreen', 'orange', 'lightred', 
'cadetblue', 'red', 'lightgray', 
'darkblue', 'white', 'darkred', 
'pink', 'black', 'darkgreen', 'darkpurple'}
"""
COLOR_MAPPING = color_mapping = {
    1: 'darkred',
    2: 'red',
    3: 'orange',
    4: 'green',
    5: 'lightgreen',
    6: 'lightblue'
}
class FoliumUtil:
    @staticmethod
    def get_colored_icon(score):
        color = COLOR_MAPPING.get(score,'gray')
        return folium.Icon(color=color)