from pymongo import MongoClient
from datetime import datetime

DB_URI = 'mongodb://welltoryuser:welltorypassword99__**@api.welltory.com:27017/{}'.format('test')

conn = MongoClient(DB_URI)
db = conn['test']



db.collection_names()


def merge_two_dicts(x, y):
    z = x.copy()
    z.update(y)
    return z


def get_value(key, dictionary):
    if key in dictionary.keys():
        return dictionary[key]
    else:
        return None


def get_period(dt):
    h = dt.hour
    if h > 5:
        if h < 12:    #6-11
            return 1
        elif h < 20:  #12-19
            return 2
    return 3



def add_values(dict_to_append, date_val, period_val, l):
    if date_val not in dict_to_append.keys():
        dict_to_append[date_val] = {}
    if period_val not in dict_to_append[date_val].keys():
        dict_to_append[date_val][period_val] = []
    dict_to_append[date_val][period_val].append(l)
    return dict_to_append



users = {}
for user in db[u'users'].find():
    uid = user[u'email']
    line = {}
    for _k in [u'username', u'wid', u'gender', u'birthday', u'weight', u'height', u'problems']:
        line[_k] = get_value(_k, user)
    users[uid] = line
    users[uid]['data'] = {}


user_email = u'andrej.lazarev@gmail.com'

user_email = u'ktrn0509@gmail.com'


for data in db[u'data'].find({u'email':user_email}):
    if u'entryType' in data.keys():
        if data[u'entryType'] == 'sleep':
            print (data)

        if data[u'entryType'] == 'rrData':
            if 'statistics' in data.keys():
                stats = data[u'statistics']
                date = data['timeStart'].strftime('%Y-%m-%d')
                period = get_period(data['timeStart'])
                l = {
                    'rr_time': data['timeStart'],
                    'pNN50': stats[u'pNN50'],
                    'bpm': stats[u'bpm'],
                    'FracDim': stats[u'FracDim'],
                    'lfhf': stats[u'lfhf'],
                    'SDANN': stats[u'SDANN'],
                    'HRVI': stats[u'HRVI'],
                    'SD2': stats[u'SD2'],
                    'rMSSD': stats[u'rMSSD'],
                    'SD1': stats[u'SD1'],
                    'hf': stats[u'hf'],
                    'vlf': stats[u'vlf'],
                    'ApEn': stats[u'ApEn'],
                    'SDNNIND': stats[u'SDNNIND'],
                    'ulf': stats[u'ulf'],
                    'stress': stats[u'stress'],
                    'TINN': stats[u'TINN'],
                    'Power': stats[u'Power'],
                    'STDRR': stats[u'STDRR'],
                    'lf': stats[u'lf'],
                    'vegetative': stats[u'vegetative']}
                add_values(users[uid]['data'], date, period, l)


for data in db[u'data'].find():
    if u'entryType' in data.keys():
        if data[u'entryType'] == 'geo':      # NOTE THAT IF DAY IS NOT IN DICT NO LOCATION WILL BE ADDED
            if not data[u'timeEnd'].year > datetime.now().year:
                date = data['timeStart'].strftime('%Y-%m-%d')
                period = get_period(data['timeStart'])
                dstart = data[u'timeStart'].day
                dend = data[u'timeEnd'].day
                if dstart < dend:
                    day_break = datetime(data[u'timeStart'].year, data[u'timeStart'].month, data[u'timeStart'].day + 1)
                    day_break_str = day_break.strftime('%Y-%m-%d')
                    h1 = (day_break - data[u'timeStart']).seconds/ 3600
                    h2 = (data[u'timeEnd'] - day_break).seconds/ 3600
                    for prd in users[uid]['data'][date].iterkeys():
                        for row in users[uid]['data'][date][prd]:
                            if data[u'address'] in row.keys():
                                row[data[u'address']] += h1
                            else:
                                row[data[u'address']] = h1
                    for prd in users[uid]['data'][day_break_str].keys():
                        for row in users[uid]['data'][day_break_str][prd]:
                            if data[u'address'] in row.keys():
                                row[data[u'address']] += h2
                            else:
                                row[data[u'address']] = h2
                else:
                    h1 = (data[u'timeEnd'] - data[u'timeStart']).seconds/ 3600
                    for prd in users[uid]['data'][date].iterkeys():
                        for row in users[uid]['data'][date][prd]:
                            if data[u'address'] in row.keys():
                                row[data[u'address']] += h1
                            else:
                                row[data[u'address']] = h1

            print (data[u'timeStart'], data[u'timeEnd'], data[u'address'])


        elif data[u'entryType'] == 'weather':
            tags = [u'lunarPhase', u'weather', u'main', u'wind', u'clouds']
            if len([tag for tag in tags if tag not in data.keys()]) == 0:
                lunar = data[u'lunarPhase']
                weather = data[u'weather']
                main = data[u'main']
                wind = data[u'wind']
                clouds = data[u'clouds']
                date = data['timeStart'].strftime('%Y-%m-%d')
                period = get_period(data['timeStart'])

                l = {
                    'lunar_diff': lunar[u'diff'],
                    'temp': main[u'temp'],
                    'pressure': main[u'pressure'],
                    'humidity': main[u'humidity'],
                    'wind_speed': wind[u'speed'],
                    'wind_deg': wind[u'deg'],
                    'lunar_diff': clouds[u'all']}

                if date not in users[uid]['data']:
                    users[uid]['data'][date] = {}
                if period not in users[uid]['data'][date]:
                    users[uid]['data'][date][period] = []
                    users[uid]['data'][date][period].append(l)
                else:
                    all_vars = [abs((i['rr_time'] - data['timeStart']).seconds) for i in users[uid]['data'][date][period]]
                    min_delta = min(all_vars)
                    min_index = all_vars.index(min_delta)
                    users[uid]['data'][date][period][min_index] = merge_two_dicts(l, users[uid]['data'][date][period][min_index])


