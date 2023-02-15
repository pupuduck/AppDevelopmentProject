from flask import render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_user, logout_user, current_user, login_required
from flask_mail import Message
from models.auth.auth_forms import RegisterForm, LoginForm, UpdateProfileForm, UpdatePasswordForm, CreditCardForm, ResetPasswordForm, RequestResetForm
from models.auth.user import User
from models.auth.paymentMethods import paymentMethods
from models.cust.contactMessage import Messages
from models.cust.contactForm import CreateMessageForm
from models.hiring.hiringForm import CreateResumesForm, CreateJobPositionsForm
from models.hiring.resume import Resumes
from models.hiring.jobPositions import JobPositions
from models.products.productForm import CreateProductForm, AddToCart
from models.products.product import Product
from models.cust.chat import get_response
from models.products.cart import cartItems
from models.auth.transaction_history import transactionHistory
from models.report.report import Report
from models.report.reportForm import CreateReportForm
from PIL import Image
from config import *
import secrets
import shelve
import calendar
import time
from datetime import datetime


# app = Flask(__name__)
# app.config["SECRET_KEY"] = "xxkxcZKH2TxsSw7bew8D9gLpCaa3YYnn"
#
# app.config['MAIL_SERVER'] = 'smtp.googlemail.com'
# app.config['MAIL_PORT'] = '587'
# app.config['MAIL_USE_TLS'] = True
# app.config['MAIL_USERNAME'] = "DoctorDonutServices"
# app.config['MAIL_PASSWORD'] = "DoctorDonut1447!"
# mail = Mail(app)
#
# login_manager = LoginManager()
# login_manager.init_app(app)


# start of account management


@login_manager.user_loader
def load_user(user_id):
    user_dict = {}
    try:
        db = shelve.open('DB/Customer/customer')
        if 'customer' in db:
            user_dict = db['customer']
        else:
            db['customer'] = user_dict
        user_dict = db['customer']
        db.close()
    except IOError:
        print("Error IO Error")
    except Exception as ex:
        print(f"unknown error occurred as {ex}")
    for objects in user_dict.values():
        if objects.get_id() == user_id:
            return objects


@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html')


@app.route('/aboutus')
def aboutus():
    return render_template('aboutus.html')


@app.route('/login', methods=['POST', 'GET'])
def login():
    login_form = LoginForm()
    error = None
    user_dict = {}
    if request.method == "POST":
        try:
            db = shelve.open('DB/Customer/customer')
            username = login_form.username.data
            password = login_form.password.data
            if 'customer' in db:
                user_dict = db['customer']
            else:
                db['customer'] = user_dict

            user_list = []
            for user in user_dict.values():
                if username == user.get_username() and user.get_status() == 'Active':
                    user_list.append(user)
                else:
                    error = "Username does not exist"
            for user in user_list:
                if user.get_password() != password:
                    error = 'Password is incorrect'
                else:
                    flash(f'Successfully logged in. Welcome back {user.get_username()}!', category='alert-success')
                    login_user(user)
                    print(f"User {current_user.get_id()} logged in")
                    return redirect(url_for('home'))
            db.close()
        except IOError:
            print("Error IO Error")
        except Exception as ex:
            print(f"unknown error occurred as {ex}")

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

        cust_dict = {}
        try:
            db = shelve.open('DB/Customer/customer')
            if 'customer' in db:
                cust_dict = db['customer']
            else:
                db['customer'] = cust_dict
            email_list = []
            username_list = []
            for objects in cust_dict.values():
                email_list.append(objects.get_email())
                username_list.append(objects.get_username())
            if username in username_list and email in email_list:
                error = "Both username and email are already taken"
            elif email in email_list:
                error = "Email is already taken"
            elif username in username_list:
                error = "Username is already taken"
            elif password != password1:
                error = "Passwords do not match"
            else:
                current_GMT = time.gmtime()
                user_id = int(calendar.timegm(current_GMT))
                c1 = User(username, email, password, user_id, 'Customer', 'Active')
                cust_dict[c1.get_id()] = c1
                db['customer'] = cust_dict
                db.close()
                flash(f'Account successfully created. Welcome {c1.get_username()}', category='alert-success')
                print(f"Account created, id = {user_id}")
                return redirect(url_for('login'))
        except IOError:
            print("Error IO Error")
        except Exception as ex:
            print(f"unknown error occurred as {ex}")
    return render_template('register.html', form=register_form, error=error)


