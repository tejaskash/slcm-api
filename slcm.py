from flask import Flask,render_template,request,Response
from slcm_scrape import getDetails
from html2json import Attendance2JSON,Internals2JSON
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
from pyvirtualdisplay import Display
from json import dumps

app = Flask(__name__)


@app.route("/")
def hello():
    return render_template("index.html")

@app.route("/displaySLCM",methods=["POST"])
def getAttendance():
    print(request.form['username'],request.form['password'])
    AttendanceHTML,MarksHTML = getDetails(request.form['username'],request.form['password'])
    print (MarksHTML)
    marksJSON = Internals2JSON(MarksHTML)
    attendanceJSON = Attendance2JSON(AttendanceHTML)
    return render_template("index.html",attd=attendanceJSON,marks=marksJSON)

@app.route("/api/v1/get",methods=["POST"])
def handleRequest():
    request_body = dict(request.get_json())
    username = request_body['request']['credentials']['username']
    password = request_body['request']['credentials']['password']
    tpe =request_body['request']['type']
    if(tpe == "ATTENDANCE"):
        attd,_=getDetails(username,password)
        jsn = Attendance2JSON(attd)
        resp = Response(jsn,200)
        resp.headers['Content-Type'] = "application/json"
        return resp
    elif(tpe == "MARKS"):
        _,marks = getDetails(username,password)
        jsn = Internals2JSON(marks)
        resp = Response(jsn,200)
        resp.headers['Content-Type'] = "application/json"
        return resp
    elif(tpe == "ALL"):
        attd,marks = getDetails(username,password)
        jsn1 = Internals2JSON(marks)
        jsn2 = Attendance2JSON(attd)
        jsn = dict()
        jsn['marks'] = jsn1
        jsn['attendance'] = jsn2
        resp = Response(dumps(jsn),200)
        resp.headers['Content-Type'] = "application/json"
        return resp
    else:
        resp = Response("Error",501)
        return resp
    return "Error Occured"

if __name__ == "__main__":
    app.run("0.0.0.0",port=5000,debug=True)
