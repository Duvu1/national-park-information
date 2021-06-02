import requests
from bs4 import BeautifulSoup
from flask import Flask, render_template, request

db = []
h_db = []
app = Flask("NationalParkInformation")


@app.route("/")
def home():
    if db:
        pass
    else:
        for i in range(1, 30):
            id = str(i).zfill(4)
            urls = f"http://www.knps.or.kr/front/portal/safe/acsCtrDtl.do?menuNo=8000340&rstId={id}"
            result = requests.get(urls)
            soup = BeautifulSoup(result.text, "html.parser")

            info = soup.find("div", {"class": "control_info_viwe"})
            detail = info.find_all("tr")

            name = detail[0].find("td", {"class": ""}).text
            control = detail[0].find("td", {"class": "control_01 last"}).text
            detailed = detail[1].find("td", {"class": ""}).text
            last = detail[1].find("td", {"class": "last"}).text
            paragraph = detail[3].find_all("p")

            print(i, name, "okay")
            ox = [name, control, detailed, last,  paragraph, urls, id]

            db.append(ox)

    if h_db:
        pass
    else:
        h_url = "http://www.jeju.go.kr/hallasan/index.htm"
        h_result = requests.get(h_url)
        h_soup = BeautifulSoup(h_result.text, "html.parser")

        h_info = h_soup.find_all("dl", {"class": "infoList"})

        for i in h_info:
            h_name = i.find("dt").text
            h_control = i.find("dd", {"class": "situation"}).text
            h_detailed = i.find_all("dd", {"class": ""})
            h_link = "http://www.jeju.go.kr" + \
                i.find("a", href=True)["href"]

            h_ox = [h_name, h_control, h_detailed, h_link]
            h_db.append(h_ox)

        print("30 한라산 okay")

    try:
        t_url = "http://www.knps.or.kr/portal/main.do"
        t_result = requests.get(t_url)
        t_soup = BeautifulSoup(t_result.text, "html.parser")
        t_location = t_soup.find("p", {"class": "p_danger"}).text

        return render_template(
            "home.html",
            db=db,
            t_location=t_location
        )

    except:
        return render_template(
            "home.html",
            db=db
        )


@app.route("/<id>")
def detail(id):
    i = int(id.lstrip("0")) - 1
    return render_template(
        "detail.html",
        data=db[i]
    )


@app.route("/hallasan")
def hallasan():
    return render_template(
        "hallasan.html",
        h_db=h_db
    )


app.run(host="0.0.0.0")