@app.route('/createAdmin', methods=['POST', 'GET'])
def create_staff():
    register_form = RegisterForm()
    error = None
    if request.method == "POST":
        username = register_form.username.data
        email = register_form.email.data
        password = register_form.password1.data
        password1 = register_form.password2.data

        cust_dict = {}
        try:
            db = shelve.open('DB/Customer/customer')
            if 'customer' in db:
                cust_dict = db['customer']
            else:
                db['customer'] = cust_dict
            email_list = []
            username_list = []
            for objects in cust_dict.values():
                email_list.append(objects.get_email())
                username_list.append(objects.get_username())
            if username in username_list and email in email_list:
                error = "Both username and email are already taken"
            elif email in email_list:
                error = "Email is already taken"
            elif username in username_list:
                error = "Username is already taken"
            elif password != password1:
                error = "Passwords do not match"
            else:
                current_GMT = time.gmtime()
                user_id = int(calendar.timegm(current_GMT))
                c1 = User(username, email, password, user_id, 'Admin', 'Active')
                cust_dict[c1.get_id()] = c1
                db['customer'] = cust_dict
                db.close()
                flash(f'Admin account successfully created.', category='alert-success')
                print(f"Account created, id = {user_id}")
                return redirect(url_for('retrieve_users'))
        except IOError:
            print("Error IO Error")
        except Exception as ex:
            print(f"unknown error occurred as {ex}")
    return render_template('createStaff.html', form=register_form, error=error)


@app.route('/update', methods=['GET', 'POST'])
def update():
    update_password_form = UpdatePasswordForm()
    update_form = UpdateProfileForm()
    submit1 = update_form.submit1.data
    submit2 = update_password_form.submit2.data
    error = None
    error2 = None
    if request.method == "POST" and submit1:
        user_dict = {}
        try:
            db = shelve.open('DB/Customer/customer')
            if 'customer' in db:
                user_dict = db['customer']
            else:
                db['customer'] = user_dict
            name_list = []
            email_list = []
            user = []
            for users in user_dict.values():
                name_list.append(users.get_username())
                email_list.append(users.get_email())
                if users.get_id() == current_user.get_id():
                    user.append(users)
            for users in user:
                if update_form.username.data in name_list and update_form.username.data != current_user.get_username():
                    error = "Username is already taken"
                if update_form.email.data in email_list and update_form.email.data != current_user.get_email():
                    error2 = "Email is already taken"
                if not error and not error2:
                    users.set_email(update_form.email.data)
                    users.set_username(update_form.username.data)
                    users.set_location(update_form.location.data)
                    users.set_phone(update_form.phone.data)
                    users.set_birthday(update_form.birthday.data)
                    if update_form.image.data:
                        image = Image.open(update_form.image.data)
                        random_hex = secrets.token_hex(8)
                        random_hex = "static/profileImage/" + random_hex + ".jpg"
                        image.save(random_hex)
                        users.set_image(random_hex)
                    db['customer'] = user_dict
                    db.close()
                    flash('Profile successfully updated', category='alert-success')
                    print(f"User {current_user.get_id()} profile updated")
                    return redirect(url_for('update'))
        except IOError:
            print("Error IO Error")
        except Exception as ex:
            print(f"unknown error occurred as {ex}")

    else:
        update_form.username.data = current_user.get_username()
        update_form.email.data = current_user.get_email()
        update_form.location.data = current_user.get_location()
        update_form.phone.data = current_user.get_phone()
        update_form.birthday.data = current_user.get_birthday()
        update_form.image.data = current_user.get_image()

    if request.method == "POST" and submit2:
        password1 = update_password_form.password1.data
        password2 = update_password_form.password2.data
        error = None
        try:
            db = shelve.open('DB/Customer/customer')
            user_dict = {}
            if 'customer' in db:
                user_dict = db['customer']
            else:
                db['customer'] = user_dict

            for users in user_dict.values():
                if users.get_id() == current_user.get_id():
                    if current_user.get_password() == password1:
                        users.set_password(password2)
                    else:
                        error = 'Current password is wrong'
            db['customer'] = user_dict
            db.close()

            flash('Password successfully changed!', category='alert-success')
            print(f'Password changed from {password1} to {password2}')

        except IOError:
            print("Error IO Error")
        except Exception as ex:
            print(f"unknown error occurred as {ex}")

    card_list = current_user.get_payment_methods()
    card_count = len(card_list)
    transaction_history = current_user.get_transaction_history()
    return render_template('update.html', update_form=update_form, update_password_form=update_password_form,
                           error=error, error2=error2, card_list=card_list, card_count=card_count, transaction_history=transaction_history)


