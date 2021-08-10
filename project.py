from flask import Flask, redirect, url_for, request, render_template, flash
from werkzeug.utils import secure_filename
from flask_wtf import FlaskForm
from flask_wtf.file import FileRequired, FileField, FileAllowed
from wtforms import TextField, SubmitField, SelectField, StringField, FloatField, RadioField, validators, ValidationError
import os
import grid
from flask_mail import Mail, Message
from wtforms_components import ColorField

app = Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'hh5094266@gmail.com'
app.config['MAIL_PASSWORD'] = 'Hhacker@12'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
app.config['MAIL_DEFAULT_SENDER']='hh5094266@gmail.com'

mail = Mail(app)

app.secret_key = 'development key'
basedir = os.path.abspath(os.path.dirname(__file__))
UPLOADED_PHOTOS_DEST = os.path.join(basedir, 'static', 'uploads')

width_choices=[('1','large'),('2', 'medium'),('3', 'small')]
class ContactForm(FlaskForm):
	email = TextField("Email:",[validators.DataRequired("Please enter your email address."),validators.Email("Please enter valid email address.")])
	photo= FileField('Upload picture:',validators=[FileRequired(), FileAllowed(['jpg', 'png', 'jpeg'], "Only Images are allowed.")])
	gridWidth= SelectField("grid width:",choices= width_choices)
	lineWidth= FloatField("Line width:")
	select= RadioField("Do you want to receive mail with picture? (If you wish to preview image first press No and proceed.)",choices=[('Y',"Yes"),('N',"No")])
	color = ColorField("Color:")
	submit = SubmitField("Send")
	
class ReviewForm(FlaskForm):
	select= RadioField("Do you want to receive mail with picture now?", choices=[('Y',"Yes"),('N',"No")])
	rate= RadioField("Rate us",choices=[("one","1"),("two","2"),("three","3"),("four","4"),("five","5")])
	submit = SubmitField("Send")

def send_email(form_data,filename):
    msg= Message('Hello', sender = 'hh5094266@gmail.com', recipients = [form_data])
    msg.body= 'Final Image. PFA'
    with app.open_resource(os.path.join(UPLOADED_PHOTOS_DEST,filename)) as fp:
        msg.attach(filename,"image/png",fp.read())
        mail.send(msg)
        print ('Sent')

#No caching at all for API endpoints.
@app.after_request
def add_header(response):
    response.headers['X-UA-Compatible'] = 'IE=Edge,chrome=1'
    response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, post-check=0, pre-check=0, max-age=0, public'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '-1'
    return response

@app.route('/display', methods=["POST", "GET"])
def display():
	reviewform=ReviewForm()
	if(request.method == "POST"):
		if(reviewform.select.data=="Y"):
			send_email(request.args.get('email'),request.args.get('dest'))
			return 'The mail has been sent. Please do visit again.'
		return 'Thankyou for visiting!'
	return render_template('result.html', email=request.args.get('email'), dest=request.args.get('dest'), select=request.args.get('select'), reviewform=reviewform)

@app.route('/', methods=["POST","GET"])
def upload():
	return redirect(url_for('upload_file'))

@app.route('/uploader', methods=["POST","GET"])
def upload_file():
	
	form=ContactForm()
	
	if request.method == 'POST':
		if form.validate_on_submit():

			# for subfield in form.select:
			# 	print(subfield)
			# 	print(subfield.label)
			
			f = form.photo.data
			try:
				os.remove(os.path.join(UPLOADED_PHOTOS_DEST,secure_filename(f.filename)))
				print('deleted file')
			except:
				print('new file')
			finally:
				f.save(os.path.join(UPLOADED_PHOTOS_DEST, secure_filename(f.filename)))
				grid.makeGrid(gap=dict(width_choices).get(form.gridWidth.data), color=str(form.color.data), filename=f.filename, stroke=int(form.lineWidth.data))
				
				if form.select.data=="Y":
					send_email(form.email.data,f.filename)
				return redirect(url_for('display', email=form.email.data, select=form.select.data, dest=f.filename))
		flash('All fields are required.')
		
		return render_template('upload.html',form=form)
			
	else:
		return render_template('upload.html',form=form)

if __name__ == '__main__':
   app.run(debug=True)
