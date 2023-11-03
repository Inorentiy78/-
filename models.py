from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
#from server import app
db = SQLAlchemy()
bc = Bcrypt()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.Text(), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    phone = db.Column(db.String(100), unique=True, nullable=False)
    lastname = db.Column(db.String(100), nullable=False)  # фамилия
    name = db.Column(db.String(100), nullable=False)  # имя
    surname = db.Column(db.String(100), nullable=False)  # отчество

    def set_password(self, _password):
        self.password = bc.generate_password_hash(_password, 13)

    def check_pass(self, _password):
        return bc.check_password_hash(self.password, _password)

    @property
    def to_json(self):
        return {"id": self.id, "username": self.username, "password": self.password, "email": self.email,
                "FIO": str(self.lastname+" " + self.name+" " + self.surname),"phone": self.phone}


if __name__ == "__main__":
    with app.app_context():
        db.drop_all()
        db.create_all()
        new_user = User(username="admin", name="Имя", 
                        lastname="Фамилия", surname="Отчество", 
                        email="admin@myprof.kz", phone="+77475378879")
        new_user.set_password("mYnewGenerationPassword")
        db.session.add(new_user)
        db.session.commit()


