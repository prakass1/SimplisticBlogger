from blog_admin.auth.model.users_model import Users
from blog_admin import db
from sqlalchemy import exc
import traceback


class UserService:
    def create_user(self, user_name, password, f_name, l_name="", is_active=False):
        try: 
            user = Users(user_name=user_name, 
            password=password, 
            is_active=is_active,
            f_name=f_name,
            l_name=l_name)
            db.session.add(user)
            db.session.commit()
            return 0
        except exc.SQLAlchemyError:
            print("Error is -- ", traceback.print_exc())
            return -1
    
    def query_single_user(self, user_name):
        result = Users.query.filter_by(user_name=user_name).first()
        if result is None:
            return -1
        else:
            return result
    

