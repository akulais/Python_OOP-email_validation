from flask import Flask, request, redirect, render_template, session, flash
import re

from mysqlconnection import MySQLConnector

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9\.\+_-]+@[a-zA-Z0-9\._-]+\.[a-zA-Z]*$')

app = Flask(__name__)
app.secret_key = 'ThisIsSecret'
mysql = MySQLConnector('emails')


@app.route('/', methods=['GET'])
def index():
	emails = mysql.fetch("SELECT * FROM emails")
	return render_template('index.html', emails = emails)


@app.route('/create', methods=['POST'])
def create():
	if len(request.form['email']) < 1:
		flash(u"Email cannot be empty!", 'error')
	if len(request.form['password']) < 1:
  		flash(u'Password cannot be blank', 'error')
	if len(request.form['confirm_password']) < 1:
  		flash(u'Confirm password cannot be blank', 'error')
  	if request.form['confirm_password'] != request.form['password']:
  		flash(u'Password and Confirm password do not match', 'error')
  	if not EMAIL_REGEX.match(request.form['email']):
  		flash(u"This is not a valid email Address!", 'error')
  	else:
  		flash(u'The email address you entered "{}" is a VALID email address!  Thank you!'.format(request.form['email']),'true')
  		query = "INSERT INTO emails (email, password, created_at, updated_at) VALUES ('{}', '{}', NOW(), NOW())".format(request.form['email'], request.form['password'])
  	try:
  		query
  		mysql.run_mysql_query(query)
  		return redirect('/')
  	
  	except:
  		return redirect('/')
  		
    # query = "UPDATE friends SET first_name = '{}', last_name='{}', occupation='{}' WHERE id = {}".format(request.form['first_name'], request.form['last_name'], request.form['occupation'], friend_id)
    
    # add a friend to the database!
@app.route('/delete/<id>')
def delete(id):
	mysql.run_mysql_query(("DELETE FROM emails WHERE id = '{}'").format(id))
	return redirect('/')

@app.route('/reset')
def reset():
	session.clear()
	return redirect("/")
app.run(debug=True)