# adding payment methods
@app.route('/addPaymentMethod', methods=['GET', 'POST'])
def add_payment_method():
    add_payment_methods = CreditCardForm()
    error = None
    if request.method == "POST":

        user_dict = {}
        try:
            db = shelve.open('DB/Customer/customer')
            if 'customer' in db:
                user_dict = db['customer']
            else:
                db['customer'] = user_dict

            if isValidCardNumber(str(add_payment_methods.card_number.data)):
                for users in user_dict.values():
                    if users.get_id() == current_user.get_id():
                        print(users)
                        card_list = users.get_payment_methods()
                        card_id = len(card_list) + 1
                        expiry_date = str(add_payment_methods.expiry_month.data) + '/' + str(add_payment_methods.expiry_year.data)
                        card = paymentMethods(card_id, add_payment_methods.full_name.data, add_payment_methods.card_number.data,
                                              add_payment_methods.cvv.data, expiry_date, add_payment_methods.street_address.data,
                                              add_payment_methods.unit_number.data, add_payment_methods.country.data, add_payment_methods.postal_code.data)
                        card_list.append(card)
                        users.set_payment_methods(card_list)
                db['customer'] = user_dict
                db.close()
                flash('New credit card added!', category='alert-success')
                return redirect('update')
            else:
                error = "Invalid credit card number"

        except IOError:
            print("IOError")
    return render_template('addPaymentMethod.html', form=add_payment_methods, error=error)


@app.route('/removePaymentMethod/<int:card_id>', methods=['GET', 'POST'])
def remove_payment_method(card_id):
    try:
        db = shelve.open('DB/Customer/customer')
        user_dict = {}
        if 'customer' in db:
            user_dict = db['customer']
        else:
            db['customer'] = user_dict

        card_list = []
        for user in user_dict.values():
            if user.get_id() == current_user.get_id():
                card_list = user.get_payment_methods()
                for cards in card_list:
                    if cards.get_card_id() == card_id:
                        index = card_list.index(cards)
                        del card_list[index]
            user.set_payment_methods(card_list)
            user_dict[user.get_id()] = user
            db['customer'] = user_dict
            db.close()
            flash('Credit card removed', category='alert-danger')
            return redirect(url_for('update'))

    except IOError:
        print("Error IO Error")
    except Exception as ex:
        print(f"unknown error occurred as {ex}")

    return redirect(url_for('update'))


# validation for card number
def isValidCardNumber(card_input):
    card_input = card_input[::- 1]
    card_input = [int(x) for x in card_input]
    for i in range(1, len(card_input), 2):
        card_input[i] *= 2

        if card_input[i] > 9:
            card_input[i] = card_input[i] % 10 + 1

    total = sum(card_input)

    return total % 10 == 0


@app.route('/logout', methods=['GET'])
@login_required
def logout():
    print(f"User {current_user.get_id()} logged out")
    logout_user()
    return redirect(url_for('home'))


@app.route('/delete', methods=['GET', 'POST'])
@login_required
def delete():
    try:
        db = shelve.open('DB/Customer/customer')
        user_dict = {}
        if 'customer' in db:
            user_dict = db['customer']
        else:
            db['customer'] = user_dict
        print(f"User {current_user.get_id()} account deleted")
        for user in user_dict.values():
            if user.get_id() == current_user.get_id():
                user.set_status('Suspended')
        logout()

        db['customer'] = user_dict
        db.close()
    except IOError:
        print("Error IO Error")
    except Exception as ex:
        print(f"unknown error occurred as {ex}")

    return render_template('home.html')


@app.route('/admin', methods=["GET"])
def adminPage():
    return render_template('admin.html')


def createStaff():
    username = input("Enter name: ")
    email = input("Enter email: ")
    password = "AdminPassword123"
    current_GMT = time.gmtime()
    user_id = (calendar.timegm(current_GMT))
    role = "Admin"
    cust_dict = {}
    try:
        db = shelve.open('DB/Customer/customer')
        if 'customer' in db:
            cust_dict = db['customer']
        else:
            db['customer'] = cust_dict

        Admin = User(username, email, password, user_id, role, 'Active')
        cust_dict[Admin.get_id()] = Admin
        db['customer'] = cust_dict
        db.close()

    except IOError:
        print("Error IO Error")
    except Exception as ex:
        print(f"unknown error occurred as {ex}")


def massAccount(amount):
    cust_dict = {}
    try:
        db = shelve.open('DB/Customer/customer')
        if 'customer' in db:
            cust_dict = db['customer']
        else:
            db['customer'] = cust_dict
        for i in range(amount):
            Admin = User(f"test{i+1}", f"test{i+1}@gmail.com", "TESTTEST", int(i+1), 'Admin', "Active")

            cust_dict[Admin.get_id()] = Admin
            db['customer'] = cust_dict
        db.close()
    except IOError:
        print("IOError")


