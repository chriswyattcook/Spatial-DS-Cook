mongo world_data --eval "db.dropDatabase()"
mongoimport --db world_data --collection terrorism       --type json --file globalterrorism.geojson       --jsonArray
