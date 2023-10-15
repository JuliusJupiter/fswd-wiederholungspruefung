from flask_wtf import FlaskForm
from wtforms.fields import BooleanField, HiddenField, SelectField, StringField, SubmitField, PasswordField
from wtforms.validators import InputRequired, Length

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired(), Length(min=5)])
    password = PasswordField('Password', validators=[InputRequired(), Length(min=5)])
    submit = SubmitField('Login')

class  RegisterForm(FlaskForm):    
    nutzername = StringField(validators=[InputRequired(), Length(min=5)]) 
    passwort = PasswordField(validators=[InputRequired(), Length(min=5)])
    submit = SubmitField('Register')    

class CreateTodoForm(FlaskForm):
    description = StringField(validators=[InputRequired(), Length(min=5)])
    submit = SubmitField('Create')

class TodoForm(FlaskForm):
    method = HiddenField()
    id = HiddenField()
    complete = BooleanField()
    description = StringField(validators=[InputRequired()])
    list_id = SelectField(coerce=int, choices=[], validate_choice=False)
    submit = SubmitField('Update')