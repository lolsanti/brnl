import sqlite3
from flask import Flask, request, session, redirect, url_for, render_template

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Замените на ваш секретный ключ
DATABASE = 'glovo.db'


# Проверка, что пользователь существует и возвращает его данные
def authenticate_user(username, password):
    con = sqlite3.connect(DATABASE)
    cur = con.cursor()
    cur.execute("SELECT * FROM user WHERE username = ? AND password = ?", (username, password))
    user = cur.fetchone()
    con.close()
    return user


# Проверка, что пользователь существует и возвращает его данные
def authenticate_user(username, password):
    con = sqlite3.connect(DATABASE)
    cur = con.cursor()
    cur.execute("SELECT * FROM user WHERE username = ? AND password = ?", (username, password))
    user = cur.fetchone()
    con.close()
    return user


def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d


@app.route('/')
def index():
    return "Главная страница"


@app.route('/admin', methods=['GET', 'PUT', 'DELETE'])
def admin():
    return


@app.route('/admin/dishes', methods=['GET'])
def dishes():
    return


@app.route('/admin/dishes/add', methods=['POST'])
def dishes_add():
    return


@app.route('/admin/dishes/<dish_name>', methods=['GET', 'PUT', 'DELETE'])
def admin_dish_name():
    return


@app.route('/admin/current_orders', methods=['GET'])
def get_current_orders():
    return


@app.route('/admin/current_orders/<order_id>', methods=['GET', 'PUT'])
def order_id():
    return


@app.route('/admin/category_list', methods=['GET', 'POST'])
def category_list():
    return


@app.route('/admin/category_list/<category_name>', methods=['GET', 'DELETE'])
def category_name():
    return


@app.route('/admin/search', methods=['GET/POST'])
def admin_search():
    return


@app.route('/cart', methods=['GET', 'PUT'])
def cart():
    return


@app.route('/cart/order', methods=['POST'])
def cart_order():
    return


@app.route('/cart/add', methods=['POST', 'PUT'])
def cart_add():
    return


@app.route('/user', methods=['GET', 'POST', 'DELETE'])
def user_page():
    if 'current_user' in session:
        current_user = session['current_user']
        user_role = current_user[5]  # Получаем роль пользователя как числовое значение
        print("user_role:", user_role)  # Добавляем отладочный вывод
        return render_template('user.html', current_user=current_user, user_role=user_role)
    else:
        return "Вы не вошли в систему"


@app.route('/user/register', methods=['GET', 'POST'])
def user_register():
    if request.method == 'GET':
        return render_template('register.html')
    elif request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        number = request.form.get('number')
        telegram = request.form.get('telegram')
        role = int(request.form.get('role'))

        # Проверка, что пользователь с таким номером не существует
        con = sqlite3.connect(DATABASE)
        cur = con.cursor()
        cur.execute("SELECT number FROM user WHERE number = ?", (number,))
        existing_number = cur.fetchone()
        con.close()

        if existing_number:
            return "Пользователь с таким номером уже существует. Пожалуйста, выберите другой номер."

        # Проверка, что пользователь с таким именем не существует
        con = sqlite3.connect(DATABASE)
        cur = con.cursor()
        cur.execute("SELECT username FROM user WHERE username = ?", (username,))
        existing_user = cur.fetchone()
        con.close()

        if existing_user:
            return "Имя пользователя уже существует. Пожалуйста, выберите другое имя пользователя."

        # Добавление нового пользователя в базу данных с информацией о Telegram
        con = sqlite3.connect(DATABASE)
        cur = con.cursor()
        cur.execute("INSERT INTO user (username, password, number, role, telegram) VALUES (?, ?, ?, ?, ?)",
                    (username, password, number, telegram, role))
        con.commit()
        con.close()

        return "Регистрация успешна. Теперь вы можете <a href='/user/login'>войти</a>."


@app.route('/user/login', methods=['GET', 'POST'])
def user_login():
    if request.method == 'GET':
        return render_template('login.html')
    elif request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        user = authenticate_user(username, password)

        if user:
            session['current_user'] = user
            user_role = user[5]

            session['user_role'] = user_role
            return redirect(url_for('user_page'))
        else:
            return "Неверное имя пользователя или пароль"


@app.route('/user/logout', methods=['GET'])
def user_logout():
    session.pop('current_user', None)
    return redirect(url_for('user_login'))


@app.route('/user/restore', methods=['POST'])
def user_restore():
    return "User restore password page"


@app.route('/user/orders', methods=['GET'])
def user_orders_history():
    return


@app.route('/user/orders/<order_id>', methods=['GET'])
def user_order(order_id: int):
    return


@app.route('/user/address', methods=['GET', 'POST'])
def user_address_list():
    return


@app.route('/user/address/<address_id>', methods=['GET', 'PUT', 'DELETE'])
def user_address(address_id: int):
    return


@app.route('/menu', methods=['GET', 'POST'])
def view_menu():
    con = sqlite3.connect("glovo.db")
    con.row_factory = dict_factory
    cur = con.cursor()

    cur.execute("SELECT * FROM category")
    category = cur.fetchall()
    cur.execute("SELECT * FROM dishes WHERE available > 0")
    dishes = cur.fetchall()

    con.close()

    current_user = session.get('current_user')  # Получить текущего пользователя из сессии

    return render_template("menu.html", current_user=current_user, category=category, dishes=dishes)


@app.route('/menu/<cat_name>', methods=['GET'])
def menu_cat_name():
    return


@app.route('/menu/<cat_name>/<dish>', methods=['GET'])
def menu_cat_name_dish():
    return redirect(url_for('menu_cat_name'))


@app.route('/menu/<cat_name>/<dish>/review', methods=['POST'])
def menu_review():
    return


@app.route('/menu/search', methods=['GET', 'POST'])
def menu_search():
    return


if __name__ == '__main__':
    app.run(debug=True)