@app.route('/retrieveUsers')
def retrieve_users():
    users_list = []
    users_dict = {}
    staff_list = []
    customer_list = []
    active_list = []
    try:
        db = shelve.open('DB/Customer/customer')
        if 'customer' in db:
            users_dict = db['customer']
        else:
            db['customer'] = users_dict
        db.close()
        for key in users_dict:
            user = users_dict.get(key)
            users_list.append(user)
            if user.get_role() == "Admin":
                staff_list.append(user)
            if user.get_role() == "Customer":
                customer_list.append(user)
            if user.get_status() == "Active":
                active_list.append(user)

    except IOError:
        print("Error IO Error")
    except Exception as ex:
        print(f"unknown error occurred as {ex}")

    return render_template('retrieveUsers.html', count=len(users_list), users_list=users_list, staff_count=len(staff_list), customer_count=len(customer_list), active_count=len(active_list))


@app.route('/updateUser/<int:user_id>/', methods=['GET', 'POST'])
def update_user(user_id):
    update_profile_form = UpdateProfileForm()
    if request.method == 'POST':
        users_dict = {}
        try:
            db = shelve.open('DB/Customer/customer')
            if 'customer' in db:
                users_dict = db['customer']
            else:
                db['customer'] = users_dict
            user = users_dict.get(str(user_id))
            user.set_username(update_profile_form.username.data)
            user.set_email(update_profile_form.email.data)
            user.set_status(update_profile_form.status.data)
            user.set_role(update_profile_form.role.data)
            db['customer'] = users_dict
            db.close()
            flash(f'Account updated!', category='alert-success')
        except IOError:
            print("IOError")
        except Exception as ex:
            print(f"Exception Error as {ex}")

        return redirect(url_for('retrieve_users'))
    else:
        users_dict = {}
        try:
            db = shelve.open('DB/Customer/customer')
            if 'customer' in db:
                users_dict = db['customer']
            else:
                db['customer'] = users_dict
            user = users_dict.get(str(user_id))
            update_profile_form.username.data = user.get_username()
            update_profile_form.email.data = user.get_email()
            update_profile_form.status.data = user.get_status()
            update_profile_form.role.data = user.get_role()
            db.close()
        except IOError:
            print("IOError")
        except Exception as ex:
            print(f"Exception Error as {ex}")

    return render_template('updateUser.html', form=update_profile_form)


@app.route('/deleteUsers/<int:user_id>', methods=['POST'])
def delete_user(user_id):
    users_dict = {}
    try:
        db = shelve.open('DB/Customer/customer')
        if 'customer' in db:
            users_dict = db['customer']
        else:
            db['customer'] = users_dict

        users_dict.pop(str(user_id))

        db['customer'] = users_dict
        db.close()
        flash('Account successfully deleted!', category='alert-success')
    except IOError:
        print("IOError")
    except Exception as ex:
        print(f"Exception Error as {ex}")

    return redirect(url_for('retrieve_users'))


def send_reset_email(user):
    token = user.get_reset_token()
    msg = Message('Password Reset Request', sender='doctordonutservices@gmail.com', recipients=[user.get_email()])
    msg.body = f""" To reset your password, visit the following link:
{url_for('reset_token', token=token, _external=True)}

If you did not make this request, then simply ignore this email and no changes will be made
"""
    mail.send(msg)


@app.route('/reset_password', methods=['GET', 'POST'])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RequestResetForm()
    if form.validate_on_submit():
        users_dict = {}
        db = shelve.open('DB/Customer/customer')
        if 'customer' in db:
            users_dict = db['customer']
        else:
            db['customer'] = users_dict
        db.close()
        for users in users_dict.values():
            if users.get_email() == form.email.data:
                print(type(users))
                print(users)
                print(users.get_email())
                send_reset_email(users)
                flash('An email has been sent with instructions to reset your password', 'alert-success')
                return redirect(url_for('login'))

    return render_template('reset_request.html', title='Reset Password', form=form)


@app.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    user = User.verify_reset_token(token)
    if user is None:
        flash('That is an invalid or expired token', 'alert-danger')
        return redirect(url_for('reset_request'))
    form = ResetPasswordForm()
    error = None
    if request.method == "POST":
        users_dict = {}
        try:
            db = shelve.open('DB/Customer/customer')
            if 'customer' in db:
                users_dict = db['customer']
            else:
                db['customer'] = users_dict
            if form.password.data == form.confirm_password.data:
                user.set_password(form.password.data)
            else:
                error = "Both passwords do not match"
            users_dict[user.get_id()] = user
            db['customer'] = users_dict
            db.close()
        except IOError:
            print("IOError")
        except Exception as ex:
            print(f"Exception Error as {ex}")
    return render_template('reset_token.html', title='Reset Password', form=form, error=error)
# end of account management
# start customer support


