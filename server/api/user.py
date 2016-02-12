from flask import Blueprint, request, session
from sqlalchemy.exc import IntegrityError
from webargs import fields, validate
from webargs.flaskparser import parser, use_args
from server import model
from server.library.util import merge
from server.database import db
from server.response import respond, success
from server.api.schemas import UserSchema
from server.exc import NotFound, LoginError, AlreadyExists, InvalidEntity

User = Blueprint("user", __name__)

@User.route("/user", methods=["POST"])
@use_args(UserSchema())
def create(details):
    try:
        user = model.User(**details)
        db.session.add(user)

        # Log the user in
        session = user.login(db.session)
        db.session.commit()

        return respond(merge({ "key": session.key}, user.dump(UserSchema(exclude=("password",)))))
    except NotFound as nf:
        raise InvalidEntity("Institution", "domain", nf.meta["fields"]["domain"])
    except IntegrityError as ie:
        raise AlreadyExists("User", "email", details["email"])

@User.route("/user/<user>", methods=["GET", "PUT"])
def get_or_update_user(user): 
    if request.method == "GET":
        try:
            user_id = int(user)
        except ValueError:
            raise NotFound()

        user = model.User.get(user_id)
        schema = UserSchema(exclude=("password",))
        data, _ = schema.dump(user)

        return respond(data)
    elif request.method == "PUT":
        pass