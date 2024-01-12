from flask import Flask
import codecs
from flask_cors import CORS


app=Flask(__name__)
CORS(app)
file = codecs.open("D:/FlaskProject-1/template/Reset_password_HTML.html", "r", "utf-8")
html_file=file.read()

@app.route('/page')
def page():
    return html_file +'''<a href="https://photos.app.goo.gl/cN56K4Tc22Bzx2GE8">Legend</a>'''
app.run()