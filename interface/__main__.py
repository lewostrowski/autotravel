from flask import Flask, sessions, render_template
from flask_cors import CORS
import json
import pandas as pd
import sqlite3
from uuid import uuid4

app = Flask(__name__)
app.secret_key = str(uuid4())
CORS(app)


@app.route("/")
def home():
    db = sqlite3.connect('travels.db')
    df = pd.DataFrame()
    try:
        # select route, search_date, to_departure, to_arrival, to_direct, price, to_carrier
        query = """
        select *
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
            return render_template('index.html', df=df)
        else:
            place_holder = {'route': ['empty']}
            df = json.loads(pd.DataFrame(place_holder).to_json(orient='records'))
            return render_template('index.html', df=df)


if __name__ == '__main__':
    app.run(debug=True)