@app.route('/messagesOverview')
def messages_overview():
    return render_template('messagesOverview.html')


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

            message = Messages(name, email, subject, message)
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
    flash("Message deleted", category='alert-success')
    return redirect(url_for('retrieveMessages'))


# end customer support
# start of hiring
@app.route('/createResumes', methods=['GET', 'POST'])
def create_resumes():
    create_resumes_form = CreateResumesForm(request.form)
    if request.method == 'POST' and create_resumes_form.validate():
        resumes_dict = {}
        db = shelve.open('DB/Hiring/resume')

        try:
            resumes_dict = db['Resumes']
        except:
            print("Error in retrieving Resumes from Resumes.db.")

        resumes = Resumes(create_resumes_form.first_name.data, create_resumes_form.last_name.data,
                          create_resumes_form.email.data, create_resumes_form.sgorpr.data,
                          create_resumes_form.citizenship.data, create_resumes_form.address.data,
                          create_resumes_form.contactno.data, create_resumes_form.preferredjob.data,create_resumes_form.uploadfile.data )
        for key in resumes_dict:
            if key == resumes.get_resumes_id():
                resumes.set_resumes_id(int(resumes.get_resumes_id()) + 1)
        resumes_dict[resumes.get_resumes_id()] = resumes
        db['Resumes'] = resumes_dict

        db.close()
        flash('Resume submitted!', category='success')
        return redirect(url_for('home'))
    return render_template('createResumes.html', form=create_resumes_form)


@app.route('/createJobPositions', methods=['GET', 'POST'])
def create_job_positions():
    create_job_positions_form = CreateJobPositionsForm()
    if request.method == 'POST':
        job_positions_dict = {}
        db = shelve.open('DB/Hiring/jobPositions')
        image = Image.open(create_job_positions_form.job_image.data)
        image.resize((300, 300))
        random_hex = secrets.token_hex(8)
        random_hex = "static/jobImages/" + random_hex + ".png"
        image.save(random_hex)
        try:
            job_positions_dict = db['JobPositions']
        except:
            print("Error in retrieving Job Positions from JobPositions.db.")

        job_position = JobPositions(create_job_positions_form.job_name.data,
                                    create_job_positions_form.job_availability.data,
                                    create_job_positions_form.job_responsibility.data,
                                    create_job_positions_form.job_salary.data,
                                    random_hex)
        for key in job_positions_dict:
            if key == job_position.get_id():
                job_position.set_id(int(job_position.get_id() + 1))
        job_positions_dict[job_position.get_id()] = job_position
        db['JobPositions'] = job_positions_dict

        db.close()

        return redirect(url_for('retrieve_jobpositions'))
    return render_template('createJobPositions.html', form=create_job_positions_form)


@app.route('/retrieveResumes')
def retrieve_resumes():
    resumes_dict = {}
    db = shelve.open('DB/Hiring/resume')
    resumes_dict = db['Resumes']
    db.close()

    resumes_list = []
    for key in resumes_dict:
        resumes = resumes_dict.get(key)
        resumes_list.append(resumes)

    return render_template('retrieveResumes.html', count=len(resumes_list), resumes_list=resumes_list)


@app.route('/retrieveJobPositions')
def retrieve_jobpositions():
    job_positions_dict = {}
    db = shelve.open('DB/Hiring/jobPositions')
    job_positions_dict = db['JobPositions']
    db.close()

    job_positions_list = []
    for key in job_positions_dict:
        job_positions = job_positions_dict.get(key)
        job_positions_list.append(job_positions)

    return render_template('retrieveJobPositions.html', count=len(job_positions_list), job_positions_list=job_positions_list)


@app.route('/displayJobPositions')
def display_jobpositions():
    job_positions_dict = {}
    db = shelve.open('DB/Hiring/jobPositions')
    job_positions_dict = db['JobPositions']
    db.close()

    job_positions_list = []
    for key in job_positions_dict:
        job_positions = job_positions_dict.get(key)
        job_positions_list.append(job_positions)

    return render_template('displayJobPositions.html', count=len(job_positions_list), jobpositions_list=job_positions_list)


