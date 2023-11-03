from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
#from server import app # комментировать при запуске server.py эту строку
db = SQLAlchemy()  # когда запускаете server.py уберите из скобок app
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
            "description": "Руководитель - это лицо или индивид, который организует и координирует деятельность группы людей, команды или организации, чтобы достичь определенных целей и результатов. Руководитель может занимать разные позиции и выполнять разные функции в зависимости от контекста и организации. ",
            "img_url": "https://avatars.mds.yandex.net/i?id=1a2e3edae618fe2f6926779bc69d3be067ced067-10843930-images-thumbs&n=13"
        },{
            'name': "преподаватель", #2 
            "description": "Преподаватель - это человек, который занимается преподаванием, то есть обучением других людей в учебных учреждениях, таких как школы, колледжи, университеты или другие образовательные организации. ",
            "img_url": "https://avatars.mds.yandex.net/i?id=edde3f66677a677c610ff601961fbd3c9af7e3fa-10636720-images-thumbs&n=13"
        },{
            'name': "художник", #3
            "description": "Художник - это человек, который создает изобразительные произведения искусства, такие как живопись, графика, скульптура, фотография, иллюстрации, а также другие виды изобразительного искусства.",
            "img_url": "https://avatars.mds.yandex.net/i?id=b078778b604e99ed68647565dd3b503fa8c78ddf-9049934-images-thumbs&n=13"
        },{
            'name': "диктор", #4
            "description": "Диктор - это профессионал, чья работа связана с озвучиванием текстов, информационных сообщений и других аудио- или видеоматериалов. Дикторы могут работать в различных областях, включая радио, телевидение, кино, интернет-проекты, рекламу и многие другие сферы.",
            "img_url": "https://avatars.mds.yandex.net/i?id=4a12f83060518a533822a47f0546c5818ff01e2e-10701951-images-thumbs&n=13"
        },{
            'name': "водитель", #5
            "description": "Водитель - это человек, который управляет транспортным средством, таким как автомобиль, грузовик, автобус, мотоцикл, поезд, корабль или самолет. Работа водителя требует умения управлять транспортным средством, соблюдать правила дорожного движения и обеспечивать безопасность как для себя, так и для пассажиров и других участников дорожного движения.",
            "img_url": "https://avatars.mds.yandex.net/i?id=86c4a3ab370cce36c1a15c9b49f70214143500ec-10851145-images-thumbs&n=13"
        },{
            'name': "спасатель", #6
            "description": "Спасатель - это человек, который специализируется на предоставлении помощи и спасении людей в экстренных ситуациях, таких как природные катастрофы, аварии, бедствия на воде или водоемах, а также других чрезвычайных ситуациях.",
            "img_url": "https://avatars.mds.yandex.net/i?id=ba159c4ec5d5f3977dcc3e7b539c368cf350abb7-8895061-images-thumbs&n=13"
        },{
            'name': "ветеринар", #7
            "description": "Ветеринар - это профессионал, который занимается медицинским уходом и лечением животных. ",
            "img_url": "https://avatars.mds.yandex.net/i?id=d2e9fab39bda233dae4140f19d21965a350e1cc3-9265564-images-thumbs&n=13"
        },{
            'name': "путешественник", #8
            "description": "Путешественник - это человек, который любит путешествовать и исследовать разные места, культуры и природные достопримечательности. ",
            "img_url": "https://avatars.mds.yandex.net/i?id=45a5f482d67ba587ce8610d84df4f6d6ed871be5-10578163-images-thumbs&n=13"
        },{
            'name': "лингвист", #9
            "description": "Лингвист - это специалист, который занимается изучением языков и их структуры, а также исследует языковые процессы, коммуникацию, историю и эволюцию языков. ",
            "img_url": "https://avatars.mds.yandex.net/i?id=167d234eb38362cc92b7cdf0c4aa8b1ecc47d218-10142557-images-thumbs&n=13"
        },{
            'name': "технарь", #10
            "description": "",
            "img_url": "https://avatars.mds.yandex.net/i?id=c38432909fae211f367f8eb4b2e0b3bed1ffd7b4-10176094-images-thumbs&n=13"
        },{
            'name': "стилист", #11
            "description": "Стилист - это специалист, который занимается созданием образов и стилей в одежде, визаже (макияже) и прическе, чтобы помочь клиентам выглядеть более привлекательно и ухоженно.",
            "img_url": "https://avatars.mds.yandex.net/i?id=d87b022ebe15f53ea1f6be38c0ace52e499191e3-9847625-images-thumbs&n=13"
        },{
            'name': "модель", #12
            "description": "Модель в контексте моды и развлекательной индустрии - это человек, который используется для демонстрации одежды, аксессуаров, косметики или других товаров, как на подиуме, так и в фотографических съемках. ",
            "img_url": "https://avatars.mds.yandex.net/i?id=be32ba9e2700a01de06e519b063a858349b2da20-9066051-images-thumbs&n=13"
        },{
            'name': "исследователь", #13
            "description": "Модель в контексте моды и развлекательной индустрии - это человек, который используется для демонстрации одежды, аксессуаров, косметики или других товаров, как на подиуме, так и в фотографических съемках. ",
            "img_url": "https://avatars.mds.yandex.net/i?id=ca642792cde115825c88aaef0f668439cb60345e-10618387-images-thumbs&n=13"
        },{
            'name': "программист", #14
            "description": "Программист - это специалист, который занимается созданием, разработкой и поддержкой программного обеспечения, включая приложения, веб-сайты, компьютерные игры и другие программы. ",
            "img_url": "https://avatars.mds.yandex.net/i?id=541927dd8b0f35f1a0623229792ce74d24f3ec78-10868764-images-thumbs&n=13"
        },{
            'name': "переводчик", #15
            "description": "Переводчик - это специалист, который занимается переводом текстов, устных высказываний или диалогов с одного языка на другой.", 
            "img_url": "https://avatars.mds.yandex.net/i?id=90fad9a56e1b0a7dd2e1d2f536c99bfa6f21a117-10340180-images-thumbs&n=13"
        },{
            'name': "спортивный тренер", #16
            "description": "Спортивный тренер - это профессионал, который занимается обучением и тренировкой спортсменов, помогая им развивать навыки и достигать лучших результатов в своей спортивной дисциплине. Работа спортивного тренера может включать в себя различные аспекты, в зависимости от конкретного вида спорта и уровня спортсменов, с которыми они работают.",
            "img_url": "https://avatars.mds.yandex.net/i?id=7874515c5586024e7e3762754f5401346efaea25-10715741-images-thumbs&n=13"
        },{
            'name': "адвокат", #17
            "description": "Адвокат - это лицензированный юрист, специализирующийся на представлении интересов клиентов в суде и вне судебных процессов. Главная задача адвоката - предоставлять юридическую консультацию, защищать права и интересы своих клиентов и представлять их в суде, если это необходимо.",
            "img_url": "https://avatars.mds.yandex.net/i?id=76b241ac21072ec1b291bcb1d84297145466b402-4883843-images-thumbs&n=13"
        },{
            'name': "бухгалтер", #18
            "description": "Бухгалтер - это профессионал, который занимается ведением бухгалтерского учета и финансовой отчетности в организации или предприятии. Работа бухгалтера включает в себя регистрацию, классификацию и анализ финансовых данных, чтобы обеспечить точное отражение финансовой деятельности компании.", 
            "img_url": "https://avatars.mds.yandex.net/i?id=37586ec6c0bbf5dbd99b78908250989a468dadef-10384987-images-thumbs&n=13"
        },{
            'name': "военный", #19
            "description": "Военный - это человек, который служит в вооруженных силах своей страны и обязан выполнять военные обязанности в интересах национальной обороны и безопасности. Вооруженные силы могут включать армию, военно-воздушные силы, флот и другие военные компоненты, в зависимости от структуры и организации страны.",
            "img_url": "https://avatars.mds.yandex.net/i?id=ac4300461b75bb9c9af2b01d6ecba1323b79ac20-9137656-images-thumbs&n=13"
        },{
            'name': "робототехник", #20
            "description": "Робототехник - это специалист, который занимается созданием, программированием и обслуживанием роботов. Робототехники работают в области робототехники, которая включает в себя разработку и использование автономных и управляемых механических устройств, известных как роботы, для выполнения различных задач.",
            "img_url": "https://avatars.mds.yandex.net/i?id=16899d52538a92bd4d789bd3f358de210670c5e4-9839669-images-thumbs&n=13"
        },{
            'name': "косметолог", #21
            "description": "Косметолог - это специалист, который занимается уходом за кожей и внешней красотой пациентов, а также проводит различные процедуры и лечение для улучшения состояния кожи, волос и ногтей. Работа косметолога включает в себя разнообразные аспекты ухода за внешностью и косметическими процедурами.",
            "img_url": "https://avatars.mds.yandex.net/i?id=12fb4df37aa04687faa126c7eb67e2e0b392d903-9863167-images-thumbs&n=13"
        },{
            'name': "маркетолог", #22
            "description": "Маркетолог - это специалист в области маркетинга, который занимается разработкой и реализацией маркетинговых стратегий и планов для продвижения товаров, услуг или бренда на рынке. Работа маркетолога направлена на привлечение клиентов, увеличение продаж и повышение узнаваемости бренда.",
            "img_url": "https://avatars.mds.yandex.net/i?id=4016fb89f4ed0e7ea58a2ee992c48fa053cd02bd-4872419-images-thumbs&n=13"
        },{
            'name': "дизайнер", #23
            "description": "Дизайнер - это творческий специалист, который занимается проектированием и созданием визуальных решений, чтобы обеспечить эффективную и привлекательную форму для различных продуктов, услуг, веб-сайтов, графических материалов и других объектов. Работа дизайнера требует художественных навыков, внимания к деталям и способности коммуницировать через визуальные средства.",
            "img_url": "https://avatars.mds.yandex.net/i?id=07b63d4bef128ac69a0751bf46a24e7060fa042b-10934180-images-thumbs&n=13"
        },{
            'name': "повар", #24
            "description": "Повар - это профессионал, специализирующийся на приготовлении блюд и кулинарных изысков. Работа повара включает в себя приготовление различных блюд, начиная от простых и повседневных, заканчивая изысканными гастрономическими шедеврами. Повары работают в различных местах, включая рестораны, кафе, гостиницы, кейтеринговые компании и другие заведения общественного питания.",
            "img_url": "https://avatars.mds.yandex.net/i?id=37d8ad0147a2a875d1fc09a429d777a79addd05c-10272338-images-thumbs&n=13"
        },{
            'name': "хареограф", #25
            "description": "Хореограф - это профессионал, занимающийся созданием хореографии и режиссурой танцевальных выступлений. Хореографы разрабатывают танцевальные композиции, учат танцоров движениям и ритмам, а также руководят репетициями для подготовки танцевальных номеров, которые могут быть частью театральных представлений, музыкальных клипов, фильмов, мероприятий и других шоу.",
            "img_url": "https://avatars.mds.yandex.net/i?id=5fd8400ad54818e8ec745f237c8713257ea0ca73-10954464-images-thumbs&n=13"
        },{
            'name': "парикмахер", #26
            "description": "Парикмахер - это специалист, который работает в индустрии красоты и занимается уходом за волосами клиентов. Работа парикмахера включает в себя стрижку, окрашивание, укладку и уход за волосами, а также консультации клиентов по уходу за волосами и стайлингу",
            "img_url": "https://avatars.mds.yandex.net/i?id=e3549a2a16160be1b871b9a4a35d74bcf3f0c516-10893744-images-thumbs&n=13"
        },{
            'name': "экскурсовод", #27
            "description": "Экскурсовод - это специалист, который проводит экскурсии и рассказывает туристам и посетителям о различных исторических, культурных, природных и других интересных местах. Работа экскурсовода включает в себя рассказ о достопримечательностях, истории и культуре места, а также организацию и проведение экскурсий.", 
            "img_url": "https://avatars.mds.yandex.net/i?id=108d806eccf19873ff01db9a73de89c839d507d3-10148236-images-thumbs&n=13"
        },
        ]

        for profession in professions:
            new_prof = Profession(name=profession['name'],description=profession['description'], img_url=profession['img_url'])
            db.session.add(new_prof)
            db.session.commit()

        partners = [{
            "name": "Казииту", #1
            "link_url" : "https://digitalcollege.kz/",
            "logo_img" : "",
            "description" :""
        },{
            "name": "РВТК", #2
            "link_url" : "https://rvtk.edu.kz/",
            "logo_img" : "https://rvtk.edu.kz/images/content/logo.png%20-%20-400.png#joomlaImage://local-images/content/logo.png%20-%20-400.png?width=150&height=150",
            "description" :"Республиканский высший техничческий колледж"
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

        


