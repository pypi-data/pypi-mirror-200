from __future__ import annotations

import copy
import importlib
import pkgutil
from datetime import datetime
from types import NoneType
from typing import TYPE_CHECKING

from sqlalchemy import create_engine
from sqlalchemy.exc import PendingRollbackError, IntegrityError
from sqlalchemy.orm import sessionmaker, registry

from lprp_core.data.model.client import Client
from lprp_core.data.model.model_base import ModelBase
from lprp_core.data.model import *
from lprp_core.data.model.parking_garage import ParkingGarage
from lprp_core.data.model.usage_log import UsageLog
from lprp_core.data.model.user import User
from lprp_core.data.model.vehicle import Vehicle

if TYPE_CHECKING:
    pass


class PersistenceManager:
    CLASSES_TO_MAP = [Client, User, Vehicle, UsageLog, ParkingGarage]

    def __init__(self):
        # init persistent relational db
        self._engine = create_engine('sqlite:///data.sqlite',
                                     echo=False)
        self._map_orm()
        self._session_maker = sessionmaker(bind=self._engine)
        self._session = self._session_maker()

    def _map_orm(self):
        print("[INFO]: mapping classes...")
        mapper_registry = registry()
        # register every model class
        for cls in PersistenceManager.CLASSES_TO_MAP:
            print(f"[INFO]: mapping class {cls.__name__}")
            mapper_registry.mapped_as_dataclass(cls, kw_only=True)
        mapper_registry.metadata.create_all(bind=self._engine)

    @staticmethod
    def _prep_for_db(obj: ModelBase, parent: ModelBase = None) -> ModelBase:
        """prepares an object for the database TODO: try replacing with a cascade action"""
        if not isinstance(obj, ModelBase):
            raise TypeError(f"{obj} is not part of the persistence model")
        for attr_name in dir(obj):
            if attr_name.startswith("__"):
                continue
            # check / run for every attribute of the object
            attr = getattr(obj, attr_name)
            if isinstance(attr, ModelBase):
                # in case attribute is not a list of objects
                if attr is not parent:
                    setattr(obj, attr_name, PersistenceManager._prep_for_db(attr, parent))
            elif isinstance(attr, list):
                # in case attribute is a list of objects
                prepared_items = []
                for item in attr:
                    if item is not parent:
                        prepared_items.append(PersistenceManager._prep_for_db(item, parent))
                    else:
                        prepared_items.append(item)
                setattr(obj, attr_name, prepared_items)
        return obj

    def get_object(self, cls: type, id) -> ModelBase:
        """returns an object of type cls with id id"""
        session = self._session
        obj = session.get(cls, id)
        return obj

    def get_objects(self, cls: type) -> list[ModelBase]:
        """returns all objects of type cls"""
        session = self._session
        objs = session.query(cls).all()
        return objs

    def save_object(self, obj: ModelBase):
        """saves an object"""
        session = self._session
        session.add(obj)
        try:
            session.commit()
        except IntegrityError as e:
            session.rollback()
            raise e

    def save_objects(self, objs: list[ModelBase]):
        """saves a list of objects"""
        session = self._session
        for obj in objs:
            session.add(obj)
        try:
            session.commit()
        except IntegrityError as e:
            session.rollback()
            raise e

    def delete_object(self, obj: ModelBase):
        """deletes an object"""
        session = self._session
        session.delete(obj)
        session.commit()

    def delete_objects(self, objs: list[ModelBase]):
        """deletes a list of objects"""
        session = self._session
        for obj in objs:
            session.delete(obj)
        session.commit()
