from app import bcrypt
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from sqlalchemy.orm import validates
from sqlalchemy_serializer import SerializerMixin
from sqlalchemy.ext.hybrid import hybrid_property




metadata = MetaData(naming_convention={
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s"
})
db = SQLAlchemy(metadata=metadata)

# Define Many-to-Many Table
owner_mechanics = db.Table(
    'owner_mechanics',
    db.Column('owner_id', db.Integer, db.ForeignKey('owners.id'), primary_key=True),
    db.Column('mechanic_id', db.Integer, db.ForeignKey('mechanics.id'), primary_key=True)
)

class User(db.Model,SerializerMixin):
    __tablename__='users'
    id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String, nullable=False,unique=True)
    _password_hash = db.Column(db.String,nullable=True)

    def __repr__(self):
        return f'user {self.user_name}'

    @hybrid_property
    def password_hash(self):
        return self._password_hash

    @password_hash.setter
    def password_hash(self, password):
        self._password_hash = bcrypt.generate_password_hash(password).decode("utf-8")


    def authenticate(self, password):
        return bcrypt.check_password_hash(self._password_hash, password.encode('utf-8'))


class Car(db.Model, SerializerMixin):
    __tablename__ = 'cars'
    serialize_only = ("id", "model", "chasis_no", "owner.name")
    serialize_rules = ()
    id = db.Column(db.Integer, primary_key=True)
    model = db.Column(db.String)
    chasis_no = db.Column(db.String)
    owner_id = db.Column(db.Integer, db.ForeignKey("owners.id"))
    owner = db.relationship("Owner", back_populates="cars")
    __table_args__ = (
        db.CheckConstraint('LENGTH(chasis_no) = 4'),
    )


    def __repr__(self):
        return f'Car of chasis no {self.chasis_no} is of model {self.model}'

class Owner(db.Model, SerializerMixin):
    __tablename__ = 'owners'
    serialize_rules = ('-cars.owners', '-mechanics.owners',)
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    cars = db.relationship("Car", back_populates="owner", cascade='all, delete-orphan')
    mechanics = db.relationship("Mechanic", secondary=owner_mechanics, back_populates="owners")
    number = db.Column(db.Integer,nullable=True)

    def __repr__(self):
        return f'Owner {self.name} is created successfully'

    @validates('number')
    def validates_number(self, key,number):
        if len(number) != 10 or not number.isdigit():
            # raise ValueError("number provided should be digits not less than 10")
            pass
        return number

class Mechanic(db.Model):
    __tablename__ = "mechanics"
    serialize_rules = ('-owners.mechanics')
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    owners = db.relationship("Owner", secondary=owner_mechanics, back_populates="mechanics")

    def __repr__(self):
        return f'Mechanic {self.name} is created successfully'
