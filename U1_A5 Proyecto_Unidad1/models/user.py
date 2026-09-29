from models import db

class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)

    @staticmethod
    def get_all():
        return User.query.all()

    @staticmethod
    def get_by_id(id):
        return db.session.get(User, id)

    @staticmethod
    def get_by_username(username):
        return User.query.filter_by(username=username).first()

    @staticmethod
    def get_by_email(email):
        return User.query.filter_by(email=email).first()

    @staticmethod
    def create(username, email, password):
        user = User(username=username, email=email, password=password)
        db.session.add(user)
        db.session.commit()

    @staticmethod
    def update(id, username, email):
        user = db.session.get(User, id)
        user.username = username
        user.email = email
        db.session.commit()

    @staticmethod
    def delete(id):
        user = db.session.get(User, id)
        db.session.delete(user)
        db.session.commit()