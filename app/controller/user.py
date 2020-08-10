from flask import jsonify, Blueprint, request
from http import HTTPStatus
from marshmallow.exceptions import ValidationError
from app.schemas.schemas import UserSchema, PostSchema , UserUpdateSchema
from app.models.model import User, Post
from app.utils.helper import check_existence, check_user , check_password
from flask_jwt_extended import (
    jwt_required,
    jwt_refresh_token_required,
    create_access_token,
    create_refresh_token,
    get_jwt_identity
)

user = Blueprint("user", __name__)


@user.route("/root", methods=["GET"])
@jwt_required
def test():

    return jsonify({"result": True})


@user.route("/user/login", methods=["POST"])
def login():

    data = request.json
    # print("datamiz", data)

    user_data = User.query.filter_by(email=data.get("email")).first()
    print("user data", user_data)
    if not user_data:
        return jsonify({"result": False, "MESSAGE": f"no user found with address {data.get('email')}"})

    result= check_password(user_data.password, data.get("password"))

    if result:
        schema = UserSchema()

        user = schema.dump(user_data)

        access_token = create_access_token(identity=user_data.id)
        refresh_token = create_refresh_token(identity=user_data.id)

        user.update(access=access_token, refresh=refresh_token)

        return jsonify(user)

    return jsonify({
        "message":"User email or password wrong"
    })

@user.route("/refresh/token", methods=["POST"])
@jwt_refresh_token_required
def refresh_token():

    user_id = get_jwt_identity()
    print("--------------", user_id)

    user_data = User.query.get(user_id)
    print("--------------", user_data)
    print("--------------", user_data.id)

    access_token = create_access_token(identity=user_data.id)

    refresh_token = create_refresh_token(identity=user_data.id)

    return jsonify({
        "access_token":access_token,
        "refresh_token":refresh_token
    })

@user.route("/test/<uuid:id>", methods=["GET"])
def user_func(id):
    posts = Post.query.all()

    print("postlar", posts)
    for post in posts:

        print("1", post.user.name)
        print("2", post.user.email)

    user_detail = User.query.filter_by(id=id).first()

    for post in user_detail.posts:
        print("3", post.title)
        print("4", post.content)

    return jsonify({"result": True})


@user.route("/user", methods=["GET"])
@jwt_required
def get_user():
    user_id=get_jwt_identity()
    
    user = User.query.filter_by(id=user_id).first()

    if user:
        return UserSchema().jsonify(user), HTTPStatus.OK

    return jsonify({"result": False})


@user.route("/users", methods=["GET"])
def get_users():

    users = User.query.all()

    return UserSchema().jsonify(users, many=True), HTTPStatus.OK


@user.route("/user", methods=["POST"])

def create_user():

    try:
        

        data = request.get_json()

        result = check_existence(data.get("email"))

        if not result:
            return jsonify({"result": False, "message": f"User with this {data.get('email')} already exists"}), HTTPStatus.NOT_FOUND

        user = UserSchema()
        new_user = user.load(data)
        new_user.save()

        user_id=new_user.id
        

        access_token = create_access_token(identity=user_id)
        refresh_token = create_refresh_token(identity=user_id)
        
        user= user.dump(new_user)
        print(user)
        user.update(access=access_token, refresh=refresh_token)
        
        return jsonify(user), HTTPStatus.OK

    except ValidationError as err:

        return jsonify(err.messages), HTTPStatus.NOT_FOUND


@user.route("/user", methods=["PUT"])
@jwt_required
def put_user():
    user_id=get_jwt_identity()

    data = request.get_json()

    user = User.query.filter_by(id=user_id).first()

    if user:
        serializer = UserUpdateSchema()

        user_up = serializer.load(data) #yoxla dumpdu yoxsa load

        user_update = user.update(**user_up)

        return jsonify({
            "message":"Updated Succesfully"
        }) ,HTTPStatus.OK

    else:
        return jsonify({"res": True}), HTTPStatus.BAD_REQUEST


@user.route("/user", methods=["DELETE"])
@jwt_required
def delete_user():
    user_id=get_jwt_identity()

    user=User.query.filter_by(id=user_id).first()


    if user:

        user.delete()

        return jsonify({"res": True}), HTTPStatus.OK

    else:
        return jsonify({"res": False}), HTTPStatus.NOT_FOUND
