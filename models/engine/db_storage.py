#!/usr/bin/python3
"""DB STORAGE"""
from os import environ
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from models.base_model import Base

class DBStorage:
    """db storage"""
    __engine = None
    __session = None

    def __init__(self):
        """initialization for DBSORAGE class"""
        self.__engine = create_engine('mysql+mysqldb://{}:{}@{}/{}'.
                                      format(environ['HBNB_MYSQL_USER'],
                                             environ['HBNB_MYSQL_PWD'],
                                             environ['HBNB_MYSQL_HOST'],
                                             environ['HBNB_MYSQL_DB']),
                                      pool_pre_ping=True)
        if 'HBNB_ENV' in environ:
            if environ['HBNB_ENV'] == 'test':
                Base.metadata.drop_all(bind=self.__engine)

    def all(self, cls=None):
        """query the current database session"""
        from models.state import State
        from models.city import City
        from models.user import User
        from models.place import Place
        from models.review import Review
        from models.amenity import Amenity
        classes = {
                "State": State, "City": City, "Amenity": Amenity,
                "Place": Place, "Review": Review, "User": User
                    }
        dic = {}
        if cls:
            query = self.__session.query(cls)
            for obj in query:
                key = f"{obj.__class__.__name__}.{obj.id}"
                dic[key] = obj
        else:
            for cl in classes.values():
                query = self.__session.query(cl).all()
                for obj in query:
                    key = f"{obj.__class__.__name__}.{obj.id}"
                    dic[key] = obj
        return dic
    
    def count(self, cls=None):
        """count all the objecs"""
        if cls:
            count = self.__session.query(cls).count()
            return count
        else:
            for value in classses.values():
                count += self.__session.query(value).count()
            return count
    
    def get(self, cls, obj_id):
        obj = self.__session.query(cls).get(obj_id)
        if obj:
            return obj
        else:
            return None

    def new(self, obj):
        """add the object to the current database session"""
        self.__session.add(obj)

    def save(self):
        """commit all changes o fthe current database session"""
        self.__session.commit()

    def delete(self, obj=None):
        """delete from the current database session"""
        if obj:
            self.__session.delete(obj)

    def reload(self):
        """create all tables in the database"""
        from models.state import State
        from models.city import City
        from models.user import User
        from models.place import Place
        from models.review import Review
        from models.amenity import Amenity
        Base.metadata.create_all(bind=self.__engine)
        sess_factory = sessionmaker(bind=self.__engine, expire_on_commit=False)
        Session = scoped_session(sess_factory)
        self.__session = Session()

    def close(self):
        """close a session"""
        #self.__session.remove()
        self.__session.close()
