# -*- coding: utf-8 -*-
# all the imports
from __future__ import print_function
import sys
from flask import Flask, request, session, redirect, \
    url_for, abort, render_template, flash, jsonify
from forms import Clusters
from datacollection import generateJson


app = Flask(__name__)
app.secret_key = 'XXXX'

#graph1
@app.route('/senate', methods=['GET'])
def senate():
    return render_template('graph1.html')

#graph2
@app.route('/house', methods=['GET'])
def house():
    return render_template('graph2.html')

#wordmap1
@app.route('/wordmap', methods=['GET'])
def wordmap():
    return render_template('wordmap1.html')

@app.route('/politicAnalyzer', methods=['GET','POST'])
def politicAnalyzer():
    form = Clusters()
    if request.method == 'POST':
        myJson = generateJson(request.form.get('numClusters'),\
            request.form.get('chamber'))
        #print(request.form.get('numClusters'),file=sys.stderr)
        #print(request.form.get('chamber'),file=sys.stderr)
        myJson.gJSON()
        form.formSubmitted = 'True'
        #time.sleep(0.1)
        return render_template('politicAnalyzer.html',form = form,\
            numClusters = request.form.get('numClusters'), chamber = request.form.get('chamber'))

    return render_template('politicAnalyzer.html',form = form)

if __name__ == "__main__":
    app.secret_key = 'super secret key'
    app.run(host='0.0.0.0', port=5000, threaded=True, debug = True)