@app.route('/updateJobPositions/<int:id>/', methods=['GET', 'POST'])
def update_jobpositions(id):
    update_job_positions_form = CreateJobPositionsForm()
    if request.method == 'POST':
        job_positions_dict = {}
        db = shelve.open('DB/Hiring/jobPositions')
        job_positions_dict = db['JobPositions']
        image = Image.open(update_job_positions_form.job_image.data)
        image.resize((300, 300))
        random_hex = secrets.token_hex(8)
        random_hex = "static/jobImages/" + random_hex + ".png"
        image.save(random_hex)
        job_positions = job_positions_dict.get(id)
        job_positions.set_job_name(update_job_positions_form.job_name.data)
        job_positions.set_job_availability(update_job_positions_form.job_availability.data)
        job_positions.set_job_responsibility(update_job_positions_form.job_responsibility.data)
        job_positions.set_job_salary(update_job_positions_form.job_salary.data)
        job_positions.set_job_image(random_hex)
        db['JobPositions'] = job_positions_dict
        db.close()
        flash('Job successfully updated!', category='alert-success')
        return redirect(url_for('retrieve_jobpositions'))
    else:
        job_positions_dict = {}
        db = shelve.open('DB/Hiring/jobPositions')
        job_positions_dict = db['JobPositions']
        db.close()

        job_positions = job_positions_dict.get(id)
        update_job_positions_form.job_name.data = job_positions.get_job_name()
        update_job_positions_form.job_availability.data = job_positions.get_job_availability()
        update_job_positions_form.job_responsibility.data = job_positions.get_job_responsibility()
        update_job_positions_form.job_salary.data = job_positions.get_job_salary()

        return render_template('updateJobPositions.html', form=update_job_positions_form)


@app.route('/deleteResumes/<int:id>', methods=['POST'])
def delete_resumes(id):
    resumes_dict = {}
    db = shelve.open('DB/Hiring/resume')
    resumes_dict = db['Resumes']

    resumes_dict.pop(id)

    db['Resumes'] = resumes_dict
    db.close()
    flash("Resume deleted!", category='alert-success')
    return redirect(url_for('retrieve_resumes'))


@app.route('/deleteJobPositions/<int:id>', methods=['POST'])
def delete_jobpositions(id):
    jobpositions_dict = {}
    db = shelve.open('DB/Hiring/jobPositions')
    jobpositions_dict = db['JobPositions']
    jobpositions_dict.pop(id)

    db['JobPositions'] = jobpositions_dict
    db.close()
    flash("Job deleted!", category='alert-success')
    return redirect(url_for('retrieve_jobpositions'))


@app.route('/viewJobs', methods=['GET', 'POST'])
def view_jobs():
    jobs_dict = {}
    db = shelve.open('DB/Hiring/jobPositions')
    jobs_dict = db['JobPositions']
    db.close()

    jobs_list = []
    for key in jobs_dict:
        jobs = jobs_dict.get(key)
        jobs_list.append(jobs)

    return render_template('viewJobs.html', count=len(jobs_list),
                           jobs_list=jobs_list)
# end of hiring
# start of transaction processing


@app.route('/createProducts', methods=['POST', 'GET'])
def create_products():
    create_product_form = CreateProductForm()
    print(create_product_form.Image.data)
    if request.method == 'POST':
        products_dict = {}
        image = Image.open(create_product_form.Image.data)
        random_hex = secrets.token_hex(8)
        random_hex = "static/donutImages/" + random_hex + ".png"
        image.save(random_hex)
        try:
            db = shelve.open('DB/Product/product')
            if 'Products' in db:
                products_dict = db['Products']
            else:
                db['Products'] = products_dict

            product = Product(create_product_form.Name.data, create_product_form.Rating.data,
                              create_product_form.Description.data, round(create_product_form.Price.data, 2), random_hex)
            products_dict[product.get_product_id()] = product
            db['Products'] = products_dict
            db.close()
            flash('Product created!', category='alert-success')
            return redirect(url_for('retrieve_product'))
        except IOError:
            print("IOError")
        except Exception as ex:
            print(f"Exception Error as {ex}")

    return render_template('createProducts.html', form=create_product_form)


@app.route('/products')
def display_product():
    products_dict = {}
    products_list = []
    add_to_cart = AddToCart()
    try:
        db = shelve.open('DB/Product/product')
        if 'Products' in db:
            products_dict = db['Products']
        else:
            db['Products'] = products_dict
        db = shelve.open('DB/Product/product', 'r')
        products_dict = db['Products']
        db.close()
        for key in products_dict:
            product = products_dict.get(key)
            products_list.append(product)

    except IOError:
        print("IOError")
    except Exception as ex:
        print(f"Exception Error as {ex}")

    return render_template('products.html', count=len(products_list), products_list=products_list, form=add_to_cart)


@app.route('/retrieveProducts')
def retrieve_product():
    products_dict = {}
    products_list = []
    try:
        db = shelve.open('DB/Product/product')
        if 'Products' in db:
            products_dict = db['Products']
        else:
            db['Products'] = products_dict
        db.close()
        products_list = []
        for key in products_dict:
            product = products_dict.get(key)
            products_list.append(product)
    except IOError:
        print("IOError")
    except Exception as ex:
        print(f"Exception Error as {ex}")
    return render_template('retrieveProducts.html', count=len(products_list), products_list=products_list)


