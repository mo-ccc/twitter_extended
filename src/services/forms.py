import wtforms

class LoginForm(wtforms.Form):
    email = wtforms.StringField('email', [wtforms.validators.DataRequired(),])
    password = wtforms.PasswordField('password', [wtforms.validators.DataRequired(),])