from flask import Flask, render_template, request, redirect, url_for, flash
from flask_login import LoginManager, login_user, logout_user, current_user, login_required
from models.auth.auth_forms import RegisterForm, LoginForm, UpdateProfileForm, UpdatePasswordForm
from models.auth.user import User
from models.cust.contactMessage import Message
from models.cust.contactForm import CreateMessageForm
from models.hiring.hiringForm import CreateResumesForm, CreateJobPositionsForm
from models.hiring.resume import Resumes
from models.hiring.jobPositions import JobPositions
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
                users.set_image(update_form.image.data)
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
        update_form.image.data = current_user.get_image()

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


@app.route('/admin', methods=["GET"])
def adminPage():
    return render_template('admin.html')

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

        return redirect(url_for('retrieve_resumes'))
    return render_template('createResumes.html', form=create_resumes_form)


@app.route('/createJobPositions', methods=['GET', 'POST'])
def create_jobpositions():
    create_jobpositions_form = CreateJobPositionsForm(request.form)
    if request.method == 'POST' and create_jobpositions_form.validate():
        jobpositions_dict = {}
        db = shelve.open('DB/Hiring/jobPositions')

        try:
            jobpositions_dict = db['JobPositions']
        except:
            print("Error in retrieving Job Positions from JobPositions.db.")

        jobpositions = JobPositions(create_jobpositions_form.jobname.data,
                                    create_jobpositions_form.jobavailability.data,
                                    create_jobpositions_form.jobrequirements.data,
                                    create_jobpositions_form.jobresponsibility.data,
                                    create_jobpositions_form.jobsalary.data)
        #        customers_dict[customer.get_customer_id()] = customer
        for key in jobpositions_dict:
            if key == jobpositions.get_id():
                jobpositions.set_id(int(jobpositions.get_id() + 1))
        jobpositions_dict[jobpositions.get_id()] = jobpositions
        db['JobPositions'] = jobpositions_dict

        db.close()

        return redirect(url_for('retrieve_jobpositions'))
    return render_template('createJobPositions.html', form=create_jobpositions_form)


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
    jobpositions_dict = {}
    db = shelve.open('DB/Hiring/jobPositions')
    jobpositions_dict = db['JobPositions']
    db.close()

    jobpositions_list = []
    for key in jobpositions_dict:
        jobpositions = jobpositions_dict.get(key)
        jobpositions_list.append(jobpositions)

    return render_template('retrieveJobPositions.html', count=len(jobpositions_list), jobpositions_list=jobpositions_list)
@app.route('/displayJobPositions/')
def display_jobpositions():
    jobpositions_dict = {}
    db = shelve.open('DB/Hiring/jobPositions')
    jobpositions_dict = db['JobPositions']
    db.close()

    jobpositions_list = []
    for key in jobpositions_dict:
        jobpositions = jobpositions_dict.get(key)
        jobpositions_list.append(jobpositions)

    return render_template('displayJobPositions.html',count=len(jobpositions_list), jobpositions_list=jobpositions_list)

@app.route('/updateResumes/<int:id>/', methods=['GET', 'POST'])
def update_resumes(id):
    update_resumes_form = CreateResumesForm(request.form)
    if request.method == 'POST' and update_resumes_form.validate():
        resumes_dict = {}
        db = shelve.open('DB/Hiring/resume')
        resumes_dict = db['Resumes']

        resumes = resumes_dict.get(id)
        resumes.set_first_name(update_resumes_form.first_name.data)
        resumes.set_last_name(update_resumes_form.last_name.data)
        resumes.set_email(update_resumes_form.email.data)
        resumes.set_sgorpr(update_resumes_form.sgorpr.data)
        resumes.set_citizenship(update_resumes_form.citizenship.data)
        resumes.set_address(update_resumes_form.address.data)
        resumes.set_contactno(update_resumes_form.contactno.data)
        resumes.set_preferredjob(update_resumes_form.preferredjob.data)
        resumes.set_uploadfile(update_resumes_form.uploadfile.data)

        db['Resumes'] = resumes_dict
        db.close()

        return redirect(url_for('retrieve_resumes'))
    else:
        resumes_dict = {}
        db = shelve.open('DB/Hiring/resume')
        resumes_dict = db['Resumes']
        db.close()

        resumes = resumes_dict.get(id)
        update_resumes_form.first_name.data = resumes.get_first_name()
        update_resumes_form.last_name.data = resumes.get_last_name()
        update_resumes_form.email.data = resumes.get_email()
        update_resumes_form.sgorpr.data = resumes.get_sgorpr()
        update_resumes_form.citizenship.data = resumes.get_citizenship()
        update_resumes_form.address.data = resumes.get_address()
        update_resumes_form.contactno.data = resumes.get_contactno()
        update_resumes_form.preferredjob.data = resumes.get_preferredjob()
        update_resumes_form.uploadfile.data = resumes.get_uploadfile()

        return render_template('updateResumes.html', form=update_resumes_form)


@app.route('/updateJobPositions/<int:id>/', methods=['GET', 'POST'])
def update_jobpositions(id):
    update_jobpositions_form = CreateJobPositionsForm(request.form)
    if request.method == 'POST' and update_jobpositions_form.validate():
        jobpositions_dict = {}
        db = shelve.open('DB/Hiring/jobPositions')
        jobpositions_dict = db['JobPositions']

        jobpositions = jobpositions_dict.get(id)
        jobpositions.set_jobname(update_jobpositions_form.jobname.data)
        jobpositions.set_jobavailability(update_jobpositions_form.jobavailability.data)
        jobpositions.set_jobrequirements(update_jobpositions_form.jobrequirements.data)
        jobpositions.set_jobresponsibility(update_jobpositions_form.jobresponsibility.data)
        jobpositions.set_jobsalary(update_jobpositions_form.jobsalary.data)

        db['JobPositions'] = jobpositions_dict
        db.close()

        return redirect(url_for('retrieve_jobpositions'))
    else:
        jobpositions_dict = {}
        db = shelve.open('DB/Hiring/jobPositions')
        jobpositions_dict = db['JobPositions']
        db.close()

        jobpositions = jobpositions_dict.get(id)
        update_jobpositions_form.jobname.data = jobpositions.get_jobname()
        update_jobpositions_form.jobavailability.data = jobpositions.get_jobavailability()

        update_jobpositions_form.jobrequirements.data = jobpositions.get_jobrequirements()
        update_jobpositions_form.jobresponsibility.data = jobpositions.get_jobresponsibility()
        update_jobpositions_form.jobsalary.data = jobpositions.get_jobsalary()

        return render_template('updateJobPositions.html', form=update_jobpositions_form)


@app.route('/deleteResumes/<int:id>', methods=['POST'])
def delete_resumes(id):
    resumes_dict = {}
    db = shelve.open('DB/Hiring/resume')
    resumes_dict = db['Resumes']

    resumes_dict.pop(id)

    db['Resumes'] = resumes_dict
    db.close()

    return redirect(url_for('retrieve_resumes'))


@app.route('/deleteJobPositions/<int:id>', methods=['POST'])
def delete_jobpositions(id):
    jobpositions_dict = {}
    db = shelve.open('DB/Hiring/jobPositions')
    jobpositions_dict = db['JobPositions']
    jobpositions_dict.pop(id)

    db['JobPositions'] = jobpositions_dict
    db.close()

    return redirect(url_for('retrieve_jobpositions'))
# end of hiring


if __name__ == '__main__':
    app.run(debug=True)
