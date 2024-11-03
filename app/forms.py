from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, FloatField
from wtforms.validators import DataRequired, Length

class LocationForm(FlaskForm):
    location = StringField(
        'Location',
        [DataRequired()]
    )
    submit = SubmitField('Search')

class DataForm(FlaskForm):
    storage_size = FloatField(
        "Storage tank size",
        [DataRequired()]
    )
    roof_size = FloatField(
        "Roof Size",
        [DataRequired()]
    )
    people = FloatField(
        "Number of people",
        [DataRequired()]
    )
    submit = SubmitField('Save')