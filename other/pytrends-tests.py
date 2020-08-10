from pytrends.request import TrendReq

pytrend = TrendReq()

kw_list = ["Crusader invasions of Egypt", "+ ed sherean album"]
pytrend.build_payload(kw_list, cat=0, timeframe='today 1-m', geo='', gprop='')
vv = pytrend.interest_over_time().cumsum()
print(vv)
    