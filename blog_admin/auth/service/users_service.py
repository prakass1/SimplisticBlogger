from blog_admin.auth.model.users_model import Users
from blog_admin import db
from sqlalchemy import exc
import traceback


class UserService:
    def __init__(self, user_name, password, f_name, l_name, is_active):
        self.user_name = user_name
        self.password = password
        self.f_name = f_name
        self.l_name = l_name
        self.is_active = is_active

    def create_user(self):
        try: 
            user = Users(user_name=self.user_name, 
            password=self.password, 
            is_active=self.is_active,
            f_name=self.f_name,
            l_name=self.l_name)
            db.session.add(user)
            db.session.commit()
            return 0
        except exc.SQLAlchemyError:
            print("Error is -- ", traceback.print_exc())
            return -1
