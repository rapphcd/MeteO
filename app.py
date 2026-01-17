from flask import Flask, render_template, request, redirect, url_for
import requests

appid = "" #votre app id openweathermap
ip = "" #votre ip

app = Flask(__name__)


def recup_data(ville):
    url = f"https://api.openweathermap.org/data/2.5/weather?q={ville}&units=metric&appid={appid}"
    response = requests.get(url)
    dico = response.json()
    if dico["cod"] != '404':
        dc = {"cod": dico["cod"], "ville": dico["name"], "temp": dico["main"]["temp"],
              "humidity": dico["main"]["humidity"], "description": dico["weather"][0]["description"],
              "icon": dico["weather"][0]["icon"]}
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
        v = dat["ville"]
        t = dat["temp"]
        h = dat["humidity"]
        d = dat["description"].capitalize()
        i = dat["icon"]

        if t >= 25:
            c = "red;"
        elif t >= 20:
            c = "orange;"
        elif t <= 10:
            c = "aqua;"
        else:
            c = "white;"
        return render_template('meteo.html', ville=v, temp=t, humidity=h, description=d, icon=i, color=c)
    return redirect(url_for('index'))


@app.route('/meteo/<ville>')
def meteoville(ville):
    if not ville:
        return redirect(url_for('index'))
    dat = recup_data(ville)
    if dat["cod"] == '404':
        return redirect(url_for('index'))
    v = dat["ville"]
    t = dat["temp"]
    h = dat["humidity"]
    d = dat["description"].capitalize()
    i = dat["icon"]

    if t >= 25:
        c = "red;"
    elif t >= 20:
        c = "orange;"
    elif t <= 10:
        c = "aqua;"
    else:
        c = "white;"
    return render_template('meteo.html', ville=v, temp=t, humidity=h, description=d, icon=i, color=c)


if __name__ == '__main__':
    app.run(debug=True, host=ip)