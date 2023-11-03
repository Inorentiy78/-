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
            "img_url": "https://cs8.pikabu.ru/post_img/big/2017/12/24/10/1514136864154767020.jpg"
        },{
            'name': "художник", #3
            "description": "К творческим профессиям можно отнести такие, как музыкант, художник, скульптор, режиссер, актер, писатель, фотограф, массовик затейник, модельер, журналист, ведущий и многие другие. Выбирают данные профессии люди одаренные, которые могут создавать принципиально новые вещи.",
            "img_url": "https://avatars.mds.yandex.net/get-pdb/1807426/b395f05b-fa0b-4550-bfd6-8b23c60338e5/s1200"
        },{
            'name': "диктор", #4
            "description": "Диктор — это специалист, который занимается чтением информационных, политических, художественных, рекламных материалов у микрофона в эфире и в записи.",
            "img_url": "https://mykaleidoscope.ru/x/uploads/posts/2022-09/1663218890_36-mykaleidoscope-ru-p-uspeshnii-televedushchii-vkontakte-39.jpg"
        },{
            'name': "спасатель", #5
            "description": "спасатели – люди, всегда готовые прийти на помощь и предотвратить беду.",
            "img_url": "https://i.pinimg.com/originals/2e/b8/a7/2eb8a723f3229030be47cf78d69ce3d7.jpg"
        },{
            'name': "ветеринар", #6
            "description": "Ветеринар – это врач, который занимается диагностикой заболеваний у животных и их лечением.",
            "img_url": "https://bigpicture.ru/wp-content/uploads/2016/02/vets05.jpg"
        },{
            'name': "лингвист", #7
            "description": "Лингвист— это специалист по языкам, языковед. Лингвист изучает языки с разных точек зрения: исторической, сравнительной, структурной, функциональной, социальной, психологической.",
            "img_url": "https://razoom.mgutm.ru/pluginfile.php/82746/course/overviewfiles/f56b51c7783b1c61c969d.jpg"
        },{
            'name': "технарь", #8
            "description": "Технарь — это эксперт, умеющий разбираться в устройстве и принципах работы различных технических устройств, а также способный выполнять ремонт и обслуживание этих устройств.",
            "img_url": "https://thesun.co.uk/wp-content/uploads/2018/05/nintchdbpict000404900112-e1525967553327.jpg"
        },{
            'name': "стилист", #9
            "description": "Стилист — это человек, который занимается созданием образов для клиентов, индивидуального имиджа. Специалист должен подобрать такую одежду, макияж и причёску, которые бы удачно замаскировали недостатки, но выгодно выделили достоинства во внешности.",
            "img_url": "https://nypost.com/wp-content/uploads/sites/2/2021/12/Sugar-baby-feature.jpg"
        },{
            'name': "модель", #10
            "description": "Модель в мире профессий – это человек, который принимает участие в рекламных съемках, представляя конкретную коллекцию, проект или бренд.",
            "img_url": "https://rsute.ru/wp-content/uploads/2021/01/5-3.jpg"
        },{
            'name': "исследователь", #11
            "description": "Исследователи – это специалисты, занимающиеся изучениями и проводящие эксперименты в той или иной области науки. Благодаря проделанной ими работе люди получают знания в различных спектрах жизни.",
            "img_url": "https://kartinkof.club/uploads/posts/2023-05/1683457216_kartinkof-club-p-nauchnie-kartinki-2.jpg"
        },{
            'name': "программист", #12
            "description": "Программист — это специалист по созданию и доработке программных продуктов для компьютеров и других устройств, архитектуры различных интернет-ресурсов, компонентов и методов анализа и моделирования.",
            "img_url": "https://images.ctfassets.net/yewqr8zk7e5s/migrated-3291/e9d28d4ca1c66b5341907db545091c82/shutterstock_574105045-2.jpg"
        },{
            'name': "спортивный тренер", #13
            "description": "Тренер — специалист в определённом виде спорта, руководящий тренировкой спортсменов.",
            "img_url": "https://hosbeg.com/wp-content/uploads/2021/03/bd49f3ce0bf65a3d1df78a1263363dd1.jpg"
        },{
            'name': "адвокат", #14
            "description": "Лицо, профессией которого является оказание квалифицированной юридической помощи физическим лицам и юридическим лицам, в том числе защита их прав и представление интересов в суде, обладающее полученным в установленном порядке статусом адвоката.",
            "img_url": "https://fikiwiki.com/uploads/posts/2022-02/1644915088_40-fikiwiki-com-p-kartinki-advokata-43.jpg"
        },{
            'name': "бухгалтер", #15
            "description": "Бухгалтер — специалист по бухгалтерскому учёту, работающий по системе учёта в соответствии с действующим законодательством.", 
            "img_url": "https://frankfurt.apollo.olxcdn.com/v1/files/km81tzti85oe1-KZ/image;s=644x461"
        },{
            'name': "военный", #16
            "description": "Военный — это человек, который профессионально занят в военной сфере и служит в вооруженных силах своей страны. Военные выполняют различные задачи, связанные с обеспечением безопасности и защитой государства. Военные несут военную службу в армии в соответствии со своей специальностью: пограничник, десантник, связист, сапер, военные инженеры, строитель и т. д. Они должны уметь чётко и грамотно выполнять приказы, соблюдать субординацию, обращаться с оружием.",
            "img_url": "https://i.pinimg.com/originals/9d/17/c5/9d17c5193b01521d0b4aa3a500ff4669.jpg"
        },{
            'name': "роботехник", #17
            "description": "Робототехника -Это собирательная профессия, в которой есть много специализаций: конструктор, сборщик роботов, программист, электронщик, тестировщик, интегратор и прочее",
            "img_url": "https://topobrazovanie.ru/wp-content/uploads/2019/03/100929016-175074220.jpg"
        },{
            'name': "косметолог", #18
            "description": "Косметолог – это специалист, который оказывает услуги по уходу за кожей человека и устранению ее эстетических недостатков. В его обязанности входит проведение различных аппаратных процедур, пилингов, чисток, массажа, инъекций и других действий, направленных на улучшение состояния или лечение кожи клиента.",
            "img_url": "https://socialcafe.ru/wp-content/uploads/2022/07/1-1-1536x1152.jpg"
        },{
            'name': "маркетолог", #19
            "description": "Маркетолог — это специалист, который занимается продвижением товаров и услуг на рынке.",
            "img_url": "https://donklephant.net/wp-content/uploads/2021/05/e8ov1m0x9cs.jpg"
        },{
            'name': "дизайнер", #20
            "description": "Быть дизайнером — значит планировать, проектировать, разрабатывать и создавать графический контент. Если речь идет о веб-дизайне, такой специалист должен разбираться в тонкостях интерфейса, чтобы делать его удобным и понятным для пользователя.",
            "img_url": "https://sumnikoff.ru/wp-content/uploads/2022/07/unnamed-file.jpg"
        },{
            'name': "повар", #21
            "description": "Повар - это человек, который занимается приготовлением пищи в заведениях общественного питания.",
            "img_url": "https://kg-portal.ru/img/73665/main_2x.jpg"
        },{
            'name': "хареограф", #22
            "description": "Хореограф -это специалист, который преподает танцевальное искусство, придумывает хореографию для мероприятий и отрабатывает ее вместе с танцорами. Как правило, хореографом могут стать танцоры, артисты балета, гимнасты, фигуристы, которые имеют большой опыт за плечами и могут многому научить.",
            "img_url": "https://i.pinimg.com/originals/53/26/30/53263005f9914ac9bb3c2c54ea63a69a.jpg"
        },{
            'name': "парикмахер", #23
            "description": "Парикмахер делает разные виды стрижек, окраску, химическую завивку и укладку, занимается лечением волос, наращиванием, ламинированием, корректирует форму прически, а также усов и бороды у мужчин, плетет косы, дреды и другие замысловатые прически.",
            "img_url": "https://uhd.name/uploads/posts/2022-09/1662782315_25-uhd-name-p-zhenskii-parikmakher-devushka-krasivo-28.jpg"
        },{
            'name': "экскурсовод", #24
            "description": "Экскурсовод – это специалист, который проводит экскурсии и делится знаниями о различных местах, культуре, истории и достопримечательностях.", 
            "img_url": "https://meets.com/blog/wp-content/uploads/2016/10/jobs-travel-2.jpg"
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

        


