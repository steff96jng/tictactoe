import jsonpickle
import random
import string
import os

def o2json(o) -> str:
    s = jsonpickle.encode(o)

    return s


def randomString(stringLength=20) -> str:
    """Generate a random string of fixed length """
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(stringLength))

class StatsProcessor(object):
    session = ""
    epoch_data = []

    def __init__(self, prefix = ""):
        self.session = prefix + randomString()
        self.start_new_epoch()

    def append_epoch_data(self, data):
        d = EpochData()
        d.data = data
        self.epoch_data.append(d)

    def export_json(self):
        file_path = 'data_export/stats_' + self.session + '.json'

        directory = os.path.dirname(file_path)
        if not os.path.exists(directory):
            os.makedirs(directory)
        
        json_file = open(file_path, "w+")
        json_file.write(o2json(self))
        json_file.close()
        print('Exported stats to ', file_path)

    def start_new_epoch(self):
        self.epoch_data = []




class EpochData(object):
    epoch_id = ""
    data = []

    def __init__(self):
        self.epoch_id = randomString(13)
    