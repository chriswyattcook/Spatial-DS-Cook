mongoimport --db world_data --collection airports --type json --file geo_json/airports_combined.geojson --jsonArray
mongoimport --db world_data --collection countries --type json --file geo_json/countries_gj.geojson --jsonArray
mongoimport --db world_data --collection earthquakes --type json --file geo_json/earthquakes_gj.geojson --jsonArray
mongoimport --db world_data --collection meteorites --type json --file geo_json/meteorite-landings.geojson --jsonArray
mongoimport --db world_data --collection states --type json --file geo_json/states_gj.geojson --jsonArray
mongoimport --db world_data --collection volcanos --type json --file geo_json/volcanos_gj.geojson --jsonArray
mongoimport --db world_data --collection cities --type json --file geo_json/world_cities_gj.geojson --jsonArray