from flask import Flask
from flask_cors import CORS
from flask_restful import Resource, Api
import json
import pandas as pd
import sqlite3
from uuid import uuid4

app = Flask(__name__)
app.secret_key = str(uuid4())
CORS(app)
api = Api(app)


class Home(Resource):
    def get(self):
        db = sqlite3.connect('travels.db')
        df = pd.read_sql('select * from routes order by search_date desc limit 50', db)
        return json.loads(df.to_json(orient='records')), 200


api.add_resource(Home, '/')

if __name__ == '__main__':
    app.run(debug=True)