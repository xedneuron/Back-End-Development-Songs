from . import app
import os
import json
from flask import jsonify, request, make_response, abort, url_for  # noqa; F401

SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
json_url = os.path.join(SITE_ROOT, "data", "pictures.json")
data: list = json.load(open(json_url))

######################################################################
# RETURN HEALTH OF THE APP
######################################################################


@app.route("/health")
def health():
    return jsonify(dict(status="OK")), 200

######################################################################
# COUNT THE NUMBER OF PICTURES
######################################################################


@app.route("/count")
def count():
    """return length of data"""
    if data:
        return jsonify(length=len(data)), 200

    return {"message": "Internal server error"}, 500


######################################################################
# GET ALL PICTURES
######################################################################
@app.route("/picture", methods=["GET"])
def get_pictures():
    """returns all of the pictures"""
    if data:
        return jsonify(data), 200
    else:
        return {"message":"404 not found"}, 404

    return {"message": "Internal server error"}, 500
    

######################################################################
# GET A PICTURE
######################################################################


@app.route("/picture/<int:id>", methods=["GET"])
def get_picture_by_id(id):
    """returns all of the pictures"""
    pass
    if data:
        for i in data:
            if i["id"] == id:
                return jsonify(i), 200
        return {"message":"404 not found"}, 404
    else:
        return {"message":"404 not found"}, 404

    return {"message": "Internal server error"}, 500
    


######################################################################
# CREATE A PICTURE
######################################################################
@app.route("/picture", methods=["POST"])
def create_picture():
    req = request.get_json()
    if req is None:
        return jsonify({"message":"400 invalid request"}), 400
    pass
    if data:
        jar = False
        for i in data:
            if req["id"] == i["id"]:
                jar = i

        if jar:
            return jsonify({"Message": 
            f"picture with id {req['id']} already present"}), 302
        
        try:
            data.append(req)
            return jsonify(req), 201
        except:
            return jsonify({"message":"500 server err"}), 500
        


######################################################################
# UPDATE A PICTURE
######################################################################


@app.route("/picture/<int:id>", methods=["PUT"])
def update_picture(id):
    req = request.get_json()
    if req is None:
        return jsonify({"message":"400 invalid request"}), 400
    pass
    if data:
        for i, json_dict in enumerate(data):
            if json_dict["id"] == req["id"]:
                data[i] = req
                return jsonify({"message":"update success"}), 200
        return jsonify({"message": "picture not found"}), 404

    return jsonify({"message":"500 server err"}), 500

######################################################################
# DELETE A PICTURE
######################################################################
@app.route("/picture/<int:id>", methods=["DELETE"])
def delete_picture(id):
    if data:
        for num, i in enumerate(data):
            if id == i["id"]:
                data.pop(num)
                return jsonify(None), 204
        return jsonify({"message": "picture not found"}), 404
        
    return jsonify({"message":"500 server err"}), 500