for data in db[u'data'].find({u'entryType':'weight'}):
    if data[u'entryType'] == 'weight':
        date = data['timeStart'].strftime('%Y-%m-%d')
        weight = data['value']
        users[uid]['data'][date] = {}
        break
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
            # print (data[u'timeStart'], data[u'timeEnd'], data[u'calories'], data[u'carbohydrate'], data[u'fat'],
            # data[u'protein'], data[u'sodium'], data[u'sugar'], data[u'fiber'], data[u'saturatedFat'],
            # data[u'monounsaturatedFat'], data[u'polyunsaturatedFat'], data[u'cholesterol'], data[u'vitaminA'],
            # data[u'vitaminC'], data[u'calcium'], data[u'iron'], data[u'potassium'])
            pass


        elif data[u'entryType'] == 'meal':
            # print (data[u'entryType'])
            # print (data[u'timeStart'], data[u'timeEnd'], data[u'calories'], data[u'carbohydrate'], data[u'fat'],
            # data[u'protein'], data[u'sodium'], data[u'sugar'], data[u'fiber'], data[u'saturatedFat'],
            # data[u'monounsaturatedFat'], data[u'polyunsaturatedFat'], data[u'cholesterol'], data[u'vitaminA'],
            # data[u'vitaminC'], data[u'calcium'], data[u'iron'], data[u'potassium'])
            pass


        elif data[u'entryType'] == 'heart_rate':
            # print (data[u'entryType'])
            # print (data[u'timeStart'], data[u'value'])
            pass


        elif data[u'entryType'] == 'body_fat':
            # print (data[u'entryType'])
            # print (data[u'timeStart'], data[u'value'])
            pass


        elif data[u'entryType'] == 'bmi':
            # print (data[u'entryType'])
            # print (data[u'timeStart'], data[u'value'])
            pass


        elif data[u'entryType'] == 'blood_pressure':
            # print (data[u'entryType'])
            # print (data[u'timeStart'], data[u'heartRate'], data[u'systolic'], data[u'diastolic'])
            pass


        elif data[u'entryType'] == 'blood_glucose':
            # print (data[u'entryType'])
            # print (data[u'timeStart'], data[u'value'])
            pass


        elif data[u'entryType'] == 'blood_oxygen':
            # print (data[u'entryType'])
            # print (data[u'timeStart'], data[u'value'])
            pass


        elif data[u'entryType'] == 'activity':
            # print (data[u'entryType'])
            # print (data[u'timeStart'], data[u'duration'], data[u'distance'], data[u'steps'], data[u'calories'])
            pass


        elif data[u'entryType'] == 'computer_activity':
            # print (data[u'entryType'])
            # print (data[u'timeStart'], data[u'total_hours'], data[u'very_productive_hours'], data[u'productive_hours'], data[u'neutral_hours'], data[u'distracting_hours'],
            # data[u'very_distracting_hours'], data[u'all_productive_hours'], data[u'all_distracting_hours'], data[u'uncategorized_hours'], data[u'business_hours'],
            # data[u'communication_and_scheduling_hours'], data[u'social_networking_hours'], data[u'design_and_composition_hours'], data[u'entertainment_hours'], data[u'news_hours'],
            # data[u'software_development_hours'], data[u'reference_and_learning_hours'], data[u'shopping_hours'], data[u'utilities_hours'], data[u'total_duration_formatted'],
            # data[u'software_development_hours'], data[u'reference_and_learning_hours'], data[u'shopping_hours'], data[u'utilities_hours'], data[u'total_duration_formatted'])
            pass


        elif data[u'entryType'] == 'air_oxygen':
            # print (data[u'entryType'])
            # print (data[u'timeStart'], data[u'value'])
            pass



