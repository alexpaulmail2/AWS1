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
    
    return render_template('register.html')
 
@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/login', methods = ['GET','POST'])
def login():
    msg=''
    
    if request.method == "POST":
       username = request.form["username"]
       password = request.form["password"]
       
       cur.execute("SELECT * FROM students WHERE username=%s AND password=%s", (username, password))
       record = cur.fetchone()
       
       if record:
           session['loggedin']=True
           session['username']=record[1]
           return redirect(url_for('home'))
       else:
           msg='Incorrect log in credentials'
    return render_template('index.html', msg=msg)
    
@app.route('/insert', methods = ['get', 'post'])
def insert():
    
    if request.method == 'POST':
        name = request.form['name']
        uname = request.form['uname']
        email = request.form['email']
        pwd = request.form['pwd']
        gender = request.form['optradio']
        address = request.form['address']
        
        cur.execute("INSERT INTO students (name1,username,email,password,gender,address) VALUES (%s,%s,%s,%s,%s,%s)", (name,uname,email,pwd,gender,address))
        conn.commit()
        
        return render_template('index.html')

@app.route('/stds')
def stds():
    cur.execute("SELECT * FROM students")
    value=cur.fetchall()
    return render_template('std-info.html', data=value)

@app.route('/reg')
def reg():
    return render_template('register.html')
       
@app.route('/logout')
def logout():
    session.pop('loggedin', None)
    session.pop('username', None)
    return redirect(url_for('login'))


if __name__ == "__main__":
    app.run(debug=True)
