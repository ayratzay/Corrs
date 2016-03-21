from pymongo import MongoClient
import pandas as pd
import datetime
import dateutil
import numpy as np
import  pytz
from sklearn import preprocessing
from vars import data_types
from relmatrix import discrete_coeff, binary_coeff

def get_row(delta_day, period = None):
    first_per = delta_day * 3
    if period:
        return first_per + period
    else:
        return [first_per, first_per + 1, first_per + 2]


def get_period(dt):
    h = dt.hour
    if h > 5:
        if h < 12:    #6-11
            return 1
        elif h < 20:  #12-19
            return 2
    return 3


def parse_dates(series_object):
    new_dates = []
    for index, value in series_object.iteritems():
        if isinstance(value, datetime.date):
            if value.tzinfo:
                new_dates.append(value.astimezone(pytz.UTC).replace(tzinfo=None))
            else:
                new_dates.append(value)
        elif isinstance(value, int):
            new_dates.append(datetime.datetime.fromtimestamp(value))
        elif isinstance(value, unicode):
            dt = dateutil.parser.parse(value)
            if dt.tzinfo:
                new_dates.append(dt.astimezone(pytz.UTC).replace(tzinfo=None))
            else:
                new_dates.append(dt)
        else:
            new_dates.append(datetime.datetime(1900, 1, 1)) # dumbing data

    return pd.Series(new_dates)



def parse_time(s):
    if isinstance(s, float):
        return s
    elif isinstance(s, str):
        return int(s.split(':')[0]) * 60 + int(s.split(':')[1])
    else:
        return 0



def parse_float(f):
    if isinstance(f, float):
        return f
    elif isinstance(f, unicode):
        return float(f.strip('%'))/100
    else:
        return 0

DB_URI = 'mongodb://welltoryuser:welltorypassword99__**@api.welltory.com:27017/{}'.format('test')
conn = MongoClient(DB_URI)
db = conn['test']

# db.collection_names()

data_columns = [
        u'stress', u'vegetative', u'pNN50', u'bpm', u'FracDim', u'Power', u'hf', u'lf', u'lfhf', u'vlf', u'ulf', u'SDANN', u'HRVI', u'SD1', u'SD2', u'rMSSD', u'ApEn', u'SDNNIND', u'TINN', u'STDRR',
        u'Mean HR', u'HR STD', u'beats', u'madrr', u'stdhr', u'meanhr', u'irrr', u'maxhr', u'sdnnidx', u'minhr', u'meanrr', u'stress_out',
        u'diff', u'humidity', u'pressure', u'temp', u'temp_max', u'deg', u'speed', u'all', u'temp_min', u'grnd_level', u'sea_level',
        u'weight', u'height', u'heart_rate', u'body_fat', u'bmi', u'systolic', u'diastolic', u'blood_glucose', u'blood_oxygen', u'air_oxygen',
        u'duration', u'distance', u'steps', u'calories',
        'calories_ate','carbohydrate','fat','protein','sodium','sugar','fiber','saturatedFat','monounsaturatedFat','polyunsaturatedFat', 'cholesterol','vitaminA','vitaminC','calcium','iron','potassium',
        'timeAsleep', 'timeAwake', 'efficiency', 'timeToFallAsleep', 'timeAfterWakeup', 'timeInBed',
        'business_percentage', 'communication_and_scheduling_percentage', 'social_networking_percentage', 'design_and_composition_percentage','entertainment_percentage',
        'news_percentage', 'software_development_percentage','reference_and_learning_percentage','shopping_percentage','utilities_percentage','total_hours']
data_columns = [c.lower() for c in data_columns]


cursor = db['users'].find()
df_users =  pd.DataFrame(list(cursor))
df_users = df_users[[u'username', u'wid', u'gender', u'birthday', u'weight', u'height', u'problems', u'email']]

# user_email = u'andrej.lazarev@gmail.com'

