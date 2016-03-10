from pymongo import MongoClient

DB_URI = 'mongodb://welltoryuser:welltorypassword99__**@api.welltory.com:27017/{}'.format('test')

conn = MongoClient(DB_URI)
db = conn['test']



db.collection_names()


def get_value(key, dictionary):
    if key in dictionary.keys():
        return dictionary[key]
    else:
        return None

users = {}
for user in db[u'users'].find():
    uid = user[u'email']
    line = {}
    for _k in [u'username', u'wid', u'gender', u'birthday', u'weight', u'height', u'problems']:
        line[_k] = get_value(_k, user)
    users[uid] = line


for data in db[u'data'].find():
    if u'entryType' in data.keys():
        if data[u'entryType'] == 'geo':
            pass
            # print (data[u'entryType'])
            # print (data[u'timeStart'], data[u'timeEnd'], data[u'latitude'], data[u'longitude'], data[u'address'])
        elif data[u'entryType'] == 'rrData':
            if 'statistics' in data.keys():
                stats = data[u'statistics']
                # print (data[u'entryType'])
                # print (data[u'timeStart'], stats[u'pNN50'], stats[u'bpm'], stats[u'FracDim'], stats[u'lfhf'],
                #         stats[u'SDANN'], stats[u'HRVI'], stats[u'SD2'], stats[u'rMSSD'],
                #         stats[u'SD1'], stats[u'hf'], stats[u'vlf'], stats[u'ApEn'],
                #         stats[u'SDNNIND'], stats[u'ulf'], stats[u'stress'],
                #         stats[u'TINN'], stats[u'Power'], stats[u'STDRR'], stats[u'lf'], stats[u'vegetative'])
        elif data[u'entryType'] == 'weather':                   ## does not work
            tags = [u'lunarPhase', u'weather', u'main', u'wind', u'clouds', u'rain', u'snow']
            if len([tag for tag in tags if tag not in data.keys()]) == 0:
                lunar = data[u'lunarPhase']
                weather = data[u'weather']
                main = data[u'main']
                wind = data[u'wind']
                clouds = data[u'clouds']
                rain = data[u'rain']
                snow = data[u'snow']
                # print (data[u'timeStart'], lunar[u'diff'], lunar[u'description'],
                #        weather[u'main'], weather[u'description'],
                #        main[u'temp'], main[u'pressure'], main[u'humidity'], main[u'temp_min'], main[u'temp_max'], main[u'sea_level'], main[u'grnd_level'],
                #        wind[u'speed'], wind[u'deg'],
                #        clouds[u'all'],
                #        rain[u'3h'],
                #        snow[u'3h'])

        elif data[u'entryType'] == 'weight':
            # print (data[u'entryType'])
            # print (data[u'timeStart'], data[u'value'])
            pass

        elif data[u'entryType'] == 'height':
            # print (data[u'entryType'])
            # print (data[u'timeStart'], data[u'value'])
            pass


        elif data[u'entryType'] == 'sleep':
            # print (data[u'entryType'])
            # print (data[u'timeStart'], data[u'timeEnd'], data[u'mainSleep'], data[u'timeAsleep'], data[u'timeAwake'],
            # data[u'efficiency'], data[u'timeToFallAsleep'], data[u'timeAfterWakeup'], data[u'timeInBed'], data[u'wakeUpMood'])
            pass

        elif data[u'entryType'] == 'meal':
            # print (data[u'entryType'])
            # print (data[u'timeStart'], data[u'timeEnd'], data[u'mainSleep'], data[u'timeAsleep'], data[u'timeAwake'],
            # data[u'efficiency'], data[u'timeToFallAsleep'], data[u'timeAfterWakeup'], data[u'timeInBed'], data[u'wakeUpMood'])
            pass

