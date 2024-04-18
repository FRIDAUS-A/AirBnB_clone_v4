#!/usr/bin/python3
"""Inherits from the BaseModel class"""
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
import models

class State(BaseModel, Base):
    """State"""
    __tablename__ = "states"
    name = Column(String(128), nullable=False)
    cities = relationship("City", backref="state")

    if models.storage_t != 'db':
        @property
        def cities(self):
            content_state = storage.all(self)
            content_city = storage.all(City)
            common = []
            for value_state in content_state.values():
                for value_city in content_city.values():
                    if value_state.to_dict()["id"] == value_city.to_dict["id"]:
                        common.append(value_state)
            return (common)
