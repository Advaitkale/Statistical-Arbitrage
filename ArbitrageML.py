import pandas as pd
import numpy as np
import sys
sys.__stdout__=sys.stdout
from datetime import datetime
#to plot within notebook
import matplotlib.pyplot as plt
from matplotlib import style
style.use('ggplot')
##%matplotlib inline

#setting figure size
from matplotlib.pylab import rcParams
rcParams['figure.figsize'] = 20,10

#for normalizing data
from sklearn.preprocessing import MinMaxScaler
scaler = MinMaxScaler(feature_range=(0, 1))
from sklearn.feature_extraction import DictVectorizer
from sklearn.model_selection import train_test_split

from sklearn.linear_model import TheilSenRegressor, RANSACRegressor
from sklearn.tree import DecisionTreeRegressor


from sklearn.metrics import r2_score
#from mlxtend.plotting import plot_decision_regions

#Reading Data
paint = pd.read_csv('AsianPaint.csv')
print(paint.head())

#Time Series Analysis
start16 = datetime(2016, 1, 1)
end16 = datetime(2016, 12, 31)
stamp16 = pd.date_range(start16, end16)

start17 = datetime(2017, 1, 1)
end17 = datetime(2017, 12, 31)
stamp17 = pd.date_range(start17, end17)

paint['Date'] = pd.to_datetime(paint.TIMESTAMP,format='%Y-%m-%d')
paint.index = paint['Date']

#New Dataset
paint = paint[['OPEN', 'HIGH', 'LOW', 'CLOSE', 'TOTTRDQTY', 'Date', 'PREVCLOSE', 'TOTTRDVAL', 'TOTALTRADES']]
paint['HL_PCT'] = (paint['HIGH'] - paint['LOW']) / paint['LOW'] * 100.0
paint.index = paint['Date']

#Seperating Train and test data
train = []
test = []
for index, rows in paint.iterrows():
    if index in stamp16:
        train.append(list(rows))
    if index in stamp17:
        test.append(list(rows))

train = pd.DataFrame(train, columns = paint.columns)
test = pd.DataFrame(test, columns = paint.columns)




#Pre-Processing  Train Data 
X_train = train[['HIGH', 'LOW', 'OPEN', 'TOTTRDQTY', 'TOTTRDVAL', 'TOTALTRADES']]
x_train = X_train.to_dict(orient='records')
vec = DictVectorizer()
X = vec.fit_transform(x_train).toarray()
Y = np.asarray(train.CLOSE)
Y = Y.astype('int')

#Pre-Processing Test data
X_test = test[['HIGH', 'LOW', 'OPEN', 'TOTTRDQTY', 'TOTTRDVAL', 'TOTALTRADES']]
x_test = X_test.to_dict(orient='records')
vec = DictVectorizer()
x = vec.fit_transform(x_test).toarray()
y = np.asarray(test.CLOSE)
y = y.astype('int')



#Classifier
clf = TheilSenRegressor()
clf.fit(X, Y) 

predict = clf.predict(x)
print("Accuracy of this Statistical Arbitrage model is: ",r2_score(predict,y))
test['predict'] = predict



#Ploting 
train.index = train.Date
test.index = test.Date
train['CLOSE'].plot()
test['CLOSE'].plot()
test['predict'].plot()
plt.legend(loc='best')
plt.xlabel('Date')
plt.ylabel('Price')
plt.show()
