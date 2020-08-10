from flask import jsonify, Blueprint, request
from http import HTTPStatus
from marshmallow.exceptions import ValidationError
from app.schemas.schemas import UserSchema, PostSchema
from app.models.model import User, Post
from app.utils.helper import check_existence, check_user
from flask_jwt_extended import (
    jwt_required,
    jwt_refresh_token_required,
    create_access_token,
    create_refresh_token,
    get_jwt_identity
)
import jwt
import os


post = Blueprint("post", __name__)


@post.route("/root", methods=["GET"])
@jwt_required
def test():

    return jsonify({"result": True})


@post.route("/posts", methods=["GET"])
@jwt_required
def get_posts():

    user_id = get_jwt_identity()
    # key=development.Development.JWT_SECRET_KEY
    # token = request.headers.get('Authorization').split(' ')[1]
    
    # print(jwt.decode(jwt=token, key=key,algorithms='HS256').get("identity"))
    

    posts = Post.query.filter_by(user_id=user_id).all()

    return PostSchema().jsonify(posts, many=True), HTTPStatus.OK


@post.route("/post/<uuid:id>", methods=["GET"])
@jwt_required
def get_post(id):

    user_id = get_jwt_identity()

    check = check_user(user_id)

    if not check:
        return jsonify({"result": False, "message": "error happened.check correct information please"}), HTTPStatus.BAD_REQUEST

    post = Post.query.filter_by(id=id, user_id=user_id).first()

    if post:

        return PostSchema().jsonify(post), HTTPStatus.OK

    else:

        return jsonify({"result": False, "message": "not found this post"}), HTTPStatus.NOT_FOUND


@post.route("/post", methods=['POST'])
@jwt_required
def create_post():

    try:
        user_id = get_jwt_identity()
        # print("--------------",user_id.id)
        data = request.json

        check = check_user(user_id)

        if not check:
            return jsonify({"result": False, "message": "error happened, check data if correct"}), HTTPStatus.BAD_REQUEST

        post = PostSchema().load(data)

        post.user_id = user_id

        post.save()

        return PostSchema().jsonify(post), HTTPStatus.OK

    except ValidationError as err:
        return jsonify(err.messages), HTTPStatus.NOT_FOUND


@post.route("/post/<uuid:id>", methods=["PUT"])
@jwt_required
def put_post(id):

    user_id = get_jwt_identity()

    data = request.get_json()

    post = Post.query.filter_by(id=id , user_id=user_id).first()

    if post:

        serializer = PostSchema()

        post_up = serializer.dump(data)

        post_update = post.update(**post_up)

        return PostSchema().jsonify(post), HTTPStatus.OK
        
    else:
        return jsonify({"res": True}), HTTPStatus.BAD_REQUEST


@post.route("/post/<uuid:id>", methods=["DELETE"])
@jwt_required
def delete_post(id):

    user_id = get_jwt_identity()

    post = Post.query.get(id)

    if post:

        post_id = Post.query.filter_by(user_id=user_id)

        if post_id:

            post.delete()

            return jsonify({"res": True}), HTTPStatus.OK

        else:
            return jsonify({"res": False, "messsage": "this post user not found "}), HTTPStatus.NOT_FOUND
    else:
        return jsonify({"res": False}), HTTPStatus.NOT_FOUND
