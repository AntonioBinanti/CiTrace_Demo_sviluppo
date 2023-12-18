# -*- coding: utf-8 -*-
"""
Created on Thu Nov 23 17:20:00 2023

@author: AntonioBinanti
"""
#%% Import librerie
from sqlalchemy.orm import Session
from . import schemas, models, database
import pandas as pd

#%% Funzioni

def get_new_id(db: Session, table: str):
    new_id = 0
    postgresql_connection = database.engine.connect()
    table = pd.read_sql(f"{table}", postgresql_connection)
    postgresql_connection.close()
    new_id = len(table)
    return new_id

def get_components(db: Session):
    return db.query(models.Components).all()

def get_components_list(db: Session):
    components = get_components(db)
    components_list = []
    for c in components:
        components_list.append(c.title)
    return components_list

def get_component(db: Session, title: str):
    return db.query(models.Components).filter(models.Components.title == title).first()

#def create_component(db: Session, component: schemas.Component):
#    component_model = models.Components(**component.dict())
#    db.add(component_model)
#    db.commit()
#    db.refresh(component_model)
#    return component_model

def create_component(db: Session, component: str):
    component_model = models.Components(title = component)
    db.add(component_model)
    db.commit()
    db.refresh(component_model)
    return component_model

def add_interests_to_user(db: Session, interests_list: list[str], user_model: models.AllUsers):
    if interests_list is not None:
        for comp in interests_list:
            db_component = get_component(db, comp)
            if db_component is None:
                db_component = create_component(db, comp)
            user_model.interests.append(db_component)
    db.add(user_model)
    db.commit()
    db.refresh(user_model)
    return user_model

def get_user(db: Session, username: str):
    return db.query(models.AllUsers).filter(models.AllUsers.username == username).first()

def get_user_id(db: Session, user_id: int):
    return db.query(models.AllUsers).filter(models.AllUsers.user_id == user_id).first()

def get_user_devices(db: Session, db_user: schemas.UserExt):
    devices_list = db_user.device_info
    return devices_list

def get_user_requests(db: Session, user_id: int, device_id: int):
    return db.query(models.Request).filter(models.Request.actualUser == user_id, models.Request.device_info == device_id).all() 

def get_user_interests(db: Session, db_user: schemas.UserExt):
    components_list = db_user.interests
    interests_list = []
    if interests_list is not None:
        for comp in components_list:
            interests_list.append(comp.title)
    return interests_list

def get_users(db: Session):
    return db.query(models.AllUsers).all()


def create_user(db: Session, user: schemas.UserCreate):
    user_id = get_new_id(db, "allUsers")
    user_model = models.AllUsers(
        user_id = user_id,
        username = user.username,
        user_IP_address = user.user_IP_address,
        role = user.role,
        city = user.city,
        logged_in = user.logged_in,
        main_language_used = user.main_language_used
        )
    #user_model = models.AllUsers(**user.dict())
    add_interests_to_user(db, interests_list = user.interests, user_model = user_model)
    #db.add(user_model)
    #db.commit()
    #db.refresh(user_model)
    return user_model

def get_device_type(db: Session, device_type: str):
    return db.query(models.Device_info).filter(models.Device_info.device_type == device_type).all()

def get_device_model_user(db: Session, device_type: str, user_id: int):
    return db.query(models.Device_info).filter(models.Device_info.device_type == device_type, models.Device_info.owner_id == user_id).first()

def get_device_identifier(db: Session, identifier: int):
    return db.query(models.Device_info).filter(models.Device_info.identifier == identifier).first()

def get_devices(db: Session):
    return db.query(models.Device_info).all()

def create_device_to_user(db: Session, device: schemas.Device, user_id: int):
    device_model = models.Device_info(**device.dict(), owner_id=user_id)
    db.add(device_model)
    db.commit()
    db.refresh(device_model)
    return device_model

def create_request(db: Session, request: schemas.Request, user_id: int, device: int):
    request_id = get_new_id(db, "request")
    request_model = models.Request(**request.dict(), request_id = request_id, actualUser = user_id, device_info = device)
    db.add(request_model)
    db.commit()
    db.refresh(request_model)
    return request_model
    
def update_user(db: Session, user_updated: schemas.UserUpdate, db_user: schemas.UserExt):
    user_data = user_updated.dict(exclude_unset = True) #Filtraggio dei soli valori inseriti dall'utente
    new_interests = user_data["interests"] 
    user_data["interests"] = []
    for key, value in user_data.items():
        setattr(db_user, key, value)
    db_user = add_interests_to_user(db = db, interests_list = new_interests, user_model = db_user)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def update_device(db: Session, device_updated: schemas.Device, db_device: schemas.DeviceExt):
    device_data = device_updated.dict(exclude_unset = True) #Filtraggio dei soli valori inseriti dall'utente
    for key, value in device_data.items():
        setattr(db_device, key, value)
    db.add(db_device)
    db.commit()
    db.refresh(db_device)
    return db_device

def get_requests(db: Session):
    return db.query(models.Request).limit(10).all()

def get_request_id(db: Session, request_id: int):
    return db.query(models.Request).filter(models.Request.request_id == request_id).first()
