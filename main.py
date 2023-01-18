from flask import Flask, render_template, request, redirect, url_for, flash
from flask_login import LoginManager, login_user, logout_user, current_user, login_required
from models.auth.auth_forms import RegisterForm, LoginForm, UpdateProfileForm, UpdatePasswordForm
from models.auth.user import User
from models.cust.contactMessage import Message
from models.cust.contactForm import CreateMessageForm
import shelve
import calendar
import time


app = Flask(__name__)
app.config["SECRET_KEY"] = "xxkxcZKH2TxsSw7bew8D9gLpCaa3YYnn"


login_manager = LoginManager()
login_manager.init_app(app)


# start of account management


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
                flash(f'Successfully logged in. Welcome back {user.get_username()}!', 'success')
                login_user(user)
                print(f"User {current_user.get_id()} logged in")
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
        password1 = register_form.password2.data
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
            elif password != password1:
                error = "Passwords do not match"
            else:
                c1 = User(username, email, password, id, 'Customer')
                cust_dict[c1.get_id()] = c1
                db['customer'] = cust_dict
                db.close()
                flash(f'Account successfully created. Welcome {c1.get_username()}')
                print(f"Account created, id = {id}")
                return redirect(url_for('login'))
        except IOError:
            print("Error IO Error")
        except Exception as ex:
            print(f"unknown error occurred as {ex}")
    return render_template('register.html', form=register_form, error=error)


@app.route('/update', methods=['GET', 'POST'])
def update():
    update_password_form = UpdatePasswordForm()
    update_form = UpdateProfileForm()
    submit1 = update_form.submit1.data
    submit2 = update_password_form.submit2.data
    if request.method == "POST" and submit1:
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
                flash('Profile successfully updated')
                print(f"User {current_user.get_id()} profile updated")
    else:
        update_form.username.data = current_user.get_username()
        update_form.email.data = current_user.get_email()
        update_form.location.data = current_user.get_location()
        update_form.phone.data = current_user.get_phone()
        update_form.birthday.data = current_user.get_birthday()

    if request.method == "POST" and submit2:
        password1 = update_password_form.password1.data
        password2 = update_password_form.password2.data
        error = None
        db = shelve.open('DB/Customer/customer')
        user_dict = {}
        user_dict = db['customer']
        for users in user_dict.values():
            if users.get_id() == current_user.get_id():
                if current_user.get_password() == password1:
                    users.set_password(password2)
                else:
                    error = 'Current password is wrong'
        db['customer'] = user_dict
        db.close()
        flash('Password successfully changed!')
        print(f'Password changed from {password1} to {password2}')

    return render_template('update.html', update_form=update_form, update_password_form=update_password_form)


@app.route('/logout', methods=['GET'])
@login_required
def logout():
    print(f"User {current_user.get_id()} logged out")
    logout_user()
    return redirect(url_for('home'))


@app.route('/delete', methods=['GET'])
@login_required
def delete():
    try:
        db = shelve.open('DB/Customer/customer')
        user_dict = {}
        user_dict = db['customer']
        if 'customer' in db:
            user_dict = db['customer']
        else:
            db['customer'] = user_dict
        print(f"User {current_user.get_id()} account deleted")
        user_dict.pop(current_user.get_id(), None)
        logout()

        db['customer'] = user_dict
        db.close()
    except IOError:
        print("Error IO Error")
    except Exception as ex:
        print(f"unknown error occurred as {ex}")

    return render_template('home.html')


def createStaff():
    username = input("Enter name: ")
    email = input("Enter email: ")
    password = "AdminPassword123"
    current_GMT = time.gmtime()
    id = int(calendar.timegm(current_GMT))
    role = "Admin"
    cust_dict = {}
    try:
        db = shelve.open('DB/Customer/customer')
        if 'customer' in db:
            cust_dict = db['customer']
        else:
            db['customer'] = cust_dict

        Admin = User(username, email, password, id, role)
        cust_dict[Admin.get_id()] = Admin
        db['customer'] = cust_dict
        db.close()

    except IOError:
        print("Error IO Error")
    except Exception as ex:
        print(f"unknown error occurred as {ex}")

# end of account management
# start customer support


@app.route('/contactUs', methods=['GET', 'POST'])
def contactUs():
    create_message_form = CreateMessageForm()
    if request.method == "POST":
        name = create_message_form.name.data
        email = create_message_form.email.data
        subject = create_message_form.subject.data
        message = create_message_form.message.data
        message_dict = {}
        try:
            db = shelve.open('DB/Message/message')
            if 'message' in db:
                message_dict = db['message']
            else:
                db['message'] = message_dict

            message = Message(name, email, subject, message)
            message_dict[message.get_message_id()] = message
            db['message'] = message_dict
            db.close()
            flash('Message sent successfully')
        except IOError:
            print("Error IO Error")
        except Exception as ex:
            print(f"unknown error occurred as {ex}")

    return render_template('contactUs.html', form=create_message_form)


@app.route('/retrieveMessages', methods=["GET", "POST"])
def retrieveMessages():
    message_dict = {}
    db = shelve.open('DB/Message/message', 'r')
    message_dict = db['message']
    db.close()

    message_list = []
    for key in message_dict:
        user = message_dict.get(key)
        message_list.append(user)

    return render_template('retrieveMessages.html', count=len(message_list), message_list=message_list)


@app.route('/deleteMessage/<int:id>', methods=['POST'])
def delete_message(id):
    message_dict = {}
    db = shelve.open('DB/Message/message', 'w')
    message_dict = db['message']

    message_dict.pop(id)

    db['message'] = message_dict
    db.close()

    return redirect(url_for('retrieveMessages'))


# end customer support
# start of hiring

# end of hiring

if __name__ == '__main__':
    app.run(debug=True)
