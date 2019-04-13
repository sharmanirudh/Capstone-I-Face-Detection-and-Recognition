import os
import secrets
from PIL import Image
from flask import render_template, url_for, flash, redirect
from app import app
from app import faces
from app.forms import RegistrationForm, LoginForm
from app.models import User, Person, Dataset

@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html')

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

@app.route("/register", methods=['GET','POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        if form.images.data:
            print("##############################################################\n")
            print(form.images.data)
            images = []
            for image in form.images.data:
                image_fn, image_path = save_image(image)
                print(image_path)
                detected_image = faces.detectFace(image_path, image_fn)
                images.append(detected_image)
        flash(f'Congratulations! you are successfully registered as {form.name.data}.', 'success')
        return render_template('detected_faces.html', title="Detected Faces", selectedListElement="registerFace", images=images)
        # return redirect(url_for('recognize'))
    return render_template('register.html', title="Register", selectedListElement="registerFace", form=form)

@app.route("/recognize")
def recognize():
    return render_template('recognize.html', title="Recognize", selectedListElement="recognizeFace")