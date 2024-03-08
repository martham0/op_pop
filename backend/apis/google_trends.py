from pytrends.request import TrendReq 

GET_METHOD='get'
# pytrend = TrendReq(retries=3)


headers = {
    'authority': 'trends.google.com',
    'accept': 'application/json, text/plain, */*',
    'accept-language': 'en-US,en;q=0.8',
    # 'cookie': 'S=billing-ui-v3=5Uelr7uAwtIjtbragoFXbbCxb0YGxBOn:billing-ui-v3-efe=5Uelr7uAwtIjtbragoFXbbCxb0YGxBOn; SID=g.a000gghLUJlhTzMhI7Tzb4ohWcctzVyaxnC4yB3Y0XcWUP5nX4s_m8mKbmqoy5yifDMwph2vaQACgYKARgSAQASFQHGX2MidjhI9EeQu6ktwSzUGtW5xhoVAUF8yKp1TtnwtoQj16VHXWeUBUEm0076; __Secure-1PSID=g.a000gghLUJlhTzMhI7Tzb4ohWcctzVyaxnC4yB3Y0XcWUP5nX4s_ovdyA8ju_MRA_yioVV0DHQACgYKAdQSAQASFQHGX2Mio_bFFLB40KM2bilVUXxGMhoVAUF8yKpkbEZPmGb2QYsePOxT1-eH0076; __Secure-3PSID=g.a000gghLUJlhTzMhI7Tzb4ohWcctzVyaxnC4yB3Y0XcWUP5nX4s_sdvNz1NWlwVVBeSoXz9uhwACgYKAckSAQASFQHGX2MiC1Cq9H3bCBnukwHx95OsVxoVAUF8yKpQumA1ox-sWB3xtLPaiP8q0076; HSID=Ahw1Eava85jSGTymk; SSID=A5fbg26yOnDylVZw6; APISID=3KQ7gDjWPepJQcvq/A_tRm6Pu-Lhht2nAD; SAPISID=kBlFdR8WSoKWie_h/AZ3BAH4C3DXtnBLiD; __Secure-1PAPISID=kBlFdR8WSoKWie_h/AZ3BAH4C3DXtnBLiD; __Secure-3PAPISID=kBlFdR8WSoKWie_h/AZ3BAH4C3DXtnBLiD; SEARCH_SAMESITE=CgQIypoB; NID=512=kxvlHwmPHT1Kdxu-AJr3UMccGLyfc8m_q33rYEXiU8Q6Lws644HuKh-J3upFVEE0riH8rwDssSwfiRZK5JMzDHqEo69Ivgv9j0_79UeNtnrv1S7sRGk5VxYy5Bjog8WfS81N_K5QLgFZACUEkxjRHpYWlp-XgcDrtieWDwNYNu7TLqcGTgG9NkjrKKNgRnaAupOcOJxwsBSXZXWayEbeKs-Q-A4rrm6UZEcn_r6PFYMX4AlGGa2pIbGPN7hEtmYdBWHqLLKn3p7s8VqTN3wvOEIidpyDxbpRJ-WIgLSKjUUgS3q8AehQmjSCnbwLo9Rx2fG9LnVqpeK1pagcgKufTpI2fUNvwAu98pARZrFpQbaKmLUV02mUQwxBImmWOPS5ntsNuXVAxOi_GfVlH_WWKY6CB5mxu9SA1W1HzpYW3lwbBtU3uP5v-UYBnLgzUZZZhlGWtvCqbj7PcItKKrBZC3GXA4cG6iOC_jqx8MvBu7LQ2D0PFRDat6GEBmjOJG2YNk-lOMRjxm16PgP8Va7q6VyN3ghhIVXcR9__XX0F1D6_ZNxW7Yo_MAJgsBbu_AahgWirjNGYi9zJljDqcmH5ODZtVnqjyI0jxmUzG_1yM-M5yGJLFUwUp58aPTpCmj9nlL74tF7BEjM5gXMA-TF3HzPH9wgzciH_4n05X3rYV7QSnZ83edLvpA; OTZ=7456219_88_88_104280_84_446940; AEC=Ae3NU9P-ylkBIuL5yF0Uy1EL-0bltTKjoPdQo_y16nAkKaOzudS1X2VRQg; __Secure-ENID=18.SE=LDP0nV8Zba9WgLYvNbrer153s8IH57axZrqX5_Dc26lGkVsiSHGdrtqCdO-sY0RSSbQq4PWJJ3uCFsyWo3JzyB3WhH-Fpy04h6hVjFofBxsUn47IfS-6dFgjnXQC53IgLcwj8svTejQbOqcowLsKZVjDJ2j3yAkm0hPFM90PJ41kZYJ4Dg9h-8u-aMa0a48GDtBLPqCZjsDpsTaKcerD4qphW4uecFfImtcjD3vjgFOpkO_Yyev0hS59wtDcFQZF3FhLn2LjNB8PQ27ICr35gqtmYzrTh1ZBqF5s_Yy3EO4zcE8ZyvSYTVaVCPU; 1P_JAR=2024-03-07-05; __Secure-1PSIDTS=sidts-CjIBYfD7Z1Xe7oIzEPdYPMwM6_HsH1dLULcihnSies3rUK9kx0kF4XfUd9NYQp-ODPDYIhAA; __Secure-3PSIDTS=sidts-CjIBYfD7Z1Xe7oIzEPdYPMwM6_HsH1dLULcihnSies3rUK9kx0kF4XfUd9NYQp-ODPDYIhAA; SIDCC=AKEyXzWa5q9VY5hCS7VnYqXPA07aSregubUfJqsgL7nvWcqeyiJoOADUS-rUHnPZ0S5zy63HaWA; __Secure-1PSIDCC=AKEyXzWp08ft4kuVwY6wveQj4EhCkyQurMTyKnMUDSh-C74XaD-p29BTsAylP4Q0WA8_MRqqyOz3; __Secure-3PSIDCC=AKEyXzVjBnWSYgY2T6ormRgN0N5kV2vNcsS50QiMwZP6glCEOMum-dsNKscvjH5S-om4x7fzUQnU',
    'referer': 'https://trends.google.com/trends/explore?cat=3&date=2004-02-07%202024-03-07&geo=US&q=%2Fm%2F01_f41&hl=en',
    'sec-ch-ua': '"Not A(Brand";v="99", "Brave";v="121", "Chromium";v="121"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-model': '""',
    'sec-ch-ua-platform': '"macOS"',
    'sec-ch-ua-platform-version': '"14.1.1"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'sec-gpc': '1',
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36',
}



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