from flask import Flask, render_template, request, jsonify, session, redirect, url_for
from models import db, bc,  User

app = Flask(__name__)
app.secret_key = "Mysecret"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

@app.route('/')
def index():
    if 'user' in session:
        user = session.get('user')
        print(user)
        lang='ru'
        return render_template('index.html', lang=lang, user=user)
    else:
        user = ""
        lang='ru'
        return render_template('index.html', lang=lang, user=user)


@app.route('/login', methods=['POST'])
def logining():
    username = request.form["username"]
    password = request.form["password"]
    print(username, password)
    user = db.session.query(User).filter(User.username==username).first()
    if not user:
        return jsonify({'msg': 'Не правильный логин или пароль'}), 404
    if user.check_pass(password):
        session['user'] = user.to_json
        return redirect(url_for('index'))
    return jsonify({'msg': 'Не правильный логин или пароль'}), 404
    
    

@app.route('/register', methods=["POST"])
def adduser():
    username = request.form["username"]
    password = request.form["password"]
    email = request.form["email"]
    phone = request.form["phone"]
    lastname = request.form["lastname"]
    name = request.form["name"]
    surname = request.form["surname"]
    user = User.query.filter(username=username).first()
    if user:
        return jsonify({'msg': 'Такой пользователь уже есть'}), 404
    new_user = User(username=username, password=password, email=email, phone=phone, 
                    lastname=lastname, name=name, surname=surname)
    with app.app_context():
        db.session.add(new_user)
        db.session.commit()
    return redirect(url_for('index'))

@app.route('/logout', methods=["GET"])
def logout():
    session.pop('user', None)
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True)
