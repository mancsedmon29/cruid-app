from flask import Flask, render_template, request, redirect
from flask_scss import Scss
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

# My app
app = Flask(__name__)
Scss(app)

# For Database 
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATION'] = False
db = SQLAlchemy(app)

# Data Class ~ Row of Data (Create a Model)
class MyTask(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(100), nullable=False)
    complete = db.Column(db.Integer, default=0)
    created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self) -> str:
        return f"Task {self.id}"


with app.app_context():
    db.create_all()


# Routes to Web Pages
# The Home Page
@app.route('/', methods=['POST', 'GET'])
def index():
    # Add a Task
    if request.method == 'POST':
        current_task = request.form['content']
        if not current_task.strip():  # Check if the task content is empty
            return render_template('index.html', tasks=MyTask.query.order_by(MyTask.created).all(), error="Task content cannot be empty.")
        
        new_task = MyTask(content=current_task)
        try: 
            db.session.add(new_task)
            db.session.commit()
            return redirect('/')
        except Exception as e:
            print(f"Error: {e}")
            return f"ERROR: {e}"

    # Display all current tasks
    tasks = MyTask.query.order_by(MyTask.created).all()
    return render_template('index.html', tasks=tasks)



#https://www.home.com/delete
# Delete an Item
@app.route('/delete/<int:id>')
def delete(id:int):
    delete_task = MyTask.query.get_or_404(id)
    try:
        db.session.delete(delete_task)
        db.session.commit()
        return redirect('/')    
    except Exception as e:
        return f"ERROR: {e}"


# Edit an item
@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id:int):
    task = MyTask.query.get_or_404(id)
    if request.method == "POST":
        task.content = request.form['content']
        try:
            db.session.commit()
            return redirect('/')
        except Exception as e:
            return f"Error: {e}"
    else:
        return render_template('edit.html', task=task)


# Runner and the Debugger
if __name__ == '__main__':
    app.run(debug=True)
