#!/usr/bin/env python3

# Program: create_planes.py
# Author: Perry Brandiezs
# Date: May 1, 2019
# Last Updated: May 28, 2019
#
# This program populates the ItemCatalog database
# with users and several planes for testing.
#

import psycopg2
from sqlalchemy import create_engine
from sqlalchemy import exc
from sqlalchemy.orm import sessionmaker
from models import Base, User, ItemCatalog, Category
import logging

# Set logger level to info
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# Connect to Database and create database session
# engine = create_engine('sqlite:////var/www/html/catalog/ItemCatalog.db')
engine = create_engine('postgres+psycopg2:///ItemCatalog')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

# Add users
NewUser = User(
    email="pbrandiezs@gmail.com",
    picture="https://platform-lookaside.fbsbx.com/platform/profilepic/"
            "?asid=2296167867307191"
            "&height=200&width=200"
            "&ext=1559163571"
            "&hash=AeTcZcYDm6Y6E-zk",
    username="Perry Brandiezs"
    )
try:
    session.add(NewUser)
    session.commit()
    logging.info("User %s added" % NewUser.username)
except exc.IntegrityError:
    logging.warning("Not added - User %s" % NewUser.username)
    session.rollback()

NewUser = User(
    email="mickeymouse@disney.com",
    picture="https://upload.wikimedia.org/wikipedia/en/thumb/d/d4/"
            "Mickey_Mouse.png/220px-Mickey_Mouse.png",
    username="Mickey Mouse"
    )
try:
    session.add(NewUser)
    session.commit()
    logging.info("User %s added" % NewUser.username)
except exc.IntegrityError:
    logging.warning("Not added - User %s" % NewUser.username)
    session.rollback()

# Add Categories
NewCategory = Category(
    category_name="Gulfstream"
    )
try:
    session.add(NewCategory)
    session.commit()
    logging.info("Category %s added" % NewCategory.category_name)
except exc.IntegrityError:
    logging.warning("Not added - Category %s" % NewCategory.category_name)
    session.rollback()

NewCategory = Category(
    category_name="Crop Duster"
    )
try:
    session.add(NewCategory)
    session.commit()
    logging.info("Category %s added" % NewCategory.category_name)
except exc.IntegrityError:
    logging.warning("Not added - Category %s" % NewCategory.category_name)
    session.rollback()

NewCategory = Category(
    category_name="Falcon"
    )
try:
    session.add(NewCategory)
    session.commit()
    logging.info("Category %s added" % NewCategory.category_name)
except exc.IntegrityError:
    logging.warning("Not added - Category %s" % NewCategory.category_name)
    session.rollback()

NewCategory = Category(
    category_name="Embraer"
    )
try:
    session.add(NewCategory)
    session.commit()
    logging.info("Category %s added" % NewCategory.category_name)
except exc.IntegrityError:
    logging.warning("Not added - Category %s" % NewCategory.category_name)
    session.rollback()

NewCategory = Category(
    category_name="Aerospatiale/BAC"
    )
try:
    session.add(NewCategory)
    session.commit()
    logging.info("Category %s added" % NewCategory.category_name)
except exc.IntegrityError:
    logging.warning("Not added - Category %s" % NewCategory.category_name)
    session.rollback()

# Add planes
NewPlane = ItemCatalog(
    category_id=1,
    item_name="G650ER",
    item_description="Long range private jet",
    user_id=1
    )
try:
    session.add(NewPlane)
    session.commit()
    logging.info("Plane %s added" % NewPlane.item_name)
except exc.IntegrityError:
    logging.warning("Not added - Plane %s" % NewPlane.item_name)
    session.rollback()

NewPlane = ItemCatalog(
    category_id=1,
    item_name="G550",
    item_description="A very nice jet",
    user_id=1
    )
try:
    session.add(NewPlane)
    session.commit()
    logging.info("Plane %s added" % NewPlane.item_name)
except exc.IntegrityError:
    logging.warning("Not added - Plane %s" % NewPlane.item_name)
    session.rollback()

NewPlane = ItemCatalog(
    category_id=1,
    item_name="G650ER",
    item_description="Mickey Mouse's Long range private jet",
    user_id=2
    )
try:
    session.add(NewPlane)
    session.commit()
    logging.info("Plane %s added" % NewPlane.item_name)
except exc.IntegrityError:
    logging.warning("Not added - Plane %s" % NewPlane.item_name)
    session.rollback()

NewPlane = ItemCatalog(
    category_id=2,
    item_name="Piper Cub",
    item_description="Little yellow airplane that spews toxic chemicals"
                     " on the food supply to kill beneficial insects.",
    user_id=1
    )
try:
    session.add(NewPlane)
    session.commit()
    logging.info("Plane %s added" % NewPlane.item_name)
except exc.IntegrityError:
    logging.warning("Not added - Plane %s" % NewPlane.item_name)
    session.rollback()

NewPlane = ItemCatalog(
    category_id=3,
    item_name="10X",
    item_description="The Dassault Mystere/Falcon 10 is an early corporate"
                     " jet aircraft developed by French aircraft"
                     " manufacturer Dassault Aviation.",
    user_id=1
    )
try:
    session.add(NewPlane)
    session.commit()
    logging.info("Plane %s added" % NewPlane.item_name)
except exc.IntegrityError:
    logging.warning("Not added - Plane %s" % NewPlane.item_name)
    session.rollback()

NewPlane = ItemCatalog(
    category_id=4,
    item_name="Phenom 100",
    item_description="The Embraer EMB-500 Phenom 100 is a very light jet"
                     " developed by Brazilian aircraft manufacturer Embraer.",
    user_id=1
    )
try:
    session.add(NewPlane)
    session.commit()
    logging.info("Plane %s added" % NewPlane.item_name)
except exc.IntegrityError:
    logging.warning("Not added - Plane %s" % NewPlane.item_name)
    session.rollback()

NewPlane = ItemCatalog(
    category_id=5,
    item_name="Concorde",
    item_description="The Aerospatiale/BAC Concorde is a French-British"
                     " turbojet-powered supersonic passenger airliner that"
                     " was operated from 1976 until 2003. It had a maximum"
                     " speed over twice the speed of sound at Mach 2.04"
                     " (1,354 mph or 2,180 km/h at cruise altitude)"
                     ", with seating for 92 to 128 passengers.",
    user_id=1
    )
try:
    session.add(NewPlane)
    session.commit()
    logging.info("Plane %s added" % NewPlane.item_name)
except exc.IntegrityError:
    logging.warning("Not added - Plane %s" % NewPlane.item_name)
    session.rollback()
