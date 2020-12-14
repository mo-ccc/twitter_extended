import wtforms

class LoginForm(wtforms.Form):
    email = wtforms.StringField('email', [wtforms.validators.DataRequired(),])
    password = wtforms.PasswordField('password', [wtforms.validators.DataRequired(),])
    
class RegisterForm(wtforms.Form):
    name = wtforms.StringField('name', [wtforms.validators.DataRequired(),])
    email = wtforms.StringField('email', [wtforms.validators.DataRequired(),])
    password = wtforms.PasswordField('password', [wtforms.validators.DataRequired(),])