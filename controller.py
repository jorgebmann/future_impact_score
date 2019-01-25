#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jan 15 14:25:54 2019

@author: jorge
"""

from flask import Flask, render_template, request
#from compute import compute
from mk_prediction import mk_prediction
from model import InputForm, SimpleForm

app = Flask(__name__)

app.secret_key = b'xb7\x8a\xcb\xfaa\xb7\xa7:\xe1\x05\xe3-i|\xa5/'

@app.route('/, methods=['GET', 'POST'])

def index():
    form = InputForm(request.form)
    check = SimpleForm()
    if request.method == 'POST' and form.validate():
        r = form.r.data
        s = mk_prediction(r)
    else:
        s = None
    if check.validate_on_submit():
        print(check.example.data)
    else:
        print(check.errors)

    return render_template("view.html", form=form, s=s, check=check)

if __name__ == '__main__':
    app.run(debug=False)
