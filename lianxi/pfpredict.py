import pandas as pd
import numpy as np
from scipy import stats
import matplotlib.pyplot as plt
import statsmodels.api as sm
from statsmodels.graphics.api import qqplot


#读取数据，进行处理
dta = [10930,10318,10595,10972,7706,6756,9092,10551,9722,10913,11151,8186,6422,6337,11649,11652,10310,12043,7937,6476,9662,9570,9981,9331,9449,6773,6304,9355, 10477,10148,10395,11261,8713,7299,10424,10795,11069,11602,11427,9095,7707,10767,12136,12812,12006,12528,10329,7818,11719,11683,12603,11495,13670,11337,10232, 13261,13230,15535,16837,19598,14823,11622,19391,18177,19994,14723,15694,13248, 9543,12872,13101,15053,12619,13749,10228,9725,14729,12518,14564,15085,14722, 11999,9390,13481,14795,15845,15271,14686,11054,10395]
dta = np.array(dta,dtype=np.float)
dta = pd.Series(dta)

#对数据进行绘图，观测是否是平稳时间序列
dta.index = pd.Index(sm.tsa.datetools.dates_from_range('1927','2016'))
# dta.plot(figsize=(12,8))
# plt.show()

# fig = plt.figure(figsize=(12,8))
# ax1 = fig.add_subplot(111)
# diff1 = dta.diff(1)
# diff1.plot(ax=ax1)
# plt.show()

#选择合适的p,q
diff1 = dta.diff(1)
fig = plt.figure(figsize=(12,8))
ax1 = fig.add_subplot(211)
fig = sm.graphics.tsa.plot_acf(dta,lags=40,ax=ax1)
ax2 = fig.add_subplot(212)
fig = sm.graphics.tsa.plot_acf(dta,lags=40,ax=ax2)
# plt.show()

#获取最佳模型
arma_mod70 = sm.tsa.ARMA(dta,(7,0)).fit()
print(arma_mod70.aic,arma_mod70.bic,arma_mod70.hqic)
arma_mod30 = sm.tsa.ARMA(dta,(0,1)).fit()
print(arma_mod30.aic,arma_mod30.bic,arma_mod30.hqic)
arma_mod71 = sm.tsa.ARMA(dta,(7,1)).fit()
print(arma_mod71.aic,arma_mod71.bic,arma_mod71.hqic)
arma_mod80 = sm.tsa.ARMA(dta,(8,0)).fit()
print(arma_mod80.aic,arma_mod80.bic,arma_mod80.hqic)

#模型检验
resid = arma_mod80.resid
fig = plt.figure(figsize=(12,8))
ax1 = fig.add_subplot(211)
fig = sm.graphics.tsa.plot_acf(dta,lags=40,ax=ax1)
ax2 = fig.add_subplot(212)
fig = sm.graphics.tsa.plot_acf(dta,lags=40,ax=ax2)
plt.show()


print(sm.stats.durbin_watson(arma_mod80.resid.values))

fig = plt.figure(figsize=(12,8))
ax = fig.add_subplot(111)
fig = qqplot(resid,line='q',ax=ax,fit=True)
plt.show()

r,q,p = sm.tsa.acf(resid.values.squeeze(),qstat=True)
data = np.c_[range(1,41),r[1:],q,p]
table = pd.DataFrame(data,columns=['lag','AC','Q','Prob(>Q)'])
print(table.set_index('lag'))

#模型预测
predict_sunspots = arma_mod80.predict('2016','2026',dynamic=True)
print(predict_sunspots)
fig,ax = plt.subplots(figsize=(12,8))
ax = dta.ix['1927':].plot(ax=ax)
fig = arma_mod80.plot_predict('2016','2026',dynamic=True,ax=ax,plot_insample=False)
plt.show()

