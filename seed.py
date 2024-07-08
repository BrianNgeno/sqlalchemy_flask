#!/usr/bin/env python3
from app import app
from models import db, Car, Owner, Mechanic, User
from faker import Faker
fake = Faker()

with app.app_context():

    # Drop all tables
    db.drop_all()

    # Create all tables
    db.create_all()

    # Clear the session
    db.session.remove()

    #seed users
    user1 = User(user_name="john_doe")
    user1.password_hash = "@dmin" 
    user2 = User(user_name="jane_doe")
    user2.password_hash = "@dmin123"
    
    db.session.add_all([user1, user2])
    db.session.commit()
    
    # Seed Owners
    owner4 = Owner(name="Mike")
    owner5 = Owner(name="Luke")
    owner6 = Owner(name="Tim")
    
    db.session.add_all([owner4, owner5, owner6])
    db.session.commit()

    # Seed Cars
    car4 = Car(model="Mustang", chasis_no="RTV9", owner=owner5)
    car5 = Car(model="Skudo", chasis_no="OP11", owner=owner5)
    car6 = Car(model="Nissan", chasis_no="QWE5", owner=owner6)

    db.session.add_all([car4, car5, car6])
    db.session.commit()

    # Seed Mechanics
    mechanic7 = Mechanic(name="Jane")
    mechanic8 = Mechanic(name="Liam")
    mechanic9 = Mechanic(name="Anne")
    
    db.session.add_all([mechanic7, mechanic8, mechanic9])
    db.session.commit()

    # Establish Many-to-Many Relationships
    owner4.mechanics.append(mechanic7)
    owner5.mechanics.append(mechanic8)
    owner6.mechanics.append(mechanic9)
   

    db.session.commit()