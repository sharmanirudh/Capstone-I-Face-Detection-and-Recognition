import os
import secrets
from PIL import Image
from flask import render_template, url_for, flash, redirect, request
from app import app, db, bcrypt
from app import faces
from app.forms import RegistrationForm, LoginForm, SignUpForm, UpdateAccountForm
from app.models import User, Person, Dataset
from flask_login import login_user, current_user, logout_user, login_required

def save_image(form_image):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_image.filename)
    image_fn = random_hex + f_ext
    image_path = os.path.join(app.root_path, 'static/user_images', image_fn)

    output_size = (400, 400)
    i = Image.open(form_image)
    i.thumbnail(output_size)
    i.save(image_path)
    
    return image_fn, image_path


@app.route("/", methods=['GET','POST'])
@app.route("/home", methods=['GET','POST'])
@app.route("/login", methods=['GET','POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('register_face', title='Register Face', selectedListElement='registerFace'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('register_face', title='Register Face', selectedListElement='registerFace'))
        else:
            flash(f'Login unsuccessful. Please check email and password.', 'danger')
    return render_template('login.html', title='Login', form=form)


@app.route("/signup", methods=['GET','POST'])
def sign_up():
    if current_user.is_authenticated:
        return redirect(url_for('register_face', title='Register Face'))
    form = SignUpForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        logout_user()
        flash(f'Congratulations! You can now login.', 'success')
        return redirect(url_for('login', title='Login'))
    return render_template('sign_up.html', title='Sign up', form=form)


@app.route("/faces/register", methods=['GET','POST'])
@login_required
def register_face():
    form = RegistrationForm()
    if form.validate_on_submit():
        if form.images.data:
            print("##############################################################\n")
            print(form.images.data)
            images = []
            random_hex = secrets.token_hex(8)
            name = random_hex + form.name.data
            person = Person(name=name)
            db.session.add(person)
            db.session.commit()
            id = Person.query.filter_by(name=name).first().id
            for image in form.images.data:
                image_fn, image_path = save_image(image)
                dataset = Dataset(image_file=image_fn, author=person)
                db.session.add(dataset)
                print(image_path)
                detected_image = faces.detectFace(image_path, image_fn)
                images.append(detected_image)
            db.session.commit()
        flash(f'Congratulations! You have successfully registered the face as {form.name.data}.', 'success')
        return render_template('detected_faces.html', title="Detected Faces", selectedListElement="registerFace", images=images)
    return render_template('register_face.html', title="Register Face", selectedListElement="registerFace", form=form)


@app.route("/faces/recognize", methods=['GET','POST'])
@login_required
def recognize_face():
    return render_template('recognize_face.html', title="Recognize Face", selectedListElement="recognizeFace")


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('login'))


@app.route("/account", methods=['GET','POST'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        current_user.email = form.email.data
        db.session.commit()
        flash(f'Your account has been updated.', 'success')
        return redirect(url_for('account', title='Account'))
    elif request.method == 'GET':
        form.email.data = current_user.email
    return render_template('account.html', title='Account', form=form)


@app.route("/faces/all")
@login_required
def all_faces():
    persons = Person.query.all()
    return render_template('all_faces.html', title='All Faces', selectedListElement="allFaces", persons=persons)


@app.route("/faces/<int:person_id>")
@login_required
def face(person_id):
    person = Person.query.get_or_404(person_id)
    datasets = Dataset.query.filter_by(author=person).all()
    print('###############################################################################')
    print(person)
    print(datasets)
    print('###############################################################################')
    return render_template('face.html', title='Face', datasets=datasets)