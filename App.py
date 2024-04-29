from flask import Flask, render_template, request
import requests
from datetime import datetime, date

app = Flask(__name__)

WEATHER_API_ENDPOINT = "http://api.openweathermap.org/data/2.5/weather"
WEATHER_API_KEY = "b60b359d0af5113fbaba3553d2643305"

NEWS_API_ENDPOINT = 'https://newsapi.org/v2/top-headlines'
NEWS_API_KEY = '87fe557b1c82431cb84bab233c6b2258'

def get_weather(city):
    params = {
        'q':city,
        'appid':WEATHER_API_KEY,
        'units':'metric'
    }
    response = requests.get(WEATHER_API_ENDPOINT,params=params)
    data = response.json()

    if data.get('cod') == 200:
        weather = {
            'city': data['name'],
            'temperature': data['main']['temp'],
            'humidity':data['main']['humidity'],
            'wind_speed':data['wind']['speed'],
            'description':data['weather'][0]['description'],
            'icon':data['weather'][0]['icon'],
            'date_time':datetime.now().strftime('%H:%M:%S'),
            'today_date':date.today()
        }
        return weather
    else:
        return None
    
def get_news(query):
    url = f'https://newsapi.org/v2/everything?q={query}&apiKey={NEWS_API_KEY}'
    response = requests.get(url)
    data = response.json()

    if response.status_code == 200:
        articles = data.get('articles', [])
        news_data = []
        for article in articles:
            title = article.get('title','No Title')
            title_url = article.get('url', 'No URL')
            image_url = article.get('urlToImage', 'https://via.placeholder.com/150')
            news_data.append({'title':title, 'image_url':image_url, 'title_url':title_url})
        # print('*'*30)
        # print(news_data)
        return news_data

@app.route('/', methods=['GET','POST'])
def home():
    default_city = "Bangalore"
    default = 'None'
    if request.method == 'POST':
        city = request.form.get('city',default_city)
        query = request.form.get('query','')
    else:
        city = request.args.get('city',default_city)
        query = request.args.get('query',default)

    weather = get_weather(city)
    news = get_news(query)



    return render_template('layout.html', weather=weather, news=news)

if __name__ == "__main__":
    app.run(debug=True)