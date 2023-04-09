import requests


img_fpath = "static/keyboard.jpg"


url = 'http://127.0.0.1:8100/'
data = {'message': img_fpath}
response = requests.post(url, json=data)
