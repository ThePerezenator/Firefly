from flask import Flask, flash, redirect, url_for, render_template, request, session, send_from_directory, abort, current_app as app
import sqlite
from urllib.parse import urlparse
from werkzeug.utils import secure_filename
import requests
import os
import itertools

UPLOAD_FOLDER = r'C:\Users\Perez\Desktop\Firefly\static\uploads'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'mp4'])

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

app = Flask(__name__, static_folder='static')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.secret_key = "perezenator"

standard_headings = ("Song", "Controls", "Status", "Tags")
requests_headings = ("Song", "Controls", "Requester", "Status", "Unix")

setlist_headings = ("Song", "")
nav_headings = ("Setlist", "")

bannedip = []
@app.before_request
def block_method():
    ip = request.environ.get('REMOTE_ADDR')
#    if ip in bannedip:
#        print(f"BLOCKED: {bannedip}")
#        abort(403)
    if ip != "72.196.113.92":
        print(requests.get(f"https://geolocation-db.com/json/{ip}&position=true").json())
        abort(403)

@app.route("/")
def home():
    return render_template("main.html")

@app.route('/favicon.ico')
def favicon():
    return app.send_static_file('favicon.ico')

@app.route("/main/", methods=["POST", "GET"])
def main():
    if request.method == "POST":
        setlist = request.form["setlist"]
        if setlist:
            sqlite.create_database(setlist)
    if request.args.get('delete') != None:
        setlist = request.args.get('delete')
        try:
            os.remove(f"/home/perez/Desktop/Python Projects/Firefly/Setlists/{setlist}")
            print(f"DELETED {setlist}")
        except:
            print(f"ERROR DELETING {setlist}")

    nav_data = zip(os.listdir("/home/perez/Desktop/Python Projects/Firefly/Setlists"), )
    return render_template("main.html", nav_data=nav_data, nav_headings=nav_headings)

@app.route("/open/", methods=["POST", "GET"])
def open():
    if request.args.get('setlist') != None:
        setlist = request.args.get('setlist')
        setlist_data = sqlite.open({setlist})
    if request.args.get('remove') != None:
        remove_song = request.args.get('remove')
        print(remove_song)
        sqlite.remove_song(setlist, remove_song)
        return redirect(f"http://noahsnotes.ddns.net:5000/open/?setlist={setlist}")
    if request.method == "POST":
        try:
            add_song = request.form["add_song"]
            sqlite.add_song(setlist, add_song)
            return redirect(f"http://noahsnotes.ddns.net:5000/open/?setlist={setlist}")
        except:
            pass
            
    return render_template("open.html", setlist=setlist, setlist_data=setlist_data, setlist_headings=setlist_headings)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=False)