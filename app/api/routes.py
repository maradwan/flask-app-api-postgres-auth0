from flask import Flask, request, jsonify
from uuid import uuid4
from .models import Raw_data, db, raw_data_schema, raw_datas_schema
from .swagger import SWAGGER_URL, API_URL, SWAGGERUI_BLUEPRINT
from .auth0 import cross_origin, requires_auth
from api import app
import http.client
from os import environ as env

client_id = env.get("CLIENT_ID")
client_secret = env.get("CLIENT_SECRET")
audience = env.get("API_IDENTIFIER")
auth0_domain = env.get("AUTH0_DOMAIN")


### swagger specific ###
app.register_blueprint(SWAGGERUI_BLUEPRINT, url_prefix=SWAGGER_URL)


# User can add id or auto generate new id
def check_id():
    try:
        return request.json['id']
    except:
        return uuid4()

    
# Create a Data
@app.route('/data/v1', methods=['POST'])
@cross_origin(headers=['Content-Type', 'Authorization'])
@requires_auth
def add_data():
    id = check_id()
    data = Raw_data.query.get(id)
    if data:
        return jsonify(id, 'Already exists in the database'),409

    try:
        eventtime = request.json['eventtime']
        devicename = request.json['devicename']
        item = request.json['item']
        detailstatus = request.json['detailstatus']
        filename = request.json['filename']
        linenumber = request.json['linenumber']

        new_raw_data = Raw_data(id, eventtime, devicename, item, detailstatus, filename, linenumber)

        db.session.add(new_raw_data)
        db.session.commit()
        return raw_data_schema.jsonify(new_raw_data)
    except:
        return jsonify('Bad post data'),400
    
    
# Get All Data
@app.route('/data/v1', methods=['GET'])
@cross_origin(headers=['Content-Type', 'Authorization'])
@requires_auth
def get_datas():
  all_raw_data = Raw_data.query.all()
  result = raw_datas_schema.dump(all_raw_data)
  return jsonify(result.data)


# Get Single Data
@app.route('/data/v1/<id>', methods=['GET'])
@cross_origin(headers=['Content-Type', 'Authorization'])
@requires_auth
def get_data(id):
  try:
      data = Raw_data.query.get(id)
      if data is None:
          return jsonify('Not Found'),404
      return raw_data_schema.jsonify(data)
  except:
      return jsonify('Misunderstood Request'),400


# Update a Data
@app.route('/data/v1/<id>', methods=['PUT'])
@cross_origin(headers=['Content-Type', 'Authorization'])
@requires_auth
def update_data(id):
  try:
      data = Raw_data.query.get(id)
  except:
      return jsonify('Request id is not UUID'),401

  if data is None:
      return jsonify('Not Found'),404

  try:
      eventtime = request.json['eventtime']
      devicename = request.json['devicename']
      item = request.json['item']
      detailstatus = request.json['detailstatus']
      filename = request.json['filename']
      linenumber = request.json['linenumber']

      data.eventtime = eventtime
      data.devicename = devicename
      data.item = item
      data.detailstatus = detailstatus
      data.filename = filename
      data.linenumber = linenumber
      db.session.commit()
      return raw_data_schema.jsonify(data)
  
  except:
      return jsonify('Misunderstood Request'),400

    
# Delete Data
@app.route('/data/v1/<id>', methods=['DELETE'])
@cross_origin(headers=['Content-Type', 'Authorization'])
@requires_auth
def delete_data(id):
  try:
      data = Raw_data.query.get(id)
  except:
      return jsonify('Misunderstood Request'),400

  if data is None:
      return jsonify('Not Found'),404
  db.session.delete(data)
  db.session.commit()

  return raw_data_schema.jsonify(data)


# Get Token from auth0
@app.route('/auth0/v1', methods=['POST'])
def auth0_token():
    try:
        username = request.json['username']
        password = request.json['password']
        conn = http.client.HTTPSConnection(f"{auth0_domain}")
        payload = f'{{"grant_type":"password", "username":"{username}", "password":"{password}", "client_id":"{client_id}","client_secret":"{client_secret}","audience":"{audience}"}}'
        headers = { 'content-type': "application/json" }
        conn.request("POST", "/oauth/token", payload, headers)
        res = conn.getresponse()
        data = res.read().decode('utf-8')
        return data
    except:
        return jsonify("Missing keys"),404
