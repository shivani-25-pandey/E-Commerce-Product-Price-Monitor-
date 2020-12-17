from flask import jsonify
from flask_restful import Resource, reqparse
from app import db

parser = reqparse.RequestParser()


class RegisterUser(Resource):

    def post(self):
        parser.add_argument('email', type=str)
        parser.add_argument('password', type=str)
        args = parser.parse_args()

        try:
            if args['email'] and args['password']:

                # Check if user already exist
                docs = db.collection('users').where('email', '==', args['email']).stream()

                user_data = None
                for doc in docs:
                    user_data = doc.to_dict()

                # If user doesn't exist create one
                if not user_data:
                    doc_ref = db.collection(u'users')
                    doc_ref.document().set({
                        'email': args['email'],
                        'password': args['password'],
                        'products': []
                    })
                    return jsonify({'message': 'User created successfully!', 'error': False, 'data': None})
                else:
                    return jsonify({'message': 'Email already exists', 'error': True, 'data': None})
            else:
                return jsonify({'message': 'Email or password is invalid', 'error': True, 'data': None})
        except:
            return jsonify({'message': 'Error while creating user', 'error': True, 'data': None})


class UserLogin(Resource):
    def post(self):
        parser.add_argument('email', type=str)
        parser.add_argument('password', type=str)
        args = parser.parse_args()

        docs = db.collection('users').where('email', '==', args['email']) \
            .where('password', '==', args['password']).stream()

        user_data = None
        for doc in docs:
            user_data = user_response(doc)

        if user_data:
            return jsonify({'message': '', 'error': False, 'data': user_data})
        else:
            return jsonify({'message': 'Email or password is invalid', 'error': True, 'data': None})
        # Retrieve all docs from firebase
        # doc_ref = db.collection('users').stream()
        # for doc in doc_ref:
        #     print(doc.to_dict())
        # try:
        #     doc_ref = db.collection('users').document(u'fPmMfgBmBP3OFl5XzrL')
        #     doc = doc_ref.get()
        #     print(doc.to_dict())
        # except google.cloud.exceptions.NotFound:
        #     print(u'No such document!')


def user_response(doc):
    user_data = doc.to_dict()
    user_data['id'] = doc.id
    del user_data['password']

    return user_data

