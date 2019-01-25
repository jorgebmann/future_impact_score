#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jan 15 14:53:54 2019

@author: jorge
"""
from flask_wtf import Form
#from wtforms import Form, FloatField, validators, StringField #, DateField
from wtforms import validators, StringField #, DateField
from wtforms.fields.html5 import DateField
from wtforms.widgets import TextArea
#from wtforms_html5 import DateRange
#from wtforms.validators import Length

class InputForm(Form):
    dop = DateField('Publication Date', validators = [validators.InputRequired()])
        #validators.DateRange(max=date.today(), min=(date.today() - timedelta(days=2)))])    
    #dop = DateField('Publication Date', validators=[Required()])
    title = StringField('Title', validators=[validators.InputRequired(), 
                                             validators.Length(max=1000)], widget=TextArea())
    r = StringField(validators=[validators.InputRequired(), 
                                validators.Length(max=3000)], widget=TextArea())

from flask import Flask, render_template
from wtforms import widgets, SelectMultipleField

class MultiCheckboxField(SelectMultipleField):
    widget = widgets.ListWidget(prefix_label=False)
    option_widget = widgets.CheckboxInput()


class SimpleForm(Form):
    #string_of_files = ['one\r\ntwo\r\nthree\r\n']    
    #string_of_files = ['MEDICAL AND HEALTH SCIENCES\r\nBIOLOGICAL SCIENCES\r\nEARTH SCIENCES\r\n\r\nHUMANITIES']
    string_of_files = ['MEDICAL AND HEALTH SCIENCES\nBIOLOGICAL SCIENCES\nEARTH SCIENCES\nSOCIAL SCIENCE AND HUMANITIES']
    #list_of_files = string_of_files[0].split()
    list_of_files = string_of_files[0].rstrip().rsplit('\n')
    # create a list of value/description tuples
    files = [(x, x) for x in list_of_files]
    example = MultiCheckboxField('Label', choices=files)

