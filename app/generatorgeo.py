import json
from geopy.geocoders import Nominatim

geolocator = Nominatim(user_agent="my_app")

mesta = [
    "Benešov", "Beroun", "Blansko", "Brno", "Bruntál", "České Budějovice", "Český Krumlov", 
    "Cheb", "Hodonín", "Hradec Králové", "Jablonec nad Nisou", "Jičín", "Karlovy Vary", 
    "Kladno", "Kroměříž", "Kutná Hora", "Litoměřice", "Louny", "Mělník", "Mladá Boleslav", 
    "Nymburk", "Ostrava", "Pardubice", "Písek", "Plzeň", "Prachatice", "Praha 2", "Praha 3", 
    "Praha 9", "Přerov", "Prostějov", "Rakovník", "Rychnov nad Kněžnou", "Semily", 
    "Sokolov", "Strakonice", "Šumperk", "Tábor", "Tachov", "Teplice", "Třebíč", "Vsetín", 
    "Vyškov", "Zlín", "Znojmo"
]

souradnice_mest = {}

for mesto in mesta:
    location = geolocator.geocode(mesto)
    if location:
        souradnice_mest[mesto] = {"lat": location.latitude, "lon": location.longitude}

# Uložení souřadnic do JSON souboru v kořenovém adresáři
with open("data/souradnice_mest.json", "w") as json_file:
    json.dump(souradnice_mest, json_file)

print("Soubor 'souradnice_mest.json' byl úspěšně uložen.")

