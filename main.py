from flask import Flask, request, jsonify
import requests


app = Flask(__name__)


@app.route('/')
def welcome():
    return "please add to the url '/api/hello?visitor_name='username''"


@app.route('/api/hello', methods=['GET'])
def display():
    name = get_user_name()
    ip, city, lat, long = get_user_ip_and_city()
    whether = get_wheather_info(lat, long)
    return jsonify({"client_ip": ip, "location": city, "greeting": f"Hello, {name}! the temperature is {whether} degrees Celcius in {city}"})


def get_user_name():
    username = request.args.get('visitor_name', 'Guest')
    return username


def get_user_ip_and_city():
    url = "http://ip-api.com/json/"
    try:
        responds = requests.get(url)
        data = responds.json()
        ip = data["query"]
        city = data["city"]
        lat = data["lat"]
        long = data["lon"]
        return ip, city, lat, long
    except requests.exceptions.RequestException as e:
        print(f"error making API request : {e}")
        return None
    except ValueError as e:
        print(f"Error parsing JSON responds:{e}")
        return None


def get_wheather_info(lat, long):
    api_key = "7300c952042796002a259cc256140402"
    url = f"https://api.openweathermap.org/data/2.5/weather?lat={
        lat}&lon={long}&appid={api_key}&units=metric"
    try:
        responds = requests.get(url)
        responds.raise_for_status()
        data = responds.json()
        temp = data["main"]["temp"]
        return temp
    except requests.exceptions.RequestException as e:
        print(f"error making API request : {e}")
        return None
    except ValueError as e:
        print(f"Error parsing JSON responds:{e}")
        return None


if __name__ == '__main__':
    app.run(debug=True)
