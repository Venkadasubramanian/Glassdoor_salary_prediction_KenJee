# %%
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv('eda_data.csv')

# %%
# choose relevant columns
df.columns

# %%
# get dummy data
df_model = df[['avg_salary','Rating','Type of ownership','Industry','Sector','Revenue',
            'employer_provided','Location','age','python_yn','SQL_yn','aws_yn',
            'excel_yn','job_simp_col','desc_len','seniority']]

df_dum = pd.get_dummies(df_model)

# %%
# train test split
from sklearn.model_selection import train_test_split
X = df_dum.drop('avg_salary',axis=1)
y= df_dum['avg_salary'].values
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.33,random_state=42)
# %%
# multiple linear regression
import statsmodels.api as sm

X_sm = X = sm.add_constant(X)
model = sm.OLS(y,X_sm)
model.fit().summary()

from sklearn.linear_model import LinearRegression, Lasso
from sklearn.model_selection import cross_val_score

lm = LinearRegression()
lm.fit(X_train,y_train)

np.mean(cross_val_score(lm,X_train, y_train,scoring='neg_mean_absolute_error'))


# %%
# lasso regression
lm_l = Lasso(alpha=0.1)
lm_l.fit(X_train,y_train)
np.mean(cross_val_score(lm_l,X_train, y_train,scoring='neg_mean_absolute_error'))

alpha = []
error = []

for i in range(1,100):
    alpha.append(i/10)
    lml = Lasso(alpha=(i/10))
    error.append(np.mean(cross_val_score(lml,X_train,y_train, scoring = "neg_mean_absolute_error",cv=3)))
plt.plot(alpha,error)

err = tuple(zip(alpha,error))
df_err = pd.DataFrame(err, columns=['alpha','error'])
df_err[df_err.error == max(df_err.error)]
# %%
# Random Forest
from sklearn.ensemble import RandomForestRegressor
rf = RandomForestRegressor()

np.mean(cross_val_score(rf,X_train,y_train,scoring = "neg_mean_absolute_error",cv=3)) 
# %%
# tune models using GridSearchCV
from sklearn.model_selection import GridSearchCV
parameters = {'n_estimators':range(10,300,10),'criterion':('mse','mae'),
              'max_features':('auto','sqrt','log2')}

gs = GridSearchCV(rf,parameters,scoring='neg_mean_absolute_error',cv=3)
gs.fit(X_train,y_train)
gs.best_score_
gs.best_estimator_
# %%
tpred_lm = lm.predict(X_test)
tpred_lm_l = lm_l.predict(X_test)
tpred_rf = gs.best_estimator_.predict(X_test)

# %%
from sklearn.metrics import mean_absolute_error
mean_absolute_error(y_test,tpred_lm)
mean_absolute_error(y_test,tpred_lm_l)
mean_absolute_error(y_test,tpred_rf)

mean_absolute_error(y_test,(tpred_lm+tpred_rf)/2)