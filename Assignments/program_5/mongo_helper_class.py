from pymongo import MongoClient
import pprint as pp


class mongoHelper(object):
    def __init__(self):
        self.client = MongoClient()

        self.db_airports = self.client.world_data.airports
        self.db_cities = self.client.world_data.cities
        self.db_countries = self.client.world_data.countries
        self.db_earthquakes = self.client.world_data.earthquakes
        self.db_meteorites = self.client.world_data.meteorites
        self.db_states = self.client.world_data.states
        self.db_volcanos = self.client.world_data.volcanos


    def get_airports_in_poly(self,poly):
        """
        Get airports within some polygon
        Params:
            poly (object): geojson poly
        """
        state_airports = self.db_airports.find( { 'geometry.coordinates' : { '$geoWithin' : { '$geometry' : poly } } })

        ap_list = []
        for ap in state_airports:
            ap_list.append(ap)

        return ap_list

    def get_state_poly(self,state):
        state_poly = self.db_states.find_one({'properties.code' : state})
        return(state_poly['geometry']['coordinates'])

    def get_doc_by_keyword(self,db_name,field,key):

        if db_name == 'airports':
            res = self.db_airports.find({'properties.'+field : {'$regex' : ".*"+key+".*"}})
        else:
            res = self.states.find({field : {'$regex' : ".*"+key+".*"}})
        
        res_list = []
        for r in res:
            res_list.append(r)

        return res_list

    def get_coordinates(self, thingy):

        return(thingy['geometry']['coordinates'])

    def get_state_by_point(self,point):
        return self.db_states.find_one({'loc':{'$geoIntersects':{'$geometry':{ "type" : "Point","coordinates" : point }}}})

    def get_state_by_name(self,name):
        pass


def main():
    mh = mongoHelper()
    poly = mh.get_state_poly("la")
    #ap = mh.get_airports_in_poly(poly)
    bykey = mh.get_doc_by_keyword('airports','ap_iata','DFW')
    pp.pprint(bykey)


    # state = mh.get_state_by_point([-95.912512, 41.118327])
    # pp.pprint(state)

if __name__=='__main__':
    main()
