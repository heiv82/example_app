from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, ValidationError, Email, EqualTo, Length
from app.models import User, Device


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField("Remember Me")
    submit = SubmitField('Sign In')


class RegistrationDeviceForm(FlaskForm):
    device_EUI = StringField('Device EUI', validators=[DataRequired()])
    device_name = StringField('Device Name', validators=[DataRequired()])
    description = StringField('Description Device', validators=[DataRequired()])
    device_profile_id = StringField('Device Profile ID', validators=[DataRequired()])
    application_id = StringField('Application ID', validators=[DataRequired()])
    application_name = StringField('Application Name', validators=[DataRequired()])
    submit = SubmitField('Register')

    def validate_device_EUI(self, device_eui):
        device = Device.query.filter_by(device_EUI=device_eui.data).first()
        if device is not None:
            raise ValueError('Please check device EUI, this device EUI is already registered.')


class ActivationDeviceForm(FlaskForm):
    devaddrs = StringField(validators=[DataRequired()])
    networksskey = StringField(validators=[DataRequired()])
    appsskey = StringField(validators=[DataRequired()])
    deveui = StringField(validators=[DataRequired()])
    submit = SubmitField()


class RegistrationUserForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    api_token = StringField('API token', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    password_repeat = PasswordField('Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Please use a different username.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValueError('Please use a different email address.')


class EditProfileForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    about_me = TextAreaField('About me', validators=[Length(min=0, max=140)])
    submit = SubmitField('Update')

    def __init__(self, original_username, *args, **kwargs):
        super(EditProfileForm, self).__init__(*args, **kwargs)
        self.original_username = original_username

    def validate_username(self, username):
        if username.data != self.original_username:
            user = User.query.filter_by(username=self.username.data).first()
            if user is not None:
                raise ValidationError('Please use a different username.')


class CreateApplication(FlaskForm):
    description = StringField('Description', validators=[DataRequired()])
    id = StringField('ID Application', validators=[DataRequired()])
    name = StringField('Name Application', validators=[DataRequired()])
    organizationID = StringField('Organization ID', validators=[DataRequired()])
    serviceProfileID = StringField('Service Profile ID', validators=[DataRequired()])
    submit = SubmitField('Create application')


class EditApplication(FlaskForm):
    description = StringField('Description', validators=[DataRequired()])
    id = StringField('ID Application', validators=[DataRequired()])
    name = StringField('Name Application', validators=[DataRequired()])
    organizationID = StringField('Organization ID', validators=[DataRequired()])
    serviceProfileID = StringField('Service Profile ID', validators=[DataRequired()])
    submit = SubmitField('Edit')
    delete = SubmitField('Delete application')


class SearchOneItem(FlaskForm):
    id_item = StringField(validators=[DataRequired()])
    del_id_item = StringField(validators=[DataRequired()])
    submit = SubmitField()
    delete = SubmitField()



