from flask import Flask, render_template, request, redirect, url_for
import requests

appid = ""  # votre app id openweathermap
ip = ""  # votre ip

app = Flask(__name__)


def getTempColor(temp):
    if temp >= 25:
        c = "red"
    elif temp >= 20:
        c = "orange"
    elif temp <= 10:
        c = "aqua"
    else:
        c = "white"
    return c

def recup_data(ville):
    url = f"https://api.openweathermap.org/data/2.5/weather?q={ville}&units=metric&appid={appid}"
    response = requests.get(url)
    dico = response.json()
    if dico["cod"] == 200:

        dc = {"cod": dico["cod"], "ville": dico["name"], "temp": dico["main"]["temp"],
              "humidity": dico["main"]["humidity"], "description": dico["weather"][0]["description"],
              "icon": dico["weather"][0]["icon"], "country": dico["sys"]["country"], "color": getTempColor(dico["main"]["temp"])}

        lon = dico['coord']['lon']
        lat = dico['coord']['lat']

        forecast_url = f'https://api.openweathermap.org/data/2.5/forecast?lat={lat}&lon={lon}&appid={appid}'

        forecast_response = requests.get(forecast_url)
        forecasts = forecast_response.json()

        if forecasts["cod"] == "200":
            forecast = forecasts['list'][-1]
            final_forecast = {'temp': {'min': forecast["main"]['temp_min'], 'max': forecast["main"]['temp_max'],
                                       'predicted': forecast["main"]['temp']}, "humidity": forecast["main"]['humidity'],
                              "description": forecast["weather"][0]["description"], "icon": forecast["weather"][0]["icon"], "color": getTempColor(forecast["main"]['temp'])}
            dc["forecast"] = final_forecast
    else:
        dc = {"cod": dico["cod"]}
    return dc


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/meteo', methods=['GET', 'POST'])
def meteo():
    if request.method == 'POST' or request.method == 'GET':
        ville = request.form.get('ville', '').strip()
        if not ville:
            return redirect(url_for('index'))
        dat = recup_data(ville)
        if dat["cod"] == '404':
            return redirect(url_for('index'))
        return render_template(
            'meteo.html',data=dat)
    return redirect(url_for('index'))

@app.route('/meteo/<ville>')
def meteoville(ville):
    if not ville:
        return redirect(url_for('index'))
    dat = recup_data(ville)
    if dat["cod"] == '404':
        return redirect(url_for('index'))

    return render_template(
        'meteo.html',data=dat )


if __name__ == '__main__':
    app.run(debug=True, host=ip)
