import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression
from scipy import stats
from sklearn.feature_selection import f_regression
import statsmodels.api as sm

def predict_next_using_best_lin_model(input, p_value=0.2):
    lst = list(range(1, len(input) + 1))

    df = pd.DataFrame({'x1': lst,
                       'y': input})
    df['x2'] = df.x1 ** 2
    df['x3'] = df.x1 ** 3
    df['xlog'] = np.log10(df.x1)

    newdata = pd.DataFrame({'x1':[len(lst)+1]})
    newdata['x2'] = newdata['x1']**2
    newdata['x3'] = newdata['x1']**3
    newdata['xlog'] = np.log10(newdata['x1'])

    model = LinearRegression()

    lin_model = model.fit(df[['x1']],df['y'])
    predict_lin = lin_model.predict(newdata[['x1']])[0]

    quad_model = model.fit(df[['x1','x2']],df['y'])
    predict_quad = quad_model.predict(newdata[['x1','x2']])[0]

    cub_model = model.fit(df[['x1','x3']],df['y'])
    predict_cub = cub_model.predict(newdata[['x1','x3']])[0]

    cub2_model = model.fit(df[['x2','x3']],df['y'])
    predict_cub2 = cub2_model.predict(newdata[['x2','x3']])[0]

    log_x_model = model.fit(df[['x1','xlog']], df['y'])
    predict_log_x = log_x_model.predict(newdata[['x1','xlog']])[0]

    log_model = model.fit(df[['xlog']],df['y'])
    predict_log = log_model.predict(newdata[['xlog']])[0]

    y = df['y']
    x_lin = df['x1']
    x_lin = sm.add_constant(x_lin)
    p_lin = pd.read_html(sm.OLS(y,x_lin).fit().summary2().as_html())[0]
    pvalue_lin = p_lin.loc[5,3]

    x_quad = df[['x1','x2']]
    x_quad = sm.add_constant(x_quad)
    p_quad = pd.read_html(sm.OLS(y, x_quad).fit().summary2().as_html())[0]
    pvalue_quad = p_quad.loc[5,3]

    x_cub = df[['x1','x3']]
    x_cub = sm.add_constant(x_cub)
    p_cub = pd.read_html(sm.OLS(y, x_cub).fit().summary2().as_html())[0]
    pvalue_cub = p_cub.loc[5, 3]

    x_cub2 = df[['x2','x3']]
    x_cub2 = sm.add_constant(x_cub2)
    p_cub2 = pd.read_html(sm.OLS(y, x_cub2).fit().summary2().as_html())[0]
    pvalue_cub2 = p_cub2.loc[5, 3]

    x_log_x = df[['x1','xlog']]
    x_log_x = sm.add_constant(x_log_x)
    p_log_x = pd.read_html(sm.OLS(y, x_log_x).fit().summary2().as_html())[0]
    pvalue_log_x = p_log_x.loc[5, 3]

    x_log = df['xlog']
    x_log = sm.add_constant(x_log)
    p_log = pd.read_html(sm.OLS(y, x_log).fit().summary2().as_html())[0]
    pvalue_log = p_log.loc[5, 3]

    d = {predict_log:pvalue_log, predict_lin:pvalue_lin, predict_log_x:pvalue_log_x, predict_cub:pvalue_cub, predict_cub2:pvalue_cub2, predict_quad:pvalue_quad}
    if any(v <= p_value for v in iter(d.values())) == True:
        return np.round(min(d, key=d.get),2)
    else:
        return sum(input[-4:])/len(input[-4:])