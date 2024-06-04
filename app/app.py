from flask import Flask, request, redirect, url_for, render_template, session
from flask_mysqldb import MySQL



app = Flask(__name__)
app.secret_key = 'abc'

app.config['MYSQL_HOST'] = 'db'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'root'
app.config['MYSQL_DB'] = 'fcds'

mySql = MySQL(app)

@app.route('/login', methods =['GET', 'POST'])
def login():
   
    if request.method == 'POST':
        cur = mySql.connection.cursor()
        username = request.form['username']
        password = request.form['password']
        
        if username == 'admin' and password == 'admin':
            return redirect(url_for('admin'))
        
        elif cur.execute(f'SELECT * FROM Login WHERE UserName = "{username}" AND password = "{password}"'):
            user = cur.fetchone()
            if user:
                session['username'] = str(user[0])
                if 'username' in session:
                    UserName = session['username']    
                    cur.execute(f"SELECT * FROM students WHERE UserName = {UserName}")
                    std =  cur.fetchall()
                    return student(std)
       
        else:
            return redirect(url_for('not_found')) 
                  
    return render_template('login.html')




@app.route('/', methods=['GET', 'POST'])
def index():  
    return render_template('login.html')


@app.route('/admin')
def admin():
    cur = mySql.connection.cursor()
    cur.execute('SELECT * FROM students')
    data = cur.fetchall()
    cur.close()
    return render_template('admin.html', data=data)




@app.route('/student', methods=['GET', 'POST'])
def student(std):
    cur = mySql.connection.cursor()
    data = std
    cur.close()
    return render_template('student.html', data=data)
    
        


@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        cur = mySql.connection.cursor()
        name = request.form['name']
        id = request.form['id']
        cgpa = request.form['cgpa']
        credit_hours = request.form['credits']
        usr = request.form['username']
        passw = request.form['password']
        cur = mySql.connection.cursor()
        cur.execute(f'SELECT * FROM students WHERE ID = {id} ')
        
        if cur.execute(f'SELECT * FROM Login WHERE UserName = {usr} ') or cur.execute(f'SELECT * FROM students WHERE ID = {id} '):
            return redirect(url_for('error_add'))
   
        else:
            cur = mySql.connection.cursor()
            cur.execute(f"INSERT INTO students (ID, Name, CGPA, Credit_Hours, UserName) VALUES ('{id}', '{name}', '{cgpa}', '{credit_hours}', '{usr}')")
            cur.execute(f"INSERT INTO login (UserName, password) VALUES ('{usr}', '{passw}')")
            mySql.connection.commit()
            return redirect(url_for('admin'))
    return render_template('add.html')





@app.route('/delete', methods = ['GET', 'POST'])
def delete():
    if request.method == 'POST':
        cur = mySql.connection.cursor()
        username = request.form['username']
        cur = mySql.connection.cursor()
        cur.execute(f'SELECT * FROM students WHERE UserName = {username} ')
        check_std = cur.fetchone()
        
        if check_std:
            cur = mySql.connection.cursor()
            cur.execute(f'DELETE FROM students WHERE UserName = {username}')
            mySql.connection.commit()
            cur.close()
            return redirect(url_for('admin'))
        else:
            return redirect(url_for('error_delete'))
    return render_template('delete.html')




@app.route('/update', methods = ['GET', 'POST'])
def update():

    if request.method == 'POST':
        cur = mySql.connection.cursor()            
        cur = mySql.connection.cursor()
        name = request.form['name']
        id = request.form['id']
        cgpa = request.form['cgpa']
        credit_hours = request.form['credits']
        user = request.form['username']
        passw = request.form['password']
        cur = mySql.connection.cursor()
        cur.execute(f"UPDATE login SET UserName = '{user}', password = '{passw}' WHERE UserName = '{user}'")
        cur.execute(f"UPDATE students SET ID = '{id}', Name = '{name}', CGPA = '{cgpa}', Credit_Hours = '{credit_hours}', UserName = '{user}' WHERE ID = '{id}'")
        mySql.connection.commit()
        cur.close()
        return redirect(url_for('admin'))
    return render_template('Update.html')



           
@app.route('/not_found', methods=['GET', 'POST'])
def not_found():
    return render_template('usr_not_found.html')



@app.route('/error_found_similar_usr', methods=['GET', 'POST'])
def error_found_similar_usr():
    if request.method == 'POST':
        return redirect(url_for('add'))
    return render_template('error_found_similar_usr.html') 

@app.route('/error_add', methods = ['GET', 'POST'])
def error_add():
    if request.method == 'POST':
        return redirect(url_for('add'))
    return render_template('error_add.html') 


         
@app.route('/error_update', methods = ['GET', 'POST'])
def error_update():
    if request.method == 'POST':
        return redirect(url_for('add'))
    return render_template('error_update.html')     



    
if __name__ == '__main__':
    app.run(host='0.0.0.0',port='5000',debug=True)
    
