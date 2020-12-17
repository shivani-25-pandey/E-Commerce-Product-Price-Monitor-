from flask import jsonify
from flask_restful import Resource, reqparse
import datetime as dt
from app import db
from module import utils

parser = reqparse.RequestParser()


class Product(Resource):

    def post(self):
        parser.add_argument('uid', type=str)
        parser.add_argument('url', type=str)
        args = parser.parse_args()

        try:
            if args['uid'] and args['url']:

                product = utils.scrap_product(args['url'])
                #print(product)
                if product:
                    doc_ref = db.collection('products')
                    doc_ref.document().set({
                        'dateAdded': dt.datetime.utcnow(),
                        'url': args['url'],
                        'uid': args['uid'],
                        'initialPrice': product[0],
                        'currentPrice': product[0],
                        'bestPrice': {
                          'price': product[0],
                          'date': dt.datetime.utcnow()
                        },
                        'title': product[1],
                        'needNotification': True,
                        'hasNotifiedToday': False
                    })
                    return jsonify({'message': 'Product added successfully!', 'error': False, 'data': None})
                else:
                    return jsonify({'message': 'Unable to retrieve product info', 'error': True, 'data': None})
            else:
                return jsonify({'message': 'Field missing', 'error': True, 'data': None})
        except Exception as e:
            return jsonify({'message': 'Error while adding product: '+ str(e), 'error': True, 'data': None})


    def get(self):
        parser.add_argument('uid', type=str)
        args = parser.parse_args()

        try:
            if args['uid']:

                #from module import utils
                #product = utils.scrap_product(args['url'])
                #print(product)
                #if product:
                doc_ref = db.collection('products')
                docs = doc_ref.stream()
                response={}
                count=0
                for doc in docs:
                    data=doc.to_dict()
                    #print(doc.to_dict())
                    #print(f"DocId {data['uid']} & UID:{args['uid']}")
                    if data['uid']==args['uid']:
                        response[str(count)]=doc.to_dict()
                        count+=1
                return jsonify({'message': 'Product Fetched successfully!','response':response,
                                    'error': False, 'data': None})
            else:
                return jsonify({'message': 'Unable to retrieve product info', 'error': True, 'data': None})
        except:
            return jsonify({'message': 'Error while Fetching product', 'error': True, 'data': None})

    def delete(self):
        parser.add_argument('uid', type=str)
        args = parser.parse_args()
        try:
            if args['uid']:

                # if product:
                doc_ref = db.collection('products')
                docs = doc_ref.stream()
                response = {}
                count = 0
                for doc in docs:
                    data = doc.to_dict()
                    if data['uid'] == args['uid']:
                        doc.reference.delete()
                return jsonify({'message': 'Product Deleted successfully!', 'response': response,
                                'error': False, 'data': None})
            else:
                return jsonify({'message': 'Unable to delete product', 'error': True, 'data': None})
        except:
            return jsonify({'message': 'Error while Deleting product', 'error': True, 'data': None})



