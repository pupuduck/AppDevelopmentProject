from flask import Flask, render_template, request, redirect, url_for, flash
from flask_login import LoginManager, login_user, logout_user, current_user, login_required
from models.auth.auth_forms import RegisterForm, LoginForm, UpdateProfileForm, UpdatePasswordForm
from models.auth.user import User
from models.cust.contactMessage import Message
from models.cust.contactForm import CreateMessageForm
from models.hiring.hiringForm import CreateResumesForm, CreateJobPositionsForm
from models.hiring.resume import Resumes
from models.hiring.jobPositions import JobPositions
from models.products.productForm import CreateProductForm
from models.products.product import Product
from PIL import Image
import secrets
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
            if username == user.get_username() and user.get_status() == 'Active':
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
                c1 = User(username, email, password, id, 'Customer', 'Active')
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

                image = Image.open(update_form.image.data)
                random_hex = secrets.token_hex(8)
                random_hex = "static/profileImage/" + random_hex + ".jpg"
                image.save(random_hex)
                users.set_image(random_hex)
                db['customer'] = user_dict
                db.close()
                flash('Profile successfully updated')
                print(f"User {current_user.get_id()} profile updated")
                return redirect(url_for('update'))

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


@app.route('/delete', methods=['GET', 'POST'])
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
    id = (calendar.timegm(current_GMT))
    role = "Admin"
    cust_dict = {}
    try:
        db = shelve.open('DB/Customer/customer')
        if 'customer' in db:
            cust_dict = db['customer']
        else:
            db['customer'] = cust_dict

        Admin = User(username, email, password, id, role, 'Active')
        cust_dict[Admin.get_id()] = Admin
        db['customer'] = cust_dict
        db.close()

    except IOError:
        print("Error IO Error")
    except Exception as ex:
        print(f"unknown error occurred as {ex}")


@app.route('/retrieveUsers')
def retrieve_users():
    users_dict = {}
    db = shelve.open('DB/Customer/customer')
    users_dict = db['customer']
    db.close()

    users_list = []
    for key in users_dict:
        user = users_dict.get(key)
        users_list.append(user)

    return render_template('retrieveUsers.html', count=len(users_list), users_list=users_list)


@app.route('/deleteUsers/<int:id>', methods=['POST'])
def delete_user(id):
    users_dict = {}
    try:
        db = shelve.open('DB/Customer/customer')
        users_dict = db['customer']
        if 'customer' in db:
            users_dict = db['customer']
        else:
            db['customer'] = users_dict

        users_dict.pop(str(id))

        db['customer'] = users_dict
        db.close()
    except IOError:
        print('Error IO error')

    return redirect(url_for('retrieve_users'))


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
                                    create_job_positions_form.job_requirements.data,
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
    update_job_positions_form = CreateJobPositionsForm()
    if request.method == 'POST':
        job_positions_dict = {}
        db = shelve.open('DB/Hiring/jobPositions')
        job_positions_dict = db['JobPositions']

        job_positions = job_positions_dict.get(id)
        job_positions.set_job_name(update_job_positions_form.job_name.data)
        job_positions.set_job_availability(update_job_positions_form.job_availability.data)
        job_positions.set_job_requirements(update_job_positions_form.job_requirements.data)
        job_positions.set_job_responsibility(update_job_positions_form.job_responsibility.data)
        job_positions.set_job_salary(update_job_positions_form.job_salary.data)

        db['JobPositions'] = job_positions_dict
        db.close()

        return redirect(url_for('retrieve_jobpositions'))
    else:
        job_positions_dict = {}
        db = shelve.open('DB/Hiring/jobPositions')
        job_positions_dict = db['JobPositions']
        db.close()

        job_positions = job_positions_dict.get(id)
        update_job_positions_form.job_name.data = job_positions.get_jobname()
        update_job_positions_form.job_availability.data = job_positions.get_jobavailability()

        update_job_positions_form.job_requirements.data = job_positions.get_jobrequirements()
        update_job_positions_form.job_responsibility.data = job_positions.get_jobresponsibility()
        update_job_positions_form.job_salary.data = job_positions.get_jobsalary()

        return render_template('updateJobPositions.html', form=update_job_positions_form)


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
        except IOError:
            print("IOError")
        except Exception as ex:
            print(f"Exception Error as {ex}")

    return render_template('createProducts.html', form=create_product_form)


@app.route('/products')
def display_product():
    products_dict = {}
    db = shelve.open('DB/Product/product', 'r')
    products_dict = db['Products']
    db.close()

    products_list = []
    for key in products_dict:
        product = products_dict.get(key)
        products_list.append(product)

    return render_template('products.html', count=len(products_list), products_list=products_list)


@app.route('/retrieveProducts')
def retrieve_product():
    update_product_form = CreateProductForm()
    products_dict = {}
    db = shelve.open('DB/Product/product', 'r')
    products_dict = db['Products']
    db.close()

    products_list = []
    for key in products_dict:
        product = products_dict.get(key)
        products_list.append(product)

    return render_template('retrieveProducts.html', count=len(products_list), products_list=products_list, form=update_product_form)


@app.route('/updateProducts/<int:id>/', methods=['GET', 'POST'])
def update_product(id):
    update_product_form = CreateProductForm()
    if request.method == 'POST' and update_product_form.validate():
        products_dict = {}
        db = shelve.open('DB/Product/product', 'w')
        products_dict = db['Products']

        product = products_dict.get(id)
        product.set_name(update_product_form.Name.data)
        product.set_rating(update_product_form.Rating.data)
        product.set_description(update_product_form.Description.data)
        product.set_price(round(update_product_form.Price.data, 2))

        db['Products'] = products_dict
        db.close()

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

        return render_template('updateProducts.html', form=update_product_form)


@app.route('/deleteProduct/<int:id>', methods=['POST'])
def delete_product(id):
    products_dict = {}
    db = shelve.open('DB/Product/product', 'w')
    products_dict = db['Products']

    products_dict.pop(id)

    db['Products'] = products_dict
    db.close()

    return redirect(url_for('retrieve_product'))


if __name__ == '__main__':
    app.run(debug=True)
