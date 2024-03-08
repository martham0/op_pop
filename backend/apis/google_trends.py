from pytrends.request import TrendReq 

GET_METHOD='get'
# pytrend = TrendReq(retries=3)




# class TrendReq(UTrendReq):
#     def _get_data(self, url, method=GET_METHOD, trim_chars=0, **kwargs):
#         return super()._get_data(url, method=GET_METHOD, trim_chars=trim_chars, headers=headers, **kwargs)

# connect to google
# pytrends = TrendReq(hl='en-US', tz=360, retries=3)
pytrends = TrendReq(hl='en-US', tz=360, timeout=(10,25), proxies=['https://34.203.233.13:80',], retries=3, backoff_factor=0.1, requests_args={'verify':False})

# build payload
kw_list = ["Blockchain"]
pytrends.build_payload(kw_list, cat=0, timeframe='today 5-y', geo='', gprop='')
print(pytrends.related_topics())