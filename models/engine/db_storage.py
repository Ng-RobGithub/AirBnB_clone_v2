#!/usr/bin/python3
"""
Defines the DBStorage class
"""
import os
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy import create_engine
from models.base_model import Base
from models.state import State
from models.city import City


class DBStorage:
    """
    DBStorage class
    """
    __engine = None
    __session = None

    def __init__(self):
        """
        Initializes the DBStorage instance
        """
        user = os.getenv('HBNB_MYSQL_USER')
        pwd = os.getenv('HBNB_MYSQL_PWD')
        host = os.getenv('HBNB_MYSQL_HOST')
        db = os.getenv('HBNB_MYSQL_DB')

        self.__engine = create_engine('mysql+mysqldb://{}:{}@{}/{}'.
                                      format(user, pwd, host, db),
                                      pool_pre_ping=True)
        if os.getenv('HBNB_ENV') == 'test':
            Base.metadata.drop_all(bind=self.__engine)

            def all(self, cls=None):
                """
                Queries all objects depending of the class name
                """
                new_dict = {}
                if cls:
                    objects = self.__session.query(eval(cls)).all()
                    for obj in objects:
                        key = "{}.{}".format(obj.__class__.__name__, obj.id)
                        new_dict[key] = obj
                    else:
                        for cls in [State, City]:
                            objects = self.__session.query(cls).all()
                            for obj in objects:
                                key = "{}.{}".format(obj.__class__.__name__,
                                                     obj.id)
                                new_dict[key] = obj
                                return new_dict

            def new(self, obj):
                """
                Adds the object to the current database session
                """
                if obj:
                    self.__session.add(obj)

            def save(self):
                """
                Commits all changes of the current database session
                """
                self.__session.commit()

            def delete(self, obj=None):
                """
                Deletes obj from the current database session
                """
                if obj:
                    self.__session.delete(obj)

            def reload(self):
                """
                Creates all tables in the database and the current database
                session
                """
                Base.metadata.create_all(self.__engine)
                Session = sessionmaker(bind=self.__engine,
                                       expire_on_commit=False)
                self.__session = scoped_session(Session)

            def close(self):
                """
                Calls remove() method on the private session attribute
                """
                self.__session.remove()
