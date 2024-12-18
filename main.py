import os

from flask import Flask, send_file, render_template, request
import xml.etree.ElementTree as ET

app = Flask(__name__)

@app.route("/")
def index():
    return send_file('src/index.html')

@app.route("/arama")
def arama():
    anahtarKelime = request.args.get('anahtarKelime','')
    return render_template('arama.html', data=anahtarKelime)

@app.route("/katalog")
def katalog():
    keyword = request.args.get('anahtarKelime', '').lower()
    results, soru = arama_fonksiyonu(keyword) 
    return render_template("katalog.html", data=results, soru=soru)

def arama_fonksiyonu(keyword):
    try:
        tree = ET.parse('katalog.xml')
        root = tree.getroot()
    except FileNotFoundError:
        return "Katalog dosyası bulunamadı."
    except ET.ParseError:
        return "Katalog dosyasında bir hata var."

    soru = "Hangi türde müzik dinlemek istersiniz?"
    catalog = []
    for cd in root.findall('CD'):
        cd_dict = {}
        for child in cd:
            cd_dict[child.tag] = child.text
        catalog.append(cd_dict)

    if request.method == "GET":
        words = keyword.split()
        filtered_catalog = [cd for cd in catalog if all(word.lower() in (v or "").lower() for word in words for v in cd.values())]
        # Sonuçların olup olmadığını kontrol edelim
        if filtered_catalog:
            return filtered_catalog, soru
        else:
            return "Aradığınız kelimeye ait sonuç bulunamadı.", None
    else:
        return catalog, soru

if __name__ == "__main__":
    app.run(port=int(os.environ.get('PORT', 80)))
