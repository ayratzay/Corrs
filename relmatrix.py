from sklearn import preprocessing, linear_model
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


def discrete_coeff(x, y):
    mdl = linear_model.Lasso(alpha=0.3)
    mdl_dummy = DummyRegressor(strategy='mean')

    y_std = preprocessing.StandardScaler().fit_transform(y)

    scores_pred = cross_validation.cross_val_score(mdl, x, y_std, cv=5, scoring='mean_squared_error')
    scores_dummy = cross_validation.cross_val_score(mdl_dummy, x, y_std, cv=5, scoring='mean_squared_error')

    if prediction_is_valuable(scores_pred, scores_dummy, maximize = False):
        mdl.fit(x, y)
        return mdl.coef_
    else:
        return np.zeros(x.shape)


def binary_coeff(x, y):
        mdl = linear_model.LogisticRegression(penalty='l1', C=0.9, solver='liblinear')
        mdl_dummy = DummyClassifier(strategy='most_frequent',random_state=0)


        scores_pred = cross_validation.cross_val_score(mdl, x, y, cv=5, scoring='f1_weighted')
        scores_dummy = cross_validation.cross_val_score(mdl_dummy, x, y, cv=5, scoring='f1_weighted')

        if prediction_is_valuable(scores_pred, scores_dummy, maximize = True):
            mdl.fit(x, y)
            return mdl.coef_
        else:
            return np.zeros(x.shape)


