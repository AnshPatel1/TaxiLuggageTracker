from mysql import connector



db = connector.connect(host='127.0.0.1', user='root', passwd='ansh1Rutu')
my_cursor = db.cursor()
my_cursor.execute("SELECT name, entry_time, exit_time, pickup_loc, drop_loc, contact_no, weight_spikes from "
                               "TravellerDetails.travellers;")
raw_info = my_cursor.fetchall()
print(raw_info)

