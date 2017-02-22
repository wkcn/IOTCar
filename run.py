from flask import Flask, request, jsonify, render_template
import pymysql
from carIOT import app

if __name__ == '__main__':
    # app.run(debug=True, host = '45.32.48.44', port = 5000)
    #app.run(debug=True, host = '127.0.0.1', port = 5000)
    app.run(debug=True, host = '0.0.0.0', port = 5000)
    # app.run(debug=False, port = 80, host = '45.32.56.30')
