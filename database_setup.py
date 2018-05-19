#shebang line for python 2
#!/usr/bin/env python
# nessary modules
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import Column, String, Integer, ForeignKey
engine = create_engine("sqlite:///catogrey.db")
Base = declarative_base()
# table to save every user data


class User(Base):
    __tablename__ = "user"
    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    email = Column(String(250), nullable=False)
    picture = Column(String(250), nullable=False)
# catogries used in this app


class Catogrey(Base):
    __tablename__ = "catogrey"
    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)

    @property
    def serialize(self):
        return {"id": self.id, "name": self.name}
# this branche table is containg the default branches and displayed for
# unregisteded user


class Branche(Base):
    __tablename__ = "branche"
    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    description = Column(String(250), nullable=False)
    catogrey_id = Column(Integer, ForeignKey("catogrey.id"))
    relathion = relationship(Catogrey)

    @property
    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "catogrey_id": self.catogrey_id

        }
# this table contain the user specfic branches or branches created by user


class UserBranche(Base):
    __tablename__ = "userbranche"
    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    description = Column(String(250), nullable=False)
    catogrey_id = Column(Integer, ForeignKey("catogrey.id"))
    catogrey = relationship(Catogrey)
    user_id = Column(Integer, ForeignKey("user.id"))
    user = relationship(User)


Base.metadata.create_all(engine)
