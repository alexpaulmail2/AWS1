# -*- coding: utf-8 -*-
"""
Created on Sat Jul 25 12:02:51 2020

@author: hp
"""

from flask import Flask, render_template, request, flash, redirect, url_for, jsonify, session 
from flask import Response,send_file

import pymysql

conn = pymysql.connect(
        host= 'demo.cntrljtsuokh.us-east-1.rds.amazonaws.com', #endpoint link
        port = 3306, # 3306
        user = 'admin', # admin
        password = 'adminadmin', #adminadmin
        db = 'demo_db', #demo
        )

cur=conn.cursor()

app = Flask(__name__)
app.secret_key = 'hello'

@app.route('/')
def index():
    
    return render_template('index.html')
 
@app.route('/login', methods = ['GET','POST'])
def login():
    msg=''
    
    if request.method == "POST":
       username = request.form["username"]
       password = request.form["password"]
       
       cur.execute("SELECT * FROM admin1 WHERE username=%s AND password1=%s", (username, password))
       record = cur.fetchone()
       
       if record:
           session['loggedin']=True
           session['username']=record[1]
           return redirect(url_for('stds'))
       else:
           msg='Incorrect log in credentials'
    return render_template('index.html', msg=msg)
    
@app.route('/stds')
def stds():
    cur.execute("SELECT * FROM students")
    value=cur.fetchall()
    return render_template('std-info.html', data=value)
    
    
@app.route('/logout')
def logout():
    session.pop('loggedin', None)
    session.pop('username', None)
    return redirect(url_for('login'))


if __name__ == "__main__":
    app.run(port=7000,debug=True)
