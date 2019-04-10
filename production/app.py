import os
import secrets
import faces
from PIL import Image
from flask import Flask, render_template, url_for, flash, redirect
from flask_sqlalchemy import SQLAlchemy
from forms import RegistrationForm, LoginForm
app = Flask(__name__)

app.config['SECRET_KEY'] = '61c5219a46120c351894df0dcd681761'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'

db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    name = db.Column(db.String(30), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    images = db.relationship('Dataset', backref='author', lazy=True)

    def __repr__(self):
        return f"User('{self.id}', '{self.username}', '{self.email}', '{self.name}', '{self.images}')"

class Dataset(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    image_file = db.Column(db.String(20), nullable=False)

    def __repr__(self):
        return f"Dataset('{self.id}', '{self.user_id}', '{self.image_file}')"

@app.route("/")
@app.route("/home")
def home():
    return render_template('register.html', title="Register", selectedListElement="registerFace", form=form)

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

if __name__ == '__main__':
    app.run()