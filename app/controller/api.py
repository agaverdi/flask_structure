from flask import jsonify, Blueprint ,request
from http import HTTPStatus
from app.schemas.schemas import CarSchema
from app.models.model import Cars
from marshmallow.exceptions import ValidationError
from ..config.settings.extensions import  db

api=Blueprint('api',__name__)

@api.route("/",methods=["GET"])
def test():
    return jsonify({"result from api":True})

@api.route("/cars", methods=["GET"])
def get_all_books():

    cars = Cars.query.all()

    return CarSchema().jsonify(cars, many=True), HTTPStatus.OK




@api.route("/cars/<uuid:id>", methods=["GET"])
def get_book(id):

    car = Cars.query.filter_by(id=id).first()

    if car:    
        return CarSchema().jsonify(car),HTTPStatus.OK


    return jsonify({"result": False})

@api.route("/cars", methods=["POST"])
def create_book():
    try:
        data = request.json

        serializer =  CarSchema()
        
        car = serializer.load(data)
        car.save()
        
        
        return CarSchema().jsonify(car),HTTPStatus.OK

    except ValidationError as err:

        return jsonify(err.message), HTTPStatus.NOT_FOUND



def update(self,**car):
    for key, value in car.items():
            setattr(self, key,value)
            return self.save()


@api.route("/cars/<uuid:id>", methods=["PUT"])
def put_cars(id):

    data=request.get_json()

    car=Cars.query.filter_by(id=id).first()

    if car:
        serializer=CarSchema()

        Car=serializer.dump(data)

        car_update=car.update(**Car)

        return CarSchema().jsonify(car), HTTPStatus.OK

    else:
        return jsonify({"res":True}), HTTPStatus.BAD_REQUEST

    
@api.route("/cars/<uuid:id>",methods=["DELETE"])
def delete_car(id):
    car=Cars.query.get(id)
    
    if car:
        car.delete()

        return jsonify({"res":True}), HTTPStatus.OK
    
    else:
        return jsonify({"res":False}), HTTPStatus.BAD_REQUEST
