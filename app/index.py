#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @File  : index.py
# @Author: Liaop
# @Date  : 2018-11-19
# @Desc  : 主页


from flask import Blueprint, render_template

index_blue = Blueprint('index', __name__, template_folder='templates')


@index_blue.route('/')
def index():
    return render_template('index.html')

@index_blue.route('/2')
def index2():
    return render_template('index2.html')