for user in df_users.itertuples():
    user_email = user.email
    cursor = db['data'].find({u'email':user_email})
    df_data =  pd.DataFrame(list(cursor))
    df_data.columns = [colname.lower() for colname in df_data.columns]

    if df_data.shape[0] != 0 and 'entrytype' in df_data.columns: #check if df_shape is more than 0
        df_data['timestart'] = parse_dates(df_data['timestart'])
        df_data['timeend'] = parse_dates(df_data['timeend'])

        df_data = df_data[~((df_data['entrytype'].isnull()) | (df_data['timestart'].isnull()) | (df_data['timeend'].isnull()))] #validate date
        df_data = df_data[((df_data['timestart'].dt.year < 2020) & (df_data['timestart'].dt.year > 2015))] #validate date

        if df_data.shape[0] != 0 and 'entrytype' in df_data.columns: #check if df_shape is more than 0

            day_min = df_data['timestart'].min().date()
            day_max = df_data['timestart'].max().date()
            total_days = (day_max - day_min).days + 1
            total_rows = total_days * 3

            if total_days > 4:

                data_table = np.zeros((total_rows, len(data_columns)))
                addresses = []

                loc_table = np.zeros((total_rows, 0))
                if 'address' in df_data.keys():
                    addresses = list(df_data['address'].unique())
                    loc_table = np.zeros((total_rows, len(addresses)))

                    for row in df_data.itertuples():
                        if row.entrytype == 'geo':
                            ind = get_row((row.timestart.date() - day_min).days)
                            try:
                                delta = (row.timeend - row.timestart).seconds / 60
                            except:
                                delta = 0
                            for i in ind:
                                loc_table[i, addresses.index(row.address)] += delta


                for row in df_data.itertuples():
                    if row.entrytype == 'rrdata':
                        if 'statisitcs' in row._fields:
                            ind = get_row((row.timestart.date() - day_min).days , get_period(row.timestart))
                            for key, value in row.statistics.iteritems():
                                col = (data_columns.index(key.lower()))
                                data_table[ind, col] = value


                for row in df_data.itertuples():
                    if row.entrytype == 'weather':
                        if 'lunarphase' in row._fields:
                            ind = get_row((row.timestart.date() - day_min).days , get_period(row.timestart))
                            for key, value in row.main.iteritems():
                                try:
                                    col = (data_columns.index(key))
                                    data_table[ind, col] = value
                                except:
                                    pass
                            for key, value in row.wind.iteritems():
                                try:
                                    col = (data_columns.index(key))
                                    data_table[ind, col] = value
                                except:
                                    pass
                            for key, value in row.clouds.iteritems():
                                try:
                                    col = (data_columns.index(key))
                                    data_table[ind, col] = value
                                except:
                                    pass

                for row in df_data.itertuples():
                    if row.entrytype == 'weight':
                        ind = get_row((row.timestart.date() - day_min).days)
                        for i in ind:
                            col = (data_columns.index('weight'))
                            try:
                                data_table[i, col] = row.value #there might be no row value
                            except:
                                pass


                for row in df_data.itertuples():
                    if row.entrytype == 'height':
                        ind = get_row((row.timestart.date() - day_min).days)
                        for i in ind:
                            col = (data_columns.index('height'))
                            try:
                                data_table[i, col] = row.value #there might be no row value
                            except:
                                pass


                for row in df_data.itertuples():
                    if row.entrytype == 'heart_rate':
                        ind = get_row((row.timestart.date() - day_min).days)
                        for i in ind:
                            col = (data_columns.index('heart_rate'))
                            try:
                                data_table[i, col] = row.value #there might be no row value
                            except:
                                pass


                for row in df_data.itertuples():
                    if row.entrytype == 'body_fat':
                        ind = get_row((row.timestart.date() - day_min).days)
                        for i in ind:
                            col = (data_columns.index('body_fat'))
                            try:
                                data_table[i, col] = row.value #there might be no row value
                            except:
                                pass


                for row in df_data.itertuples():
                    if row.entrytype == 'bmi':
                        ind = get_row((row.timestart.date() - day_min).days)
                        for i in ind:
                            col = (data_columns.index('bmi'))
                            try:
                                data_table[i, col] = row.value #there might be no row value
                            except:
                                pass


                for row in df_data.itertuples():
                    if row.entrytype == 'blood_pressure':
                        ind = get_row((row.timestart.date() - day_min).days, get_period(row.timestart))
                        col = (data_columns.index('systolic'))
                        data_table[ind, col] = row.systolic
                        col = (data_columns.index('diastolic'))
                        data_table[ind, col] = row.diastolic


                for row in df_data.itertuples():
                    if row.entrytype == 'blood_glucose':
                        ind = get_row((row.timestart.date() - day_min).days, get_period(row.timestart))
                        col = (data_columns.index('blood_glucose'))
                        data_table[ind, col] = row.value


                for row in df_data.itertuples():
                    if row.entrytype == 'blood_oxygen':
                        ind = get_row((row.timestart.date() - day_min).days, get_period(row.timestart))
                        col = (data_columns.index('blood_oxygen'))
                        data_table[ind, col] = row.value



                for row in df_data.itertuples():
                    if row.entrytype == 'blood_oxygen':
                        ind = get_row((row.timestart.date() - day_min).days, get_period(row.timestart))
                        col = (data_columns.index('blood_oxygen'))
                        data_table[ind, col] = row.value


                for row in df_data.itertuples():
                    if row.entrytype == 'activity':
                        ind = get_row((row.timestart.date() - day_min).days)
                        col = (data_columns.index(u'duration'))
                        data_table[i, col] = row.duration
                        col = (data_columns.index('distance'))
                        data_table[i, col] = row.distance
                        col = (data_columns.index('steps'))
                        data_table[i, col] = row.steps
                        col = (data_columns.index('calories'))
                        data_table[i, col] = row.calories


                for row in df_data.itertuples():
                    if row.entrytype == 'air_oxygen':
                        ind = get_row((row.timestart.date() - day_min).days, get_period(row.timestart))
                        col = (data_columns.index('air_oxygen'))
                        data_table[ind, col] = row.value


                for row in df_data.itertuples():
                    if row.entrytype == 'meal':
                        ind = get_row((row.timestart.date() - day_min).days)
                        for i in ind:
                            col = (data_columns.index('calories_ate'))
                            data_table[i, col] += row.calories
                            col = (data_columns.index('carbohydrate'))
                            data_table[i, col] += row.carbohydrate
                            col = (data_columns.index('fat'))
                            data_table[i, col] += row.fat
                            col = (data_columns.index('protein'))
                            data_table[i, col] += row.protein
                            col = (data_columns.index('sodium'))
                            data_table[i, col] += row.sodium
                            col = (data_columns.index('sugar'))
                            data_table[i, col] += row.sugar
                            col = (data_columns.index('fiber'))
                            data_table[i, col] += row.fiber
                            col = (data_columns.index('saturatedfat'))
                            data_table[i, col] += row.saturatedfat
                            col = (data_columns.index('monounsaturatedfat'))
                            data_table[i, col] += row.monounsaturatedfat
                            col = (data_columns.index('polyunsaturatedfat'))
                            data_table[i, col] += row.polyunsaturatedfat
                            col = (data_columns.index('cholesterol'))
                            data_table[i, col] += row.cholesterol
                            col = (data_columns.index('vitamina'))
                            data_table[i, col] += row.vitamina
                            col = (data_columns.index('vitaminc'))
                            data_table[i, col] += row.vitaminc
                            col = (data_columns.index('calcium'))
                            data_table[i, col] += row.calcium
                            col = (data_columns.index('iron'))
                            data_table[i, col] += row.iron
                            col = (data_columns.index('potassium'))
                            data_table[i, col] += row.potassium


                for row in df_data.itertuples():
                    if row.entrytype == 'sleep':
                        ind = get_row((row.timeend.date() - day_min).days)
                        for i in ind:
                            if 'timeasleep' in row._fields:
                                col = (data_columns.index('timeasleep'))
                                data_table[i, col] = row.timeasleep
                            if 'timeawake' in row._fields:
                                col = (data_columns.index('timeawake'))
                                data_table[i, col] = row.timeawake
                            col = (data_columns.index('efficiency'))
                            data_table[i, col] = parse_float(row.efficiency)
                            if 'timetofallasleep' in row._fields:
                                col = (data_columns.index('timetofallasleep'))
                                data_table[i, col] = row.timetofallasleep
                            if 'timeafterwakeup' in row._fields:
                                col = (data_columns.index('timeafterwakeup'))
                                data_table[i, col] = row.timeafterwakeup
                            col = (data_columns.index('timeinbed'))
                            data_table[i, col] = parse_time(row.timeinbed)


                for row in df_data.itertuples():
                    if row.entrytype == 'computer_activity':
                        ind = get_row((row.timeend.date() - day_min).days)
                        for i in ind:
                            col = (data_columns.index('business_percentage'))
                            data_table[i, col] = row.business_percentage
                            col = (data_columns.index('communication_and_scheduling_percentage'))
                            data_table[i, col] = row.communication_and_scheduling_percentage
                            col = (data_columns.index('social_networking_percentage'))
                            data_table[i, col] = row.social_networking_percentage
                            col = (data_columns.index('design_and_composition_percentage'))
                            data_table[i, col] = row.design_and_composition_percentage
                            col = (data_columns.index('entertainment_percentage'))
                            data_table[i, col] = row.entertainment_percentage
                            col = (data_columns.index('news_percentage'))
                            data_table[i, col] = row.news_percentage
                            col = (data_columns.index('software_development_percentage'))
                            data_table[i, col] = row.software_development_percentage
                            col = (data_columns.index('reference_and_learning_percentage'))
                            data_table[i, col] = row.reference_and_learning_percentage
                            col = (data_columns.index('shopping_percentage'))
                            data_table[i, col] = row.shopping_percentage
                            col = (data_columns.index('utilities_percentage'))
                            data_table[i, col] = row.utilities_percentage
                            col = (data_columns.index('total_hours'))
                            data_table[i, col] = row.total_hours

                print (day_min, total_days)

                table = np.hstack([data_table, loc_table])
                col_names = data_columns + addresses

                row_mask = table.sum(axis = 1) != 0
                table = table[row_mask, :]
                table.sum(axis = 0) != 0

                col_mask = table.sum(axis = 0) != 0
                table = table[:, col_mask]
                col_names = np.array(col_names)[col_mask]


                ###############

                n = 3  # number of days to take from past for each row
                table = np.hstack([table] + [np.vstack([table[n:], table[-n:]]) for i in range(1, n + 1 )]) # append n days before #does not concern day period
                col_names
                col_names_prev = [col + '_' + str(days_before) + 'dbefore' for days_before in range(1, n + 1) for col in col_names] # new colnames


                x_std = preprocessing.StandardScaler().fit_transform(table)

                for col in col_names:
                    if col in data_types.keys():
                        ind = np.where(col_names == col)
                        y =  table[:, ind].reshape(-1, 1)
                        x = x_std
                        x[:, ind] = 0
                        if data_types[col] == 'dis':
                            coeff = discrete_coeff(x, y)
                        elif data_types[col] == 'bin':
                            coeff = binary_coeff(x, y)

                        positive = col_names[np.where(coeff > 0)] ### output these values
                        negative = col_names[np.where(coeff < 0)] ### output these values
                        col ### output these values




#### output as text
### value1 arrow up value2 arrow down

### output as data
### dict{email: {val1: [val2, float], [val3, float], val2:[...], 'data':[list of obejcts _id which were used]}}





