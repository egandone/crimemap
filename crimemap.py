import os
import json
from cfenv import AppEnv
from flask import Flask
from flask import send_from_directory
from flask import render_template
from dbhelper import DBHelper
from flask import request

app = Flask(__name__)

app_env = AppEnv()
db = DBHelper(app_env)
db.create_table()

# Google Maps API Key = "AIzaSyBXYBYNCCPGeRUQU2EmCdCy1PvT8WmO8ck"
@app.route("/")
def home():
  try:
    crimes = db.get_all_crimes()
    crimes = json.dumps(crimes)
  except Exception as e:
    print(e)
    crimes = None
  return render_template("home.html", crimes=crimes)

@app.route("/submitcrime", methods=["POST"])
def submitcrime():
  category = request.form.get("category")
  date = request.form.get("date")
  latitude = float(request.form.get("latitude"))
  longitude = float(request.form.get("longitude"))
  description = request.form.get("description")
  db.add_crime(category, date, latitude, longitude, description)
  return home()

@app.route('/favicon.ico')
def favicon():
  print(app.root_path)
  return send_from_directory(os.path.join(app.root_path, 'static'), 'favicon.ico', mimetype='image/vnd.microsoft.icon')

@app.route("/clear")
def clear():
  try:
    db.clear_all()
  except Exception as e:
    print(e)
  return home()

if __name__ == "__main__":
  app.run(host="0.0.0.0", port=app_env.port, debug=False)
