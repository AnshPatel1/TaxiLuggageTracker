from mysql import connector
import datetime


class Trunk:
    def __init__(self, initial_value):
        self.initial_value = initial_value
        self.total_weight = 0 - self.initial_value
        self.active_travellers = {}  # {'name': [entry time, exit_time, pickup location, drop location, contact, pos_spikes, id]
        self.past_travellers = {}  # {'name': [entry time, exit_time, pickup location, drop location, contact, neg_spikes, id]
        self.db = connector.connect(host='127.0.0.1', user='root', passwd='ansh1Rutu')
        self.my_cursor = self.db.cursor()

    def remove_luggage(self, negative_spikes):
        self.refresh_traveller_list()
        total_removed_weight = 0
        for i in negative_spikes:
            total_removed_weight = total_removed_weight + i
        for name in self.active_travellers.keys():
            temp = 0
            for i in self.active_travellers[name][6]:
                temp = temp + i
            if temp - (temp*0.03) < total_removed_weight or temp + (temp*0.03) > total_removed_weight:
                return name, self.active_travellers[7]

    def refresh_traveller_list(self):
        if not self.db.is_connected():
            self.db.refresh()
        self.my_cursor.execute("SELECT name, entry_time, pickup_loc, drop_loc, contact_no, weight_spikes from "
                               "TravellerDetails.travellers WHERE exit_time IS NULL;")
        traveller_details = self.my_cursor.fetchall()
        for traveller in traveller_details:
            spikes = list(traveller[6].split(','))
            self.active_travellers[traveller[0]] = [traveller[1],
                                                    traveller[2],
                                                    traveller[3],
                                                    traveller[4],
                                                    traveller[5],
                                                    spikes,
                                                    traveller[7]
                                                    ]
        self.my_cursor.execute("SELECT name, entry_time, pickup_loc, drop_loc, contact_no, weight_spikes, id from "
                               "TravellerDetails.travellers WHERE exit_time IS NOT NULL;")
        traveller_details = self.my_cursor.fetchall()
        for traveller in traveller_details:
            spikes = list(traveller[6].split(','))
            self.past_travellers[traveller[0]] = [traveller[1],
                                                  traveller[2],
                                                  traveller[3],
                                                  traveller[4],
                                                  traveller[5],
                                                  spikes,
                                                  traveller[7]
                                                  ]
