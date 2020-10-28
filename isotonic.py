import pandas as pd
import numpy as np
from sklearn.isotonic import IsotonicRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score
import matplotlib.pyplot as plt
%matplotlib inline

prop = 0.7

data = pd.read_csv('s3://sagemakerbmeironia/sagemaker_input_data/data.csv', sep=';')
data.set_index('date_ws', inplace=True)

check_equal_df = False
while not check_equal_df:
    data_pre = data.copy()
    data.fillna(method='ffill', inplace=True)
    check_equal_df = data.equals(data_pre)

check_equal_df = False
while not check_equal_df:
    data_pre = data.copy()
    data.fillna(method='bfill', inplace=True)
    check_equal_df = data.equals(data_pre)
    
returns = np.log(data).diff()

market = returns.mean(axis=1)
market.iloc[0] = 1
market_cum = market.cumsum()
X = market_cum[:-1]
y = market_cum[1:]
index = int(prop*len(y))
X_train, X_test, y_train, y_test = X.iloc[:index],  X.iloc[index:],  y.iloc[:index],  y.iloc[index:]

reg = IsotonicRegression(increasing='auto', out_of_bounds='clip')
reg.fit(X_train, y_train)
prediction = reg.predict(X_test)
r2_score(y_test, prediction)

fig, ax1 = plt.subplots()
ax1.plot(y_test, color='tab:green')
ax1.plot(prediction, color='tab:blue')
ax2 = ax1.twinx()
ax2.plot(y_test-prediction, color='tab:red')
fig.tight_layout()
fig.set_size_inches(18.5, 10.5, forward=True)
plt.show()