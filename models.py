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
            "description": "Руководитель — это человек, который управляет частью работы организации. Например, финансами, логистикой, продажами, кадровой политикой. Руководитель принимает управленческие решения: решает, как и что нужно делать, чтобы компания достигла целей.",
            "img_url": "https://top-fon.com/uploads/posts/2023-01/1674627690_top-fon-com-p-upravlenie-personalom-fon-dlya-prezentatsi-7.png"
        },{
            'name': "преподаватель", #2
            "description": "Преподаватель – это педагог, наставник, учитель, который обучает слушателей какой-либо академической дисциплине или направлению профессиональных знаний по учебной программе средней или высшей школы.",
            "img_url": ""
        },{
            'name': "художник", #3
            "description": "К творческим профессиям можно отнести такие, как музыкант, художник, скульптор, режиссер, актер, писатель, фотограф, массовик затейник, модельер, журналист, ведущий и многие другие. Выбирают данные профессии люди одаренные, которые могут создавать принципиально новые вещи.",
            "img_url": ""
        },{
            'name': "диктор", #4
            "description": "Диктор — это специалист, который занимается чтением информационных, политических, художественных, рекламных материалов у микрофона в эфире и в записи.",
            "img_url": ""
        },{
            'name': "водитель", #5
            "description": "",
            "img_url": ""
        },{
            'name': "спасатель", #6
            "description": "спасатели – люди, всегда готовые прийти на помощь и предотвратить беду.",
            "img_url": ""
        },{
            'name': "ветеринар", #7
            "description": "Ветеринар – это врач, который занимается диагностикой заболеваний у животных и их лечением.",
            "img_url": ""
        },{
            'name': "лингвист", #9
            "description": "Лингвист— это специалист по языкам, языковед. Лингвист изучает языки с разных точек зрения: исторической, сравнительной, структурной, функциональной, социальной, психологической.",
            "img_url": ""
        },{
            'name': "технарь", #10
            "description": "Технарь — это эксперт, умеющий разбираться в устройстве и принципах работы различных технических устройств, а также способный выполнять ремонт и обслуживание этих устройств.",
            "img_url": ""
        },{
            'name': "стилист", #11
            "description": "Стилист — это человек, который занимается созданием образов для клиентов, индивидуального имиджа. Специалист должен подобрать такую одежду, макияж и причёску, которые бы удачно замаскировали недостатки, но выгодно выделили достоинства во внешности.",
            "img_url": ""
        },{
            'name': "модель", #12
            "description": "Модель в мире профессий – это человек, который принимает участие в рекламных съемках, представляя конкретную коллекцию, проект или бренд.",
            "img_url": ""
        },{
            'name': "исследователь", #13
            "description": "Исследователи – это специалисты, занимающиеся изучениями и проводящие эксперименты в той или иной области науки. Благодаря проделанной ими работе люди получают знания в различных спектрах жизни.",
            "img_url": ""
        },{
            'name': "программист", #14
            "description": "",
            "img_url": ""
        },{
            'name': "переводчик", #15
            "description": "Программист — это специалист по созданию и доработке программных продуктов для компьютеров и других устройств, архитектуры различных интернет-ресурсов, компонентов и методов анализа и моделирования.", 
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

        