@app.route('/addToCart/<int:product_id>', methods=['GET', 'POST'])
def add_cart(product_id):
    add_to_cart = AddToCart()
    user_dict = {}
    product_dict = {}
    error = None
    if request.method == "POST":
        try:
            db = shelve.open('DB/Customer/customer')
            if 'customer' in db:
                user_dict = db['customer']
            else:
                db['customer'] = user_dict

            user = user_dict.get(current_user.get_id())
            cart = user.get_cart()

            db2 = shelve.open('DB/Product/product')
            if 'Products' in db2:
                product_dict = db2['Products']
            else:
                db2['Products'] = product_dict
            if add_to_cart.Quantity.data >= 1:
                cart_id = len(cart) + 1
                product = product_dict.get(product_id)
                cart_item = cartItems(product.get_name(), add_to_cart.Quantity.data, product.get_price(), product_id, cart_id, product.get_image())
                cart.append(cart_item)
                user.set_cart(cart)
                db['customer'] = user_dict
                db.close()
                db2.close()
                print("item added")
                flash(f'Item added', category='alert-success')
            else:
                flash(f'Quantity cannot be less than 1', category='alert-danger')

        except IOError:
            print("IOError")
        except Exception as ex:
            print(f"Exception Error as {ex}")
        return redirect(url_for('display_product'))


@app.route('/cart', methods=['GET', 'POST'])
def cart():
    user_dict = {}
    cart_list = []
    card_list = []
    subtotal = 0
    total = 0
    cart_count = 0
    card_count = 0
    try:
        db = shelve.open('DB/Customer/customer')
        if 'customer' in db:
            user_dict = db['customer']
        else:
            db['customer'] = user_dict

        user = user_dict.get(current_user.get_id())
        card_list = user.get_payment_methods()
        cart_list = user.get_cart()
        cart_count = len(cart_list)
        card_count = len(card_list)
        subtotal = 0
        for items in cart_list:
            subtotal += items.get_total_item_price()

        total = float(subtotal) + 2.99
        total = "{:.2f}".format(total)

    except IOError:
        print("IOError")
    except Exception as ex:
        print(f"Exception Error as {ex}")
    return render_template('cart.html', cart_list=cart_list, total=total, subtotal=subtotal, card_list=card_list, card_count=card_count, cart_count=cart_count)


@app.route('/checkOut', methods=["GET", "POST"])
def check_out():
    try:
        db = shelve.open('DB/Customer/customer')
        user_dict = {}
        if 'customer' in db:
            user_dict = db['customer']
        else:
            db['customer'] = user_dict

        timestamp = time.time()
        date_time = datetime.fromtimestamp(timestamp)
        str_date_time = date_time.strftime("%d-%m-%Y, %H:%M:%S")
        user = user_dict.get(current_user.get_id())
        transaction_history = user.get_transaction_history()
        transaction_id = len(transaction_history) + 1
        cart_list = user.get_cart()
        subtotal = 0
        for items in cart_list:
            subtotal += items.get_total_item_price()

        total = float(subtotal) + 2.99
        transaction = transactionHistory(transaction_id, str_date_time, total)
        transaction_history.append(transaction)
        user.set_transaction_history(transaction_history)

        cart_list.clear()
        user.set_cart(cart_list)
        db['customer'] = user_dict
        flash("Order purchased successfully!")
        print(transaction_history)
        db.close()

    except IOError:
        print("IOError")
    except Exception as ex:
        print(f"Exception Error as {ex}")
    return redirect(url_for('home'))


@app.route('/updateProducts/<int:id>/', methods=['GET', 'POST'])
def update_product(id):
    update_product_form = CreateProductForm()
    if request.method == 'POST':

        products_dict = {}
        try:
            db = shelve.open('DB/Product/product')
            if 'Products' in db:
                products_dict = db['Products']
            else:
                db['Products'] = products_dict

            image = Image.open(update_product_form.Image.data)
            random_hex = secrets.token_hex(8)
            random_hex = "static/donutImages/" + random_hex + ".png"
            image.save(random_hex)
            product = products_dict.get(id)
            print(product)
            product.set_name(update_product_form.Name.data)
            product.set_rating(update_product_form.Rating.data)
            product.set_description(update_product_form.Description.data)
            product.set_price(round(update_product_form.Price.data, 2))
            product.set_image(random_hex)
            db['Products'] = products_dict
            db.close()
        except IOError:
            print("IOError")
        except Exception as ex:
            print(f"Exception Error as {ex}")

        return redirect(url_for('retrieve_product'))
    else:
        products_dict = {}
        db = shelve.open('DB/Product/product', 'r')
        products_dict = db['Products']
        db.close()

        product = products_dict.get(id)
        update_product_form.Name.data = product.get_name()
        update_product_form.Rating.data = product.get_rating()
        update_product_form.Description.data = product.get_description()
        update_product_form.Price.data = product.get_price()
        update_product_form.Image.data = product.get_image()

        return render_template('updateProducts.html', form=update_product_form)


