from flask import Flask, request, render_template
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

def check_xss(url):
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        forms = soup.find_all("form")
        for form in forms:
            if "<script>" in str(form):
                return True
    except:
        return False
    return False

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/scan', methods=['POST'])
def scan():
    url = request.form.get('url')
    xss_vuln = check_xss(url)
    return render_template('report.html', xss=xss_vuln)

if __name__ == "__main__":
    app.run(debug=True)
