import os
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

@app.route("/")
def home():
  try:
    data = db.get_all_inputs()
  except Exception as e:
    print(e)
    data = None
  return render_template("home.html", data=data)

@app.route('/favicon.ico')
def favicon():
  print(app.root_path)
  return send_from_directory(os.path.join(app.root_path, 'static'), 'favicon.ico', mimetype='image/vnd.microsoft.icon')

@app.route("/add", methods=["POST"])
def add():
  try:
    data = request.form.get("userinput")
    db.add_input(data)
  except Exception as e:
    print(e)
  return home()
  
@app.route("/clear")
def clear():
  try:
    db.clear_all()
  except Exception as e:
    print(e)
  return home()
if __name__ == "__main__":
  app.run(host="0.0.0.0", port=app_env.port, debug=False)
