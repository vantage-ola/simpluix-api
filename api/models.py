from marshmallow import Schema, fields, validate, pre_load
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

db = SQLAlchemy() # ORM
ma = Marshmallow()


class ResourceAddUpdateDelete():
    def add(self, resource):
        db.session.add(resource) 
        return db.session.commit()

    def update(self):
        return db.session.commit()
    
    def delete(self, resource): 
        db.session.delete(resource) 
        return db.session.commit()
        
category = db.Table('infotag',
 db.Column('info_id', db.Integer, db.ForeignKey('info.id')),
 db.Column('category_id', db.Integer, db.ForeignKey('category.id'))
)

class Info(db.Model, ResourceAddUpdateDelete):

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    location = db.Column(db.String(20))
    website = db.Column(db.String(50))
    address = db.Column(db.String(75))
    phone = db.Column(db.String(50))
    date_created = db.Column(db.TIMESTAMP, server_default=db.func.current_timestamp(), nullable=False)
    
    info_category = db.relationship('InfoCategory', secondary=category, backref=db.backref('tags', lazy= True))

    def __init__(self, name, location, website, address, phone):
        self.name = name
        self.location = location
        self.website = website
        self.address = address
        self.phone = phone

class InfoCategory(db.Model, ResourceAddUpdateDelete):

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), unique=True, nullable=False)

    def __init__(self, name):
        self.name = name

#declare the fields manually 
class InfoCategorySchema(ma.Schema):

    id = fields.Integer(dump_only=True)
    name = fields.String(required=True, validate=validate.Length(3)) #minimum of 3 characters
    url = ma.URLFor('service.infocategoryresource',id='<id>',_external=True)
    tags = fields.Nested('InfoSchema', many=True, exclude=('info_category'))

class InfoSchema(ma.Schema):
    
    id = fields.Integer(dump_only = True)
    name = fields.String(required=True, validate=validate.Length(4)) #minimum of 4 characters
    location = fields.String(required=True, validate=validate.Length(7)) #minimum of 4 characters
    website = fields.String(required=True, validate=validate.Length(8)) #minimum of 4 characters
    address = fields.String(required=True, validate=validate.Length(8)) #minimum of 4 characters
    phone = fields.Integer()
    date_created = fields.DateTime()
    url = ma.URLFor('service.inforesource', id='<id>',_external=True)
    info_category =fields.Nested(InfoCategorySchema, only=['id', 'url', 'name'],required=True)

    @pre_load
    def process_info_category(self, data):
        info_category = data.get('info_category')
        if info_category:
            if isinstance(info_category, dict): 
                info_category_name = info_category.get('name') 
            else: 
                info_category_name = info_category 
                info_category_dict = dict(name=info_category_name) 
        else:
            info_category_dict = {} 
            data['info_category'] = info_category_dict 
            return data
