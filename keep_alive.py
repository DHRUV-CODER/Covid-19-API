from threading import Thread
import requests
import bs4

from flask import Flask, jsonify, render_template,request,redirect,url_for

app = Flask(__name__)


@app.route('/')
def home():
	return render_template("index.html")

@app.route("/sup")
def hi():
    return redirect("/")

@app.route('/country=<string:country>')
def country(country):
    url = f'https://www.worldometers.info/coronavirus/country/{country.replace(" ","-")}'

    result = requests.get(url)

    soup = bs4.BeautifulSoup(result.text,'lxml')
    cases = soup.find_all('div', class_='maincounter-number')
    links = soup.find('div', {'style': 'display:inline'})
    latest_updated = soup.find('div', class_='news_date')
    
    try:
        last_updated = latest_updated.text
    except:
        last_updated = "Not Provided"

    data = []
    for i in cases:
        span = i.find('span')
        data.append(span.string)


    try:
        images = links.find('img')
        flag = f"https://www.worldometers.info/{images.attrs['src']}"
    except:
        flag = "https://static.wixstatic.com/media/2cd43b_af35a03a70e144ddba269287704a6465~mv2.png/v1/fill/w_256,h_256,q_90/2cd43b_af35a03a70e144ddba269287704a6465~mv2.png"
    
    try:
        Covid_Data = {
            'Stats For' : country.capitalize(),
            'case_stats' : {
                'Total_Cases' : data[0],
                'Deaths' : data[1],
                'Recovered' : data[2],
                'last_updates' : last_updated,
            },
            'uri' : {
                'Flag' : flag,
                'Source' : url,
            },
                "Guidelines" : {
                "WHO" : "https://www.who.int/emergencies/diseases/novel-coronavirus-2019",
                "MythBusters" : "https://www.who.int/emergencies/diseases/novel-coronavirus-2019/advice-for-public/myth-busters"
            },
                "Credits & Info" : {
                "Made By" : "Dhruv",
                "Data From" : "https://www.worldometers.info/coronavirus/",
                "Language" : "Flask-Python Using Web-Scraping"           
            }
        }
    except:
        Covid_Data  = {
            "Code" : "404",
            "Message" : "Try Again Invalid Country"
        }
    return jsonify(Covid_Data)

@app.route("/worldwide")
def earth():
    url = "https://www.worldometers.info/coronavirus/"
    result = requests.get(url)
    
    soup = bs4.BeautifulSoup(result.text,'lxml')
    cases = soup.find_all('div', class_='maincounter-number')
    links = soup.find('div', {'style': 'display:inline'})
    latest_updated = soup.find('div', class_='news_date')
    try:
        last_updated = latest_updated.text
    except:
        last_updated = "Not Provided"

    data = []
    for i in cases:
        span = i.find('span')
        data.append(span.string)

    flag = "https://static.wixstatic.com/media/2cd43b_af35a03a70e144ddba269287704a6465~mv2.png/v1/fill/w_256,h_256,q_90/2cd43b_af35a03a70e144ddba269287704a6465~mv2.png"
    
    Covid_Data = {
        'case_stats' : {
            'Total_Cases' : data[0],
            'Deaths' : data[1],
            'Recovered' : data[2],
            'last_updates' : last_updated,
        },
        'uri' : {
            'Flag' : flag,
            'Source' : url,
        },
        "Guidelines" : {
            "WHO" : "https://www.who.int/emergencies/diseases/novel-coronavirus-2019",
            "MythBusters" : "https://www.who.int/emergencies/diseases/novel-coronavirus-2019/advice-for-public/myth-busters"
        },
        "Credits & Info" : {
            "Made By" : "Dhruv",
            "Data From" : "https://www.worldometers.info/coronavirus/",
            "Language" : "Flask-Python Using Web-Scraping"           
        }
    }

    return jsonify(Covid_Data)    




if __name__ == '__main__':
	app.run(debug=True)

def run():
    app.run(host="0.0.0.0", port=8080)


def keep_alive():
    server = Thread(target=run)
    server.start()