import  datetime
import pandas as pd
from sklearn import preprocessing, linear_model, metrics
from sklearn.multiclass import OneVsRestClassifier
from sklearn import cross_validation
import numpy as np
from sklearn.dummy import DummyClassifier, DummyRegressor


def prediction_is_valuable(scores1, scores2, maximize = True):
    if maximize:
        if scores1.mean() > scores2.mean():
            return True
    if not maximize:
        if scores1.mean() > scores2.mean():
            return True
    return False


def index_columns(column_name, dataframe_columns, datatypes):
    cols = []
    cols.append(list(dataframe_columns).index(column_name))
    for c in datatypes[column_name]['siblings']:
        cols.append(list(dataframe_columns).index(c))
    return cols


data_types = {
u'Sleep_end': {'dt': 'multi', 'siblings': []},
u'day_period': {'dt': 'multi', 'siblings': []},
u'HRVI': {'dt': 'dis', 'siblings': [u'vegetative', u' stress_level', u'stress', u'rMSSD', u'SD1', u'SD2', u'rMSSD', u'TINN', u'SDNN', u'pNN50']},
u'SD1': {'dt': 'dis', 'siblings': [u'vegetative', u' stress_level', u'stress', u'rMSSD', u'SD2', u'rMSSD', u'TINN', u'SDNN', u'HRVI', u'pNN50']},
u'SD2': {'dt': 'dis', 'siblings': [u'vegetative', u' stress_level', u'stress', u'rMSSD', u'SD1', u'rMSSD', u'TINN', u'SDNN', u'HRVI', u'pNN50']},
u'SDNN': {'dt': 'dis', 'siblings': [u'vegetative', u' stress_level', u'stress', u'rMSSD', u'SD1', u'SD2', u'rMSSD', u'TINN', u'HRVI', u'pNN50']},
u'TINN': {'dt': 'dis', 'siblings': [u'vegetative', u' stress_level', u'stress', u'rMSSD', u'SD1', u'SD2', u'rMSSD', u'SDNN', u'HRVI', u'pNN50']},
u'hf': {'dt': 'dis', 'siblings': []},
u'lf': {'dt': 'dis', 'siblings': []},
u'lfhf': {'dt': 'dis', 'siblings': []},
u'pNN50': {'dt': 'dis', 'siblings': [u'vegetative', u' stress_level', u'stress', u'rMSSD', u'SD1', u'SD2', u'rMSSD', u'TINN', u'SDNN', u'HRVI']},
u'rMSSD': {'dt': 'dis', 'siblings': [u'vegetative', u' stress_level', u'stress', u'rMSSD', u'SD1', u'SD2',u'TINN', u'SDNN', u'HRVI', u'pNN50']},
u'stress': {'dt': 'dis', 'siblings': []},
u'ulf': {'dt': 'dis', 'siblings': []},
u'vlf': {'dt': 'dis', 'siblings': []},
u'vegetative': {'dt': 'dis', 'siblings': []},
u' stress_level': {'dt': 'dis', 'siblings': []},
u' heart_rate': {'dt': 'dis', 'siblings': []},
u'Sleep_quality': {'dt': 'dis', 'siblings': []},
u'Wakeup_mood': {'dt': 'multi', 'siblings': []},
u'Films': {'dt': 'bin', 'siblings': []},
u'Worked out': {'dt': 'bin', 'siblings': []},
u'Ate late': {'dt': 'bin', 'siblings': []},
u'Alhogol': {'dt': 'bin', 'siblings': []},
u'wakeup_time': {'dt': 'multi', 'siblings': []},
u'sleep_time': {'dt': 'dis', 'siblings': []},
u'slept_time': {'dt': 'multi', 'siblings': []},
u'withings_1': {'dt': 'dis', 'siblings': []},
u'stayed_home': {'dt': 'dis', 'siblings': []},
u'stayed_office': {'dt': 'dis', 'siblings': []},
u'stayed_workout': {'dt': 'dis', 'siblings': []},
u'commuting_time': {'dt': 'dis', 'siblings': []},
u'came_home': {'dt': 'dis', 'siblings': []},
u'came_work': {'dt': 'dis', 'siblings': []},
u'count': {'dt': 'dis', 'siblings': []},
u'Business': {'dt': 'dis', 'siblings': []},
u'Communication_Scheduling': {'dt': 'dis', 'siblings': []},
u'Design_Composition': {'dt': 'dis', 'siblings': []},
u'Entertainment': {'dt': 'dis', 'siblings': []},
u'News_Opinion': {'dt': 'dis', 'siblings': []},
u'Reference_Learning': {'dt': 'dis', 'siblings': []},
u'Shopping': {'dt': 'dis', 'siblings': []},
u'Social_Networking': {'dt': 'dis', 'siblings': []},
u'Software_Development': {'dt': 'dis', 'siblings': []},
u'Uncategorized': {'dt': 'dis', 'siblings': []},
u'Utilities': {'dt': 'dis', 'siblings': []},
u'lunarPhase': {'dt': 'dis', 'siblings': []},
u'temp ': {'dt': 'dis', 'siblings': []},
u'pressure ': {'dt': 'dis', 'siblings': []},
u'humidity ': {'dt': 'dis', 'siblings': []},
u'wind ': {'dt': 'dis', 'siblings': []},
u'clouds ': {'dt': 'dis', 'siblings': []},
u'precipitation ': {'dt': 'dis', 'siblings': []}}


df = pd.read_csv(r'data/to_plot1.csv')

df = df[df['UserId'] == 1]
df.drop(['UserId', 'Faked_Date', 'rr_time'], axis = 1, inplace = True)


df.columns = [u'Sleep_end', u'day_period', u'HRVI', u'SD1', u'SD2', u'SDNN', u'TINN',
       u'hf', u'lf', u'lfhf', u'pNN50', u'rMSSD', u'stress', u'ulf', u'vlf',
       u'vegetative', u' stress_level', u' heart_rate', u'Sleep_quality',
       u'Wakeup_mood', u'Films', u'Worked out', u'Ate late', u'Alhogol',
       u'wakeup_time', u'sleep_time', u'slept_time', u'withings_1',
       u'stayed_home', u'stayed_office', u'stayed_workout', u'commuting_time',
       u'came_home', u'came_work', u'count', u'Business',
       u'Communication_Scheduling', u'Design_Composition', u'Entertainment',
       u'News_Opinion', u'Reference_Learning', u'Shopping',
       u'Social_Networking', u'Software_Development', u'Uncategorized',
       u'Utilities', u'lunarPhase', u'temp ', u'pressure ', u'humidity ',
       u'wind ', u'clouds ', u'precipitation ']


df['Sleep_end'] = pd.to_datetime(df['Sleep_end'], format='%Y-%m-%d')

#add 3 days before


df = df.set_index(['Sleep_end', 'day_period'], drop = False)
df = df.drop('Sleep_end', axis = 1)

new_tbl = []
for index, row in df.iterrows():
    new_row = np.array([], dtype=np.float64)
    day_iter = 0
    base_day = row.values
    new_row = np.append(new_row, base_day)

    for d in range(1, 4):
        try:
            next_row = df.ix[index[0] - datetime.timedelta(days=d), index[1]].values
            new_row = np.append(new_row, base_day - next_row)
            base_day = next_row
        except:
            new_row = np.append(new_row, base_day - base_day)
    new_tbl.append(new_row)

n = 3
df_new = pd.DataFrame(new_tbl,
                    columns=list(df.columns) + [col + '_' + str(days_before) + 'dbefore' for days_before in range(1, n + 1) for col in df.columns],
                    index = df.index)

df_new = df_new.dropna(axis=0)
df = df.ix[df_new.index]



for i in df.columns:
    if i not in ['day_period']:
        x_std = preprocessing.StandardScaler().fit_transform(df_new)
        x_std[:, index_columns(i, df.columns, data_types)] = 0

        if data_types[i]['dt'] == 'dis':

            mdl = linear_model.Lasso(alpha=0.3)
            mdl_dummy = DummyRegressor(strategy='mean')

            y_temp = pd.DataFrame(df[i])
            y_std = preprocessing.StandardScaler().fit_transform(y_temp)

            scores_pred = cross_validation.cross_val_score(mdl, x_std, y_std, cv=5, scoring='mean_squared_error')
            scores_dummy = cross_validation.cross_val_score(mdl_dummy, x_std, y_std, cv=5, scoring='mean_squared_error')

            if prediction_is_valuable(scores_pred, scores_dummy, maximize = False):
                print (i, 'model works')
                print (scores_pred.mean(), scores_dummy.mean())
                mdl.fit(x_std, y_std)
                # mdl.score(x_std, y_std)
                # mdl.predict(x_std)
                print (df_new.columns [np.argsort(mdl.coef_)[-3:]], mdl.coef_[np.argsort(mdl.coef_)[-3:]])



        elif data_types[i]['dt'] == 'bin':

            mdl = linear_model.LogisticRegression(penalty='l1', C=0.9, solver='liblinear')
            mdl_dummy = DummyClassifier(strategy='most_frequent',random_state=0)

            y_temp = pd.DataFrame(df[i]).astype('int')
            y_std = y_temp.as_matrix().ravel()

            scores_pred = cross_validation.cross_val_score(mdl, x_std, y_std, cv=5, scoring='f1_weighted')
            scores_dummy = cross_validation.cross_val_score(mdl_dummy, x_std, y_std, cv=5, scoring='f1_weighted')

            if prediction_is_valuable(scores_pred, scores_dummy, maximize = True):
                print (i, 'model works')
                print (scores_pred.mean(), scores_dummy.mean())
                # mdl.fit(x_std, y_std)
                # mdl.coef_

        elif data_types[i]['dt'] == 'multi':

            mdl = linear_model.LogisticRegression(penalty='l2', C=0.9, multi_class='multinomial', solver='newton-cg')
            classif = OneVsRestClassifier(mdl)
            mdl_dummy = DummyClassifier(strategy='uniform',random_state=0)


            y_temp = pd.DataFrame(df[i]).astype('int')
            enc = preprocessing.OneHotEncoder(sparse=False)
            y_std = enc.fit_transform(y_temp)

            scores_pred = cross_validation.cross_val_score(classif, x_std, y_std, cv=5, scoring='f1_weighted')
            scores_dummy = cross_validation.cross_val_score(mdl_dummy, x_std, y_std, cv=5, scoring='f1_weighted')

            if prediction_is_valuable(scores_pred, scores_dummy, maximize = True):
                print (i, 'model works')
                print (scores_pred.mean(), scores_dummy.mean())



