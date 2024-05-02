from werkzeug.utils import secure_filename
import os
from flask import Flask, render_template, request, redirect, url_for
import mysql.connector

app = Flask(__name__)

# Database configuration
db_host = 'localhost'
db_user = 'root'
db_password = ''  # Replace with your MySQL password if any
db_name = 'EVSFlask'

# Function to establish database connection
# Function to establish database connection
def get_db_connection():
    return mysql.connector.connect(
        host=db_host,
        user=db_user,
        password=db_password,
        database=db_name
    )