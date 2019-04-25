from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from sqlalchemy import text as sa_text
from sqlalchemy.dialects.postgresql import UUID

app = Flask(__name__)

# Init db
db = SQLAlchemy()
# Init ma
ma = Marshmallow(app)

# Data Class/Model
class Raw_data(db.Model):
  id = db.Column(UUID(as_uuid=True), primary_key=True, server_default=sa_text("uuid_generate_v4()"))
  eventtime = db.Column(db.DateTime(timezone=True))
  devicename = db.Column(db.String(200))
  item = db.Column(db.String(200))
  detailstatus = db.Column(db.String(200))
  filename = db.Column(db.String(200))
  linenumber = db.Column(db.Integer)

  def __init__(self, id, eventtime, devicename, item, detailstatus, filename, linenumber):
    self.id = id
    self.eventtime = eventtime
    self.devicename = devicename
    self.item = item
    self.detailstatus = detailstatus
    self.filename = filename
    self.linenumber = linenumber

# raw_data Schema
class RawdataSchema(ma.Schema):
    class Meta:
        fields = ('id', 'eventtime', 'devicename', 'item', 'detailstatus', 'filename', 'linenumber')

# Init schema
raw_data_schema = RawdataSchema(strict=True)
raw_datas_schema = RawdataSchema(many=True, strict=True)
