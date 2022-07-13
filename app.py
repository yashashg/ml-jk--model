from flask import Flask
from flask_restful import Resource, Api, reqparse
import pickle
import pandas as pd
from sklearn.preprocessing import LabelEncoder

app = Flask(__name__)
api = Api(app)

class Users(Resource):
    # methods go here
    
    def post(self):
        
        parser = reqparse.RequestParser()  # initialize
        parser.add_argument('userId', required=True)  # add args
        args = parser.parse_args()  # parse arguments to dictionary
        # text = p.convert(args['userId'])
        print (args['userId'])
        userId=[args['userId']]
        df = pd.read_csv(r"incident.csv", encoding="utf8")
        y = df['Category']
        encoder = LabelEncoder()
        y = encoder.fit_transform(y)

        v = dict(zip(list(y), df['Category'].to_list()))
        loaded_model = pickle.load(open(r"itsmmodel.pkl", 'rb'))
        result = loaded_model.predict(userId)
        return {'userId':v[result[0]] }, 200  # return data with 200 OK
        
        
api.add_resource(Users, '/users')  # '/users' is our entry point
    
if __name__ == '__main__':
    app.run()  # run our Flask app
