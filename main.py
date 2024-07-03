from flask import Flask, request, jsonify
import requests


app = Flask(__name__)


@app.route('/')
def welcome():
    return "please add to the url '/api/hello?visitor_name='username''"


@app.route('/api/hello', methods=['GET'])
def display():
    city = "abuja"
    name = get_user_name()
    ip = get_user_ip()
    whether = get_wheather_info(city)
    return jsonify({"client_ip": ip,
                    "location": city,
                    "greeting": f"Hello, {name}! the temperature is {whether} degrees Celcius in {city}"})


def get_user_name():
    username = request.args.get('visitor_name', 'Guest')
    return username


def get_user_ip():
    ip = request.remote_addr
    return ip


def get_wheather_info(city):
    api_key = "7300c952042796002a259cc256140402"
    url = f"https://api.openweathermap.org/data/2.5/weather?q={
        city}&appid={api_key}&units=metric"
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
