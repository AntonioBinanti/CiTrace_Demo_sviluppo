# -*- coding: utf-8 -*-
"""
Created on Thu Nov 23 17:21:00 2023

@author: AntonioBinanti
"""

#%% Import librerie
from pydantic import BaseModel
from typing import Dict, List, Optional
from datetime import datetime

#%% Definizione Pydantic models di input ed output
class UserReg(BaseModel):
    new_user_preferences: List[str]
    
class UserPref(BaseModel):
    user_id: int #long
    device_info_id: int #long
    
class PredictionCluster(BaseModel):
    cluster: List[int]
    
class PredictionComponents(BaseModel):
    scorciatoie: Dict[str, int]
    
class Device(BaseModel):
    device_type: str
    class Config:
        orm_mode = True
    
class DeviceExt(Device):
    identifier: int
    owner_id: Optional[int] 
    #owners: Optional[List[str]] = [] #DA CONTROLLARE
    
class Request(BaseModel):
    event: str
    selector: Optional[str]
    timestamp: str
    page_url_current: Optional[str]
    component: str
    class Config:
        orm_mode = True
        
class RequestExt(Request):
    actualUser: int
    device_info: int
    request_id: int
    
class Component(BaseModel):
    title: str
    class Config:
        orm_mode = True
        
class ComponentExt(Component):
    component_id: int
    #users: Optional[List[int]]

class UserCreate(BaseModel):
    username: str
    user_IP_address: int
    role: str
    city: str
    interests: Optional[List[str]] = []
    logged_in: bool
    #logged_in_time: str
    main_language_used: str
    class Config:
        orm_mode = True

class User(BaseModel):
    username: str
    user_IP_address: int
    role: str
    city: str
    interests: Optional[List[Component]] = []
    logged_in: bool
    #logged_in_time: str
    main_language_used: str
    class Config:
        orm_mode = True
        
class UserUpdate(BaseModel):
    username: Optional[str]
    user_IP_address: Optional[int]
    role: Optional[str]
    city: Optional[str]
    interests: Optional[List[str]] = []
    logged_in: Optional[bool]
    #logged_in_time: str
    main_language_used: Optional[str]
    class Config:
        orm_mode = True
    
class UserExt(User):
    user_id: int
    device_info: Optional[List[Device]] = []
    
class UserRequests(User):
    user_id: int
    requests: Optional[List[RequestExt]] = []
    class Config:
        orm_mode = True
        
class ActionPredict(BaseModel):
    user_id: int
    browser_id: int
    year: int
    month: int
    day: int
    hour: int
    minute:int 
    day_week: Optional[int]
    class Config:
        orm_mode = True
