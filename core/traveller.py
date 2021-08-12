from mysql import connector
import datetime
from geopy.geocoders import Nominatim


class Traveller:
    def __init__(self, baggage_weight_spike_list, name, contact, address):
        self.db = connector.connect(host='127.0.0.1', user='root', passwd='ansh1Rutu')
        self.mycursor = self.db.cursor()
        self.name = name
        self.contact = contact
        self.baggage_spikes = ''
        self.total_weight = 0
        for i in baggage_weight_spike_list:
            self.baggage_spikes = self.baggage_spikes + (str(i) + ", ")
            self.total_weight = self.total_weight + i
        self.entry_time = datetime.datetime.now().strftime("%H:%M:%S, %m/%d/%Y")
        self.curr_loc = self.get_address(address[0], address[1])
        self.mycursor.execute("insert into TravellerDetails.travellers (name, contact_no, weight_spikes, "
                              "total_weight, entry_time, pickup_loc) values ('{}', '{}', '{}', '{}', '{}', '{}');"
                              "".format(self.name,
                                        self.contact,
                                        self.baggage_spikes,
                                        self.total_weight,
                                        self.entry_time,
                                        self.curr_loc
                                        )
                              )
        self.db.commit()
        self.mycursor.execute("Select MAX(id) from TravellerDetails.travellers;")
        self.traveller_id = int(self.mycursor.fetchone()[0])
        self.exit_time = ''

    def end_ride(self):
        self.exit_time = datetime.datetime.now().strftime("%H:%M:%S, %m/%d/%Y")
        self.mycursor.execute("UPDATE TravellerDetails.travellers SET exit_time = '{}' Where id = {}"
                              "".format(self.exit_time, self.traveller_id))

    def get_address(self, lat, long, data='display_name'):
        # TODO: Implement GPS interface & remove parameters
        locator = Nominatim(user_agent='google')
        coordinates = str(lat) + ',' + str(long)
        location = locator.reverse(coordinates)
        return location.raw[data]

