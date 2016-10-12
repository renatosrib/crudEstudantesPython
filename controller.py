from flask import Flask, request, flash, url_for, redirect, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///students.sqlite3'
app.config['SECRET_KEY'] = "random string"

db = SQLAlchemy(app)



class students(db.Model):
   id = db.Column('student_id', db.Integer, primary_key = True)
   name = db.Column(db.String(100))
   city = db.Column(db.String(50))
   addr = db.Column(db.String(200)) 
   pin = db.Column(db.String(10))

def __init__(self, name="", city="", addr="",pin=""):
   self.name = name
   self.city = city
   self.addr = addr
   self.pin = pin



@app.route('/')
def show_all():
   return render_template('show_all.html', students = students.query.all() )

@app.route('/edit/<id>', methods = ['GET', 'POST'])
def editar(id):
	#Get student by id
	#student = students.query.get(id)
	student = students.query.get_or_404(id)	
	if request.method == 'POST':
		student.name = request.form['name']
		student.city = request.form['city']
		student.addr = request.form['addr']
		student.pin = request.form['pin']
		db.session.commit()
		return redirect(url_for('show_all'))
	return render_template('edit.html',student = student)

@app.route('/delete/<id>',methods=['GET'])
def remover(id):
	student = students.query.get(id)
	db.session.delete(student)
	db.session.commit()
	flash("O aluno \""+student.name+"\" foi removido com sucesso")
	return redirect(url_for('show_all'))

@app.route('/new', methods = ['GET', 'POST'])
def new():
   if request.method == 'POST':
      if not request.form['name'] or not request.form['city'] or not request.form['addr']:
         flash('Favor preencher todos os campos.', 'error')
      else:
         student = students(name=request.form['name'],city=request.form['city'],
            addr=request.form['addr'],pin=request.form['pin'])
         
         db.session.add(student)
         db.session.commit()
         flash("O aluno \"%s\" foi incluído com sucesso."%student.name)
         return redirect(url_for('show_all'))
   return render_template('new.html')



if __name__ == '__main__':
   db.create_all()
   app.run(debug = True)
