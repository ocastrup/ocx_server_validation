from abc import ABC

from flask_wtf import Form, FlaskForm
from wtforms import TextField, PasswordField, SelectField, RadioField, SubmitField, FileField, TextAreaField, \
    validators, Flags, HiddenField
from flask_table import Table, Col
from wtforms.validators import DataRequired, EqualTo, Length, InputRequired, ValidationError
from flask_wtf.file import FileField, FileAllowed, FileRequired
from pathlib import Path
import re

# Set your classes here.
ALLOWED_EXTENSIONS = set(['xml', 'ocx'])


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def validate_file(form, field):
    message = 'The model to validate must have a valid extension: ".ocx" or ".xml"'
    if not allowed_file(field.data):
        raise ValidationError(message)


class SelectSchemaForm(FlaskForm):
    file_list = []  # A list for passing the schema version to the form field#
    #    directory = Path(app.config["SCHEMA_PATH"])
    directory = Path('./schema_versions')
    for x in directory.iterdir():
        if x.is_file():
            # Filter out the UnitsML schema
            if x.match('OCX*'):
                # extract the version number from the file name
                name = str(x.name)
                # The schema naming convention is: OCX_Schema_Vxxx.xml
                regx = re.search('V(\d+?)\.', name)
                version = regx.group(1)
                key = 'V' + version
                file_list.append((key, name))  # Tuple of (key,schemafile)
                file_list = sorted(file_list, reverse=True)
    schema = SelectField('Schemas', choices=file_list)
    submit = SubmitField('Load schema')

class UploadOCXForm(FlaskForm):
    pattern = re.compile( '(.*?)\.(ocx|xml)$',re.IGNORECASE)
    ocx = FileField('OCX File', validators=[FileAllowed(['ocx','xml']),FileRequired()])
#    file = FileField('OCX File', [DataRequired(),
#                         validators.regexp('(.*?)\.(ocx|xml)$', re.IGNORECASE,
#                        'The model to validate must have a valid extension: ".ocx" or ".xml"')])
    description = TextAreaField(u'OCX model')
    submit = SubmitField('Validate')


class ItemError(object):
    def __init__(self, line, msg):
        self.line = line
        self.msg = msg

class ErrorTable(Table):
    classes = ['table']
    line = Col('Line num.')
    msg = Col('Error message')

class ItemChange(object):
    def __init__(self, version, author, date, change):
        self.author = author
        self.version = version
        self.date = date
        self.change = change

class ChangeTable(Table):
    classes = ['table']
    author = Col('Author')
    version = Col('Version')
    date = Col('Date')
    change = Col('Description')



