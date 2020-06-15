#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jan 15 14:53:54 2019

@author: Jörg Bahlmann
"""
from flask_wtf import Form
from wtforms import validators, StringField #, DateField
from wtforms.fields.html5 import DateField
from wtforms.widgets import TextArea

class InputForm(Form):
    dop = DateField('Publication Date', validators = [validators.InputRequired()])
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
    string_of_files = ['MEDICAL AND HEALTH SCIENCES\nBIOLOGICAL SCIENCES\nEARTH SCIENCES\nSOCIAL SCIENCE AND HUMANITIES']
    list_of_files = string_of_files[0].rstrip().rsplit('\n')
    files = [(x, x) for x in list_of_files]
    example = MultiCheckboxField('Label', choices=files)

