import openaq
api = openaq.OpenAQ()
status, body = api.cities()
