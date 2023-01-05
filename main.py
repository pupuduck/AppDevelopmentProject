from flask import Flask, render_template, request, redirect, url_for
from flask_login import LoginManager, login_user, logout_user, login_required
from models.auth.auth_forms import RegisterForm, LoginForm
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
    for object in user_dict.values():
        if object.get_id() == user_id:
            return object


@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html')


@app.route('/login', methods=["GET", "POST"])
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
        for user in user_dict.values():
            if user.get_username() == username:
                login_user(user)
                return redirect(url_for('home'))
            else:
                error = 'test'

    return render_template('login.html', form=login_form, error=error)


@app.route('/register', methods=['GET', 'POST'])
def register():
    register_form = RegisterForm()
    error = None
    if request.method == "POST":
        username = register_form.username.data
        email = register_form.email.data
        password = register_form.email.data
        current_gmt = time.gmtime()
        id = calendar.timegm(current_gmt)
        cust_dict = {}
        try:
            db = shelve.open('DB/Customer/customer')
            if 'customer' in db:
                cust_dict = db['customer']
            else:
                db['customer'] = cust_dict
            username_list = []
            email_list = []
            for objects in cust_dict.values():
                username_list.append(objects.get_username())
                email_list.append(objects.get_email())
            if username in username_list and email in email_list:
                error = "Both username and email are already taken"
            elif email in email_list:
                error = "Email is already taken"
            elif username in username_list:
                error = "Username is already taken"
            else:
                user = User(username, email, password, id)
                cust_dict[user.get_id()] = user
                db['customer'] = cust_dict
                db.close()
                return redirect(url_for('home'))
        except IOError:
            print("IO Error")
        except Exception as ex:
            print(f"Unknown error occured as {ex}")
    return render_template('register.html', form=register_form, error=error)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return render_template('home.html')


@app.route('/products')
def products():
    return render_template('products.html')


if __name__ == '__main__':
    app.run(debug=True)