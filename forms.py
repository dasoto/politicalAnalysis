# -*- coding: utf-8 -*-
# all the imports
from flask_wtf import Form
from wtforms import TextField,SelectField,RadioField,SubmitField,\
    HiddenField

class Clusters(Form):
    chamber = RadioField(u'Select the chamber:',choices = [(1,'Senate'),(2,'HoR')])
    numClusters = SelectField(u'Cluster Number:', \
        choices=[(2, '2'), (3, '3'), (4, '4'),(5, '5'),(6, '6'),\
            (7, '7'),(8, '8')])
    formSubmitted = HiddenField()
    submit = SubmitField("Send")
