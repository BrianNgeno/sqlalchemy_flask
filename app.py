from flask import Flask, make_response, request, jsonify, abort, session
from flask_migrate import Migrate
from flask_cors import CORS
from flask_restful import Api,Resource
from werkzeug.exceptions import NotFound
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt


app =Flask(__name__)
CORS(app)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///test.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False
app.secret_key=b'\xa8 \xd3t\xf4\x88\x02\x9d'
# db = SQLAlchemy(app)
bcrypt = Bcrypt(app)

api = Api(app)
from models import db,Car, Owner, User
db.init_app(app)
migrate = Migrate(app,db)



@app.errorhandler(NotFound)
def handle_not_found(e):
    response = make_response(
        jsonify({'error': 'NotFound', 'message': 'The requested resource does not exist'}),
        404
    )
    response.headers['Content-Type'] = 'application/json'
    return response
app.register_error_handler(404, handle_not_found)

@app.route('/sessions/<string:key>',methods=['GET'])
def show_cookies(key):
    session['username']=session.get('username') or 'john_doe'
    response = make_response(jsonify({
        'session':{
            'session_key':key,
            'session_value':session[key],
            'session_access':session.accessed,
        },
        'cookie':[{cookie:request.cookies[cookie]}
            for cookie in request.cookies],}),200)
    response.set_cookie('cookie_name','cookie')
    return response

@app.before_request
def check_login():
    user_id = session.get('user_id')
    if user_id is None\
        and request.endpoint != 'home'\
        and request.endpoint != 'user_login'\
        and request.endpoint != 'car_list' \
        and request.endpoint != 'check_session' :
        return{"error":"unauthorized access"},401

class Login(Resource):
    def post(self):
        user_name = request.get_json()['user_name']
        user = User.query.filter(User.user_name == user_name).first()
        password=request.get_json()['password']
        if user.authenticate(password):
            session['user_id']=user.id
            return user.to_dict(),200
        return {"error":"invalid username or password "}

class CheckSession(Resource):
    def get(self):
        user = User.query.filter(User.id == session.get('user_id')).first()
        if user:
            return user.to_dict()
        else:
            return{'mesage':'401=Unauthorized user'}, 401

class Logout(Resource):
    def delete(self):
        session['user_id']=None
        return {'message':'logout success'}


class Index(Resource):
    def get(self):
        body={"message":'<h1>Welcome, Hello World!</h1>'}
        return make_response( body,200)


class Cars(Resource):
    def get(self):
        cars = []
        for car in Car.query.all():
            car_dict = car.to_dict()
            cars.append(car_dict)
        response = make_response(
            cars,
            200,
            {'Content-Type':'application/json'}
        )
        return response
    def post(self):
        new_car = Car(
            model=request.get_json()["model"],
            chasis_no = request.get_json()["chasis_no"],
            owner_id = request.get_json()["owner_id"],
        )
       
        if len(new_car.chasis_no) != 4:
            body = {"message":"the chasis number should be exactly 4 characters"}
            return make_response(body,200)
        db.session.add(new_car)
        db.session.commit()
        car_dict = new_car.to_dict()
        response= make_response(car_dict,201)
        return response


class CarById(Resource):    
    def get(self,id):
        car = Car.query.filter(Car.id==id).first()
     
        if car:
            car_dict = car.to_dict()
            response = make_response(car_dict,200,{'Content-Type':'application/json'})
            return response
        else:
            abort(404)
        
    def delete(self,id):
        car = Car.query.filter(Car.id==id).first()
        db.session.delete(car)
        db.session.commit()
        body  = {
            "delete-successful":True,
            "message":"car deleted successfully"
        }
        response = make_response(
            body,
            200
        )
        return response
      

    def patch(self,id):
        car = Car.query.filter(Car.id==id).first()
        for attr in request.form:
            setattr(review, attr, request.form.get(attr))

        db.session.add(car)
        db.session.commit()

        car_dict = car.to_dict()

        response = make_response(
            car_dict,
            200
        )

        return response

@app.route('/trigger404')
def trigger_404():
    return NotFound()

class Owners(Resource):
    def get(self):
        owners = []
        for owner in Owner.query.all():
            owner_dict = owner.to_dict()
            owners.append(owner_dict)
        response = make_response(
            owners,
            200,
            {'Content-Type':'application/json'}
        )
        return response
    def post(self):
        new_owner = Owner(
            name=request.form["name"],
            number = request.form["number"]
        )
        if len(new_owner.number) != 10:
            body = {"message":"the number should be exactly 10 characters"}
            return make_response(body,200)
        else:
            db.session.add(new_owner)
            db.session.commit()
            owner_dict = new_owner.to_dict()
            response= make_response(owner_dict,201)
            return response



api.add_resource(Index,'/', endpoint='home')
api.add_resource(Cars,'/cars',endpoint='car_list')
api.add_resource(Owners,'/owners',endpoint='owner_list')
api.add_resource(CarById,'/cars/<int:id>',endpoint='car')
api.add_resource(Login,'/login',endpoint='user_login')
api.add_resource(CheckSession,'/session',endpoint='check_session')
api.add_resource(Logout,'/logout',endpoint='user_logout')

if __name__ == '__main__':
    app.run(port=5000,debug=True)