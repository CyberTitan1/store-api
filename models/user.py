from db import db

class User(db.Model):

    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    password = db.Column(db.String(80), nullable=False)

    @classmethod
    def get_all_users(cls):
        user_list = []
        users = cls.query.all()
        for user in users:
            user_list.append(
                {
                    "id": user.id,
                    "name": user.name,
                    "password": user.password,
                }
            )
        return user_list
    
    @classmethod
    def get_user_by_id(cls, user_id):
        try:
            user = cls.query.get(user_id)
            if user:
                return True, user
            else:
                return None
        except Exception as e:
            return False
            

    @classmethod
    def create_user(cls, user_name, User_password):
        try:
            user = cls(name=user_name, password=User_password)
            db.session.add(user)
            db.session.commit()
            return True, user
        except Exception as e:
            db.session.rollback()
            return False, e
        
    @classmethod
    def delete_user(cls, user_id):

        try:
            user = cls.query.get(user_id)
            if user:
                db.session.delete(user)
                db.session.commit()
                return True
            else:
                return None
        except Exception as e:
            db.session.rollback()
            return False

    @classmethod
    def update_user(cls, user_id, name, password):
        
        try:
            user = cls.query.get(user_id)
            if user:
                user.name = name
                user.password = password 
                db.session.commit()
                return True 
            else:
                return None
        except Exception as e:
            db.session.rollback()
            return False
        
    @classmethod
    def verify_user_details(cls, user_name, user_password):
        try:
            user = cls.query.filter_by(name=user_name, password=user_password).one()
            if user:
                return True, user
            else:
                return None
        except Exception as e:
            return False
        







        

        

