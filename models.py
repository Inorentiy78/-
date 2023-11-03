from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from server import app # комментировать при запуске server.py эту строку
db = SQLAlchemy(app)  # когда запускаете server.py уберите из скобок app
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


class Profession(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    description = db.Column(db.Text(), nullable=True)
    img_url = db.Column(db.Text(), nullable=True)

class ProfessionPartner(db.Model):
    profession_id = db.Column(db.Integer, db.ForeignKey('profession.id'), nullable=False, primary_key=True)
    partner_id = db.Column(db.Integer, db.ForeignKey('partners.id'), nullable=False, primary_key=True)


class Partners(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    link_url = db.Column(db.Text(), nullable=False)
    logo_img = db.Column(db.String(100),  nullable=False)
    description = db.Column(db.Text(),  nullable=False)
    professions = db.relationship('Profession', secondary=ProfessionPartner.__table__, lazy='subquery',
        backref=db.backref('partners', lazy=True))

    @property
    def to_json(self):
        return {"id": self.id, "name": self.name, "link_url": self.link_url, "description": self.description,
                "professions": self.professions }


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

        professions = [ {
            'name': "руководитель",  #1
            "description": "",
            "img_url": ""
        },{
            'name': "преподаватель", #2
            "description": "",
            "img_url": ""
        },{
            'name': "художник", #3
            "description": "",
            "img_url": ""
        },{
            'name': "диктор", #4
            "description": "",
            "img_url": ""
        },{
            'name': "водитель", #5
            "description": "",
            "img_url": ""
        },{
            'name': "спасатель", #6
            "description": "",
            "img_url": ""
        },{
            'name': "ветеринар", #7
            "description": "",
            "img_url": ""
        },{
            'name': "путешественник", #8
            "description": "",
            "img_url": ""
        },{
            'name': "лингвист", #9
            "description": "",
            "img_url": ""
        },{
            'name': "технарь", #10
            "description": "",
            "img_url": ""
        },{
            'name': "стилист", #11
            "description": "",
            "img_url": ""
        },{
            'name': "модель", #12
            "description": "",
            "img_url": ""
        },{
            'name': "исследователь", #13
            "description": "",
            "img_url": ""
        },{
            'name': "программист", #14
            "description": "",
            "img_url": ""
        },{
            'name': "переводчик", #15
            "description": "", 
            "img_url": ""
        },{
            'name': "спортивный тренер", #16
            "description": "",
            "img_url": ""
        },{
            'name': "адвокат", #17
            "description": "",
            "img_url": ""
        },{
            'name': "бухгалтер", #18
            "description": "", 
            "img_url": ""
        },{
            'name': "военный", #19
            "description": "",
            "img_url": ""
        },{
            'name': "роботехник", #20
            "description": "",
            "img_url": ""
        },{
            'name': "косметолог", #21
            "description": "",
            "img_url": ""
        },{
            'name': "маркетолог", #22
            "description": "",
            "img_url": ""
        },{
            'name': "дизайнер", #23
            "description": "",
            "img_url": ""
        },{
            'name': "повар", #24
            "description": "",
            "img_url": ""
        },{
            'name': "хареограф", #25
            "description": "",
            "img_url": ""
        },{
            'name': "парикмахер", #26
            "description": "",
            "img_url": ""
        },{
            'name': "экскурсовод", #27
            "description": "", 
            "img_url": ""
        },
        ]

        for profession in professions:
            new_prof = Profession(name=profession['name'],description=profession['description'], img_url=profession['img_url'])
            db.session.add(new_prof)
            db.session.commit()

        partners = [{
            "name": "Казиту", #1
            "link_url" : "",
            "logo_img" : "",
            "description" :""
        },{
            "name": "РВТК", #2
            "link_url" : "",
            "logo_img" : "",
            "description" :""
        },
        ]

        for partner in partners:
            new_partner = Partners(name=partner['name'],link_url=partner['link_url'], logo_img=partner['logo_img'],
                                 description= partner['description'])
            db.session.add(new_partner)
            db.session.commit()

        #  здесь напишите связи профессии с партнерами. 
        # типа в каком из партнеров есть такая профессия 
        # или можно обучится. по id. 
        # рядом с каждой профессией написал в комментах их id чтобы не считать каждый раз
        professionpartners = [{
            "profession_id": 1,
            "partner_id":1
        },{
            "profession_id": 2,
            "partner_id":1
        },{
            "profession_id": 3,
            "partner_id":1
        },{
            "profession_id": 4,
            "partner_id":1
        },
        ]

        


