from flask import Flask, render_template, request, redirect, url_for
from flask_login import LoginManager, login_user, logout_user, current_user, login_required
from models.auth.auth_forms import RegisterForm, LoginForm, UpdateProfileForm
from models.auth.user import User
import shelve
import calendar
import time


app = Flask(__name__)
app.config["SECRET_KEY"] = "xxkxcZKH2TxsSw7bew8D9gLpCaa3YYnn"


login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    db = shelve.open('DB/Customer/customer')
    user_dict = {}
    user_dict = db['customer']
    db.close()
    for objects in user_dict.values():
        if objects.get_id() == user_id:
            return objects


@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html')


@app.route('/products')
def products():
    return render_template('products.html')


@app.route('/login', methods=['POST', 'GET'])
def login():
    login_form = LoginForm()
    error = None
    if request.method == "POST":
        username = login_form.username.data
        password = login_form.password.data
        db = shelve.open('DB/Customer/customer')
        user_dict = {}
        user_dict = db['customer']
        db.close()
        user_list = []
        for user in user_dict.values():
            if username == user.get_username():
                user_list.append(user)
            else:
                error = "Username does not exist"
        for user in user_list:
            if user.get_password() != password:
                error = 'Password is incorrect'
            else:
                login_user(user)
                return redirect(url_for('home'))

    return render_template('login.html', form=login_form, error=error)


@app.route('/register', methods=['POST', 'GET'])
def register():
    register_form = RegisterForm()
    error = None
    if request.method == "POST":
        username = register_form.username.data
        email = register_form.email.data
        password = register_form.password1.data
        current_GMT = time.gmtime()
        id = int(calendar.timegm(current_GMT))
        cust_dict = {}
        try:
            db = shelve.open('DB/Customer/customer')
            if 'customer' in db:
                cust_dict = db['customer']
            else:
                db['customer'] = cust_dict
            object_list = []

            for objects in cust_dict.values():
                object_list.append(objects.get_email())
            if username in cust_dict and email in object_list:
                error = "Both username and email are already taken"
            elif email in object_list:
                error = "Email is already taken"
            elif username in cust_dict:
                error = "Username is already taken"
            else:
                c1 = User(username, email, password, id)
                cust_dict[c1.get_id()] = c1
                db['customer'] = cust_dict
                db.close()
                return redirect(url_for('login'))
        except IOError:
            print("Error IO Error")
        except Exception as ex:
            print(f"unknown error occurred as {ex}")
    return render_template('register.html', form=register_form, error=error)


@app.route('/update', methods=['GET', 'POST'])
def update():
    update_form = UpdateProfileForm()
    if request.method == "POST":
        db = shelve.open('DB/Customer/customer')
        user_dict = {}
        user_dict = db['customer']
        for users in user_dict.values():
            if users.get_id() == current_user.get_id():
                users.set_username(update_form.username.data)
                users.set_email(update_form.email.data)
                users.set_location(update_form.location.data)
                users.set_phone(update_form.phone.data)
                users.set_birthday(update_form.birthday.data)
                db['customer'] = user_dict
                db.close()
            else:
                print('error')
    else:
        update_form.username.data = current_user.get_username()
        update_form.email.data = current_user.get_email()
        update_form.location.data = current_user.get_location()
        update_form.phone.data = current_user.get_phone()
        update_form.birthday.data = current_user.get_birthday()

    return render_template('update.html', form=update_form)


@app.route('/logout', methods=['GET'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))


@app.route('/delete', methods=['GET'])
def delete():
    try:
        db = shelve.open('DB/Customer/customer')
        user_dict = {}
        user_dict = db['customer']
        if 'customer' in db:
            user_dict = db['customer']
        else:
            db['customer'] = user_dict
        user_dict.pop(current_user.get_id(), None)
        logout()

        db['customer'] = user_dict
        db.close()
    except IOError:
        print("Error IO Error")
    except Exception as ex:
        print(f"unknown error occurred as {ex}")

    return render_template('home.html')


if __name__ == '__main__':
    app.run(debug=True)
