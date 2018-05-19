from database_setup import Branche,Base,Catogrey;
from sqlalchemy import  create_engine;
from sqlalchemy.orm import sessionmaker;
engine=create_engine('sqlite:///catogrey.db');
Base.metadata.bind=engine;
dbsession=sessionmaker(bind=engine);
session=dbsession();
for i in session.query(Catogrey).all():
    print i.id,"\t",i.name
for i in session.query(Branche).all():
    print i.id,"\t",i.name,"\t",i.catogrey_id;