@app.route('/deleteItem/<int:cart_id>/', methods=['GET', 'POST'])
def delete_item(cart_id):
    try:
        db = shelve.open('DB/Customer/customer')
        user_dict = {}
        if 'customer' in db:
            user_dict = db['customer']
        else:
            db['customer'] = user_dict

        user = user_dict.get(current_user.get_id())
        cart_list = user.get_cart()
        for carts in cart_list:
            if carts.get_cart_id() == cart_id:
                index = cart_list.index(carts)
                del cart_list[index]

        user.set_cart(cart_list)
        user_dict[user.get_id()] = user
        db['customer'] = user_dict
        db.close()
        flash('Item removed', category='alert-danger')
        return redirect(url_for('cart'))

    except IOError:
        print("Error IO Error")
    except Exception as ex:
        print(f"unknown error occurred as {ex}")

    return redirect(url_for('cart'))


@app.route('/deleteProduct/<int:id>/', methods=['POST', 'GET'])
def delete_product(id):
    products_dict = {}
    db = shelve.open('DB/Product/product', 'w')
    products_dict = db['Products']

    products_dict.pop(id)

    db['Products'] = products_dict
    db.close()

    return redirect(url_for('retrieve_product'))


@app.get("/")
def index_get():
    return render_template("base.html")


@app.post("/predict")
def predict():
    text = request.get_json().get("message")
    response = get_response(text)
    message = {"answer": response}
    return jsonify(message)


# report generation
@app.route('/createReport', methods=['GET', 'POST'])
def create_report():
    create_report_form = CreateReportForm(request.form)
    if request.method == 'POST' and create_report_form.validate():
        reports_dict = {}
        db = shelve.open('DB/Report/report', 'c')

        try:
            reports_dict = db['Reports']
        except:
            print("Error in retrieving Reports from report.db.")

        report = Report(create_report_form.first_name.data, create_report_form.last_name.data, create_report_form.gender.data, create_report_form.membership.data, create_report_form.remarks.data)
        reports_dict[report.get_report_id()] = report
        db['Reports'] = reports_dict

        db.close()

        return redirect(url_for('retrieve_reports'))
    return render_template('createReport.html', form=create_report_form)


@app.route('/retrieveReports')
def retrieve_reports():
    reports_dict = {}
    reports_list = []
    try:
        db = shelve.open('DB/Report/report', 'r')
        if 'Reports' in db:
            reports_dict = db['Reports']
        else:
            db['Reports'] = reports_dict

        db.close()

        reports_list = []

        for key in reports_dict:
            report = reports_dict.get(key)
            reports_list.append(report)
    except:
        print('error')

    return render_template('retrieveReport.html', count=len(reports_list), reports_list=reports_list)


@app.route('/updateReport/<int:id>/', methods=['GET', 'POST'])
def update_report(id):
    update_report_form = CreateReportForm(request.form)
    if request.method == 'POST' and update_report_form.validate():
        reports_dict = {}
        db = shelve.open('DB/Report/report', 'w')
        reports_dict = db['Reports']

        report = reports_dict.get(id)
        report.set_first_name(update_report_form.first_name.data)
        report.set_last_name(update_report_form.last_name.data)
        report.set_gender(update_report_form.gender.data)
        report.set_membership(update_report_form.membership.data)
        report.set_remarks(update_report_form.remarks.data)

        db['Reports'] = reports_dict
        db.close()

        return redirect(url_for('retrieve_reports'))
    else:
        reports_dict = {}
        db = shelve.open('DB/Report/report', 'r')
        reports_dict = db['Reports']
        db.close()

        report = reports_dict.get(id)
        update_report_form.first_name.data = report.get_first_name()
        update_report_form.last_name.data = report.get_last_name()
        update_report_form.gender.data = report.get_gender()
        update_report_form.membership.data = report.get_membership()
        update_report_form.remarks.data = report.get_remarks()

        return render_template('updateReport.html', form=update_report_form)


@app.route('/deleteReport/<int:id>', methods=['POST'])
def delete_report(id):
    reports_dict = {}
    db = shelve.open('DB/Report/report', 'w')
    reports_dict = db['Reports']

    reports_dict.pop(id)

    db['Reports'] = reports_dict
    db.close()

    return redirect(url_for('retrieve_reports'))


if __name__ == '__main__':
    app.run(debug=True)
