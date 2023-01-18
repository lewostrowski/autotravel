from flask import Flask, render_template
from flask_cors import CORS
import json
import pandas as pd
import sqlite3
from uuid import uuid4

from common import notify

app = Flask(__name__)
app.secret_key = str(uuid4())
CORS(app)


@app.route("/")
def home():
    db_name = 'travels.db'
    db = sqlite3.connect(db_name)
    df = pd.DataFrame()
    try:
        # type, departure_date do query
        query = """
        select route, search_date, to_departure, to_direct, price, to_carrier
        from routes 
        order by search_date desc 
        limit 100
        """
        df = pd.read_sql(query, db)
    except pd.errors.DatabaseError as er:
        print(er)
    finally:
        if not df.empty:
            df = json.loads(df.to_json(orient='records'))
            bargain = notify.check_bargain(db_name, False)
            return render_template('index.html', df=df, bargain=bargain)
        else:
            place_holder = {'route': ['empty']}
            df = json.loads(pd.DataFrame(place_holder).to_json(orient='records'))
            return render_template('index.html', df=df)


if __name__ == '__main__':
    app.run(debug=True)
