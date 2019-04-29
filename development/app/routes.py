import os
import secrets
from PIL import Image
from flask import render_template, url_for, flash, redirect, request, make_response, send_from_directory
from app import app, db, bcrypt
from app import faces
from app.forms import DetectionForm, RegistrationForm, RecognizeForm, LoginForm, SignUpForm, UpdateAccountForm
from app.models import User, Person, Dataset
from flask_login import login_user, current_user, logout_user, login_required

static_folder_path = './app/static/'

def save_image_to_user_images(form_image_name, to_be_saved_image):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_image_name)
    image_fn = random_hex + f_ext
    image_path = os.path.join(app.root_path, 'static/user_images/', image_fn)

    output_size = (500, 500)
    i = to_be_saved_image
    i.thumbnail(output_size)
    i.save(image_path)
    
    return image_fn, image_path

def save_image_to_dataset(dir_name, form_image_name, to_be_saved_image):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_image_name)
    image_fn = dir_name + '_' + random_hex + f_ext
    try:
        os.makedirs(static_folder_path + 'images/dataset/' + dir_name)
    except FileExistsError:
        print("directory already exists")
        pass
    image_path = os.path.join(app.root_path, 'static/images/dataset/' + dir_name, image_fn)

    output_size = (200, 200)
    i = to_be_saved_image
    i.thumbnail(output_size)
    i.save(image_path)
    
    return image_fn, image_path


@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')


# @app.route('/', methods=['GET','POST'])
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


@app.route("/faces/detect", methods=['GET','POST'])
@login_required
def detect_faces():
    form = DetectionForm()
    if form.validate_on_submit():
        if form.images.data:
            print("##############################################################\n")
            print(form.images.data)
            images = []
            for image in form.images.data:
                detected_image = faces.detectFaces(image)
                image_fn, image_path = save_image_to_user_images(form_image_name=image.filename, 
                    to_be_saved_image=detected_image)
                print(image_path)
                images.append(image_fn)
        flash(f'Detected faces have been marked.', 'success')
        return render_template('detected_faces.html', title="Detected Faces", selectedListElement="detectFaces", images=images)
    return render_template('detect_faces.html', title="Detect Face", selectedListElement="detectFaces", form=form)


@app.route("/faces/register", methods=['GET','POST'])
@login_required
def register_face():
    form = RegistrationForm()
    if form.validate_on_submit():
        if form.images.data:
            print("##############################################################\n")
            print(form.images.data)
            images = []
            # random_hex = secrets.token_hex(8)
            name = form.name.data
            person = Person(name=name)
            db.session.add(person)
            db.session.commit()
            id = Person.query.filter_by(name=name).first().id
            has_at_least_one_image_with_single_face = False
            for image in form.images.data:
                # TODO see if there is one only one face in the image (because suppose if there are 
                # 2 persons in the image and the 2nd one tries to recognize himself then if id folder
                # of 1st one comes first than the 2nd one's id folder, 2nd one will be recognized as
                # 1st person as the photo is in 1st person's id folder)
                face_image = faces.hasSingleFace(image)
                if face_image is not None:
                    has_at_least_one_image_with_single_face = True
                    image_fn, image_path = save_image_to_dataset(dir_name=str(id), 
                        form_image_name=image.filename, to_be_saved_image=face_image)
                    dataset = Dataset(image_file=image_fn, author=person)
                    db.session.add(dataset)
                    print(image_path)
                    images.append(image_fn)
            if has_at_least_one_image_with_single_face is True:
                db.session.commit()
                faces.make_new_face_encodings()
                flash(f'Congratulations! Successfully registered the face as {form.name.data}. Try recognizing {form.name.data}.', 'success')
                return redirect(url_for('recognize_faces', title='Recognize Faces'))
            else:
                flash(f'{form.name.data} not registered as there was no face in the image. Try providing different images.', 'danger')
                return render_template('register_face.html', title="Register Face", selectedListElement="registerFace", form=form)
    return render_template('register_face.html', title="Register Face", selectedListElement="registerFace", form=form)


@app.route("/faces/recognize", methods=['GET','POST'])
@login_required
def recognize_faces():
    form = RecognizeForm()
    if form.validate_on_submit():
        if form.images.data:
            print("##############################################################\n")
            print(form.images.data)
            images = []
            for image in form.images.data:
                recognized_image = faces.recognizeFaces(image)
                image_fn, image_path = save_image_to_user_images(form_image_name=image.filename, 
                    to_be_saved_image=recognized_image)
                print(image_path)
                images.append(image_fn)
        flash(f'Recognized faces have been marked.', 'success')
        return render_template('recognized_faces.html', title="Recognized Faces", selectedListElement="recognizeFace", images=images)
    return render_template('recognize_faces.html', title="Recognize Face", selectedListElement="recognizeFace", form=form)


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


@app.route('/manifest.json')
def manifest():
    return send_from_directory('static', 'manifest.json')


@app.route('/sw.js')
def service_worker():
    response = make_response(send_from_directory('static', 'sw.js'))
    response.headers['Cache-Control'] = 'no-cache'
    return response