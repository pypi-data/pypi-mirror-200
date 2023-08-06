import pandas as pd
import subprocess as sp
import sys
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime
from pmdarima.arima import auto_arima

sp.call("wget -nc https://covid19.mhlw.go.jp/public/opendata/newly_confirmed_cases_daily.csv", shell = True)

df = pd.read_csv("newly_confirmed_cases_daily.csv")
df = df[['Date', 'ALL']]
df['Date'] = pd.to_datetime(df['Date'])
df = df.set_index('Date')
df = df.iloc[1152:, :]

model = auto_arima(df, start_p=1, start_q=1, max_p=3, max_q=3, seasonal=False, trace=True)
model.fit(df)

pred = model.predict(n_periods=30)

plt.plot(df, label='Result')
plt.plot(pd.date_range(start=df.index[-1], periods=30, freq='D'), pred, label='Prediction')
plt.ylabel('Number of infected [daily]')
plt.xlabel('Date')
plt.grid()
plt.legend()
plt.show()