from flask import Flask
from flask_apscheduler import APScheduler
from flask_restful import Api
from flask_cors import CORS

import os
import module.schedule_job as job

if os.environ.get('IS_HEROKU'):
    print(os.environ.get('FIREBASE_KEY'))

import firebase_admin
from firebase_admin import credentials, firestore, auth


cred = credentials.Certificate("config/firebase_pvt_key.json")
firebase_admin.initialize_app(cred)
db = firestore.client()


# It's necessary to import below class after initializing firebase

from module.product import Product
from module.user import UserLogin, RegisterUser

app = Flask(__name__)
api = Api(app)
CORS(app)
scheduler = APScheduler()
scheduler.init_app(app)
scheduler.start()


scheduler.add_job(id='notification_job', func=job.product_price_notification, trigger='interval', seconds=60)

api.add_resource(UserLogin, '/login')
api.add_resource(RegisterUser, '/register')
api.add_resource(Product, '/product')
#api.add_resource(FetchProduct, '/fetch_product')

if __name__ == '__main__':
    app.run()
