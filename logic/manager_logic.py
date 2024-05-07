import argparse
from sqlalchemy import select
from model.base_entity import ManagerEntity
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

engine = create_engine("postgresql://postgres:foxit@localhost/trello")

def get_session():
    Session = sessionmaker(bind=engine)
    session = Session()
    return session


class manager:
    def __init__(self):
        self.session = get_session()
        # self.create_admin_from_input()


    def create_admin(self,admin_name,admin_pass):
        admin = self.session.execute(select(ManagerEntity).filter_by(admin_name=admin_name))
        result_edited = admin.scalars().one_or_none()
        print(result_edited)
        if result_edited:
            print("admin is exist")
        else:
            db_model = ManagerEntity(admin_name=admin_name,admin_pass=admin_pass)
            self.session.add(db_model)
            self.session.commit()
            self.session.refresh(db_model)



