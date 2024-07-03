from flask import Flask, request, jsonify
import requests
import socket


app = Flask(__name__)


@app.route('/')
def welcome():
    return "please add to the url '/api/hello?visitor_name='username''"


@app.route('/api/hello', methods=['GET'])
def display():
    name = get_user_name()
    ip = get_user_ip()
    whether, city = get_wheather_info(get_public_ip())
    return jsonify({"client_ip": ip,
                    "location": city,
                    "greeting": f"Hello, {name}! the temperature is {whether} degrees Celcius in {city}"})


def get_user_name():
    username = request.args.get('visitor_name', 'Guest')
    return username


def get_user_ip():
    ip = request.remote_addr
    return ip


def get_public_ip():
    response = requests.get('https://api64.ipify.org')
    ip_data = response.json()
    public_ip = ip_data['origin']
    return public_ip


def get_wheather_info(ip):
    api_key = "46accdfb7cf34ac8b0493214240307"
    url = f"http://api.weatherapi.com/v1/current.json?key={
        api_key}&q={str(ip)}&aqi=no"
    try:
        responds = requests.get(url)
        responds.raise_for_status()
        data = responds.json()
        temp_c = data["current"]["temp_c"]
        location = data["location"]["region"]
        return temp_c, location
    except requests.exceptions.RequestException as e:
        print(f"error making API request : {e}")
        return None
    except ValueError as e:
        print(f"Error parsing JSON responds:{e}")
        return None


if __name__ == '__main__':
    app.run(debug=True)
