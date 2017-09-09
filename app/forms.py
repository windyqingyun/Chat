from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,SubmitField,BooleanField
from wtforms.validators import required

class LoginForm(FlaskForm):

    name = StringField('username',validators=[required()])
    role = BooleanField('kf')

    password = PasswordField('password',validators=[required()])
    submit = SubmitField('submit')

    def validate_name(self, field):
        if field.data:
            field.data = field.data.strip().lower()


