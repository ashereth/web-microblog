from flask import Flask, render_template, request
import datetime
from pymongo import MongoClient
import os
from dotenv import load_dotenv

load_dotenv()

entries_with_date = []

# make sure to have this function and
#  put everything in it and make sure it returns app at the end
def create_app():
    app = Flask(__name__)
    # set up the client using the connection string for the mongodb database
    client = MongoClient(os.getenv("MONGODB_URI"))
    app.db = client.microblog

    @app.route('/', methods=["GET", 'POST'])
    def home():
        if request.method == "POST":
            # get whatever was entered into content
            entry_content = request.form.get("content")
            #format the date so that it looks better 
            formatted_date = datetime.datetime.today().strftime("%y-%m-%d")
            app.db.entries.insert_one({"content": entry_content, "date": formatted_date})
            global entries_with_date
            entries_with_date = [
                (entry["content"], 
                entry["date"], 
                # make an even better format of the datetime to be displayed on the webpage
                datetime.datetime.strptime(entry["date"], "%y-%m-%d").strftime('%b %d')
                )
                #get all the entries in the database in reverse
                    # order so that most recent entries show first
                for entry in app.db.entries.find({}).sort("_id", -1)
            ]

        return render_template("home.html", entries=entries_with_date)

    return app
