import os
import secrets
from PIL import Image
from flask import url_for,current_app
from flask_mail import Message
from flaskblog import mail
def save_pic(picture):
	random = secrets.token_hex(8)
	_, f_ext =os.path.splitext(picture.filename)
	pic_name = random + f_ext
	pic_path = os.path.join(current_app.root_path,"static/profile_pics",pic_name)
	output_size = (125,125)
	i = Image.open(picture)
	i.thumbnail(output_size)
	i.save(pic_path)
	return pic_name

def send_reset_email(user):
	token = user.get_reset_token()
	msge = Message("Password Reset Request",
	 	sender = 'mohamedraees2@gmail.com',
	 	recipients = [user.email])
	msge.body = f'''To reset your password, visit the following links:
{url_for('user.reset_token', token = token, _external = True)}

If you did not
'''
	mail.send(msge)