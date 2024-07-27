from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import desc
from datetime import datetime
from flask_login import LoginManager, UserMixin, login_user, current_user, logout_user, login_required
from pytz import timezone
from flask_migrate import Migrate
import os 


app = Flask(__name__, static_url_path='/static')
app.config['SECRET_KEY'] = 'Language'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'  # Example for SQLite database
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

db = SQLAlchemy(app)
migrate = Migrate(app, db)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
UPLOAD_FOLDER = 'static/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER



class Post_hs(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(20), nullable=False)
    description = db.Column(db.String(200), nullable=False)
    file = db.Column(db.String(200), nullable=False)
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    date = db.Column(db.String(200), nullable=False, default=datetime.now(timezone('Asia/Seoul')))
    author = db.relationship('User', backref='posts_hs', lazy=True)
    
class Post_sj(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(20), nullable=False)
    description = db.Column(db.String(200), nullable=False)
    file = db.Column(db.String(200), nullable=False)
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    date = db.Column(db.String(200), nullable=False, default=datetime.now(timezone('Asia/Seoul')))
    author = db.relationship('User', backref='posts_sj', lazy=True)
    
class Post_ju(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(20), nullable=False)
    description = db.Column(db.String(200), nullable=False)
    file = db.Column(db.String(200), nullable=False)
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    date = db.Column(db.String(200), nullable=False, default=datetime.now(timezone('Asia/Seoul')))
    author = db.relationship('User', backref='posts_ju', lazy=True)
    

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    def __repr__(self):
        return f"User('{self.username}')"

    
with app.app_context():
    db.create_all()


 
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))



@app.route("/")
def home():
    return render_template('main.html')

@app.route("/hs")
@login_required
def hs():
    page = request.args.get('page', 1, type=int)  # Get the page number from the URL, default to 1
    per_page = 5
    posts_hs = Post_hs.query.order_by(desc(Post_hs.id)).paginate(page=page, per_page=per_page, error_out=False)
    return render_template("hs.html", posts_hs=posts_hs)

@app.route("/sj")
@login_required
def sj():
    page = request.args.get('page', 1, type=int)  # Get the page number from the URL, default to 1
    per_page = 5
    posts_sj = Post_sj.query.order_by(desc(Post_sj.id)).paginate(page=page, per_page=per_page, error_out=False)
    return render_template("sj.html", posts_sj=posts_sj)

@app.route("/ju")
@login_required
def ju():
    page = request.args.get('page', 1, type=int)  # Get the page number from the URL, default to 1
    per_page = 5
    posts_ju = Post_ju.query.order_by(desc(Post_ju.id)).paginate(page=page, per_page=per_page, error_out=False)
    return render_template("ju.html", posts_ju=posts_ju)

@app.route('/hs/new', methods=['GET', 'POST'])
@login_required
def hs_new_post():
    if request.method=='POST':
        title = request.form["title"]
        description = request.form["description"]
        file = request.files['file']
        dt_with_ms = datetime.now(timezone('Asia/Seoul'))
        formatted_dt = dt_with_ms.strftime('%Y-%m-%d %H:%M:%S')
        if file:
            filename = file.filename
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

            # Create a new GalleryItem object
            new_item = Post_hs(title=title, description=description, file=filename, 
                               author_id=current_user.id, date=formatted_dt)
            db.session.add(new_item)
            db.session.commit()

            return redirect(url_for('hs'))

    return render_template('hs_new_post.html')

@app.route('/sj/new', methods=['GET', 'POST'])
@login_required
def sj_new_post():
    if request.method=='POST':
        title = request.form["title"]
        description = request.form["description"]
        file = request.files['file']
        dt_with_ms = datetime.now(timezone('Asia/Seoul'))
        formatted_dt = dt_with_ms.strftime('%Y-%m-%d %H:%M:%S')
        if file:
            filename = file.filename
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

            # Create a new GalleryItem object
            new_item = Post_sj(title=title, description=description, file=filename, 
                               author_id=current_user.id, date=formatted_dt)
            db.session.add(new_item)
            db.session.commit()

            return redirect(url_for('sj'))

    return render_template('sj_new_post.html')

@app.route('/ju/new', methods=['GET', 'POST'])
@login_required
def ju_new_post():
    if request.method=='POST':
        title = request.form["title"]
        description = request.form["description"]
        file = request.files['file']
        dt_with_ms = datetime.now(timezone('Asia/Seoul'))
        formatted_dt = dt_with_ms.strftime('%Y-%m-%d %H:%M:%S')
        if file:
            filename = file.filename
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

            # Create a new GalleryItem object
            new_item = Post_ju(title=title, description=description, file=filename, 
                               author_id=current_user.id, date=formatted_dt)
            db.session.add(new_item)
            db.session.commit()

            return redirect(url_for('ju'))

    return render_template('ju_new_post.html')


@app.route('/hs/post/<int:post_id>', methods=['GET'])
@login_required 
def view_post_hs(post_id):
    post = Post_hs.query.get_or_404(post_id)
    return render_template('view_post_hs.html', post=post)

@app.route('/hs/post/<int:post_id>/edit', methods=['GET','POST'])
@login_required  
def edit_post_hs(post_id):
    post = Post_hs.query.get_or_404(post_id)
    
    if request.method == 'POST':
        if post.author == current_user:
            post.title = request.form['title']
            post.description = request.form['description']
            file = request.files['file']
            if file:
                filename = file.filename
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                post.file = filename
            db.session.commit()
            return redirect(url_for('hs'))
        else:
            flash("You are not authorized to edit this post.",'danger')
            return redirect(url_for('edit_post_hs', post_id=post_id))

    return render_template('edit_post_hs.html', post=post)

@app.route('/hs/post/<int:post_id>/delete', methods=['GET','POST'])
@login_required  
def delete_post_hs(post_id):
    post = Post_hs.query.get_or_404(post_id)
    
    if post.author == current_user:
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], post.file)
        if os.path.exists(file_path):
            os.remove(file_path)
        db.session.delete(post)
        db.session.commit()
        return redirect(url_for('hs'))
    else:
        flash("You are not authorized to delete this post.",'danger')
        return redirect(url_for('edit_post_hs', post_id=post_id))

@app.route('/sj/post/<int:post_id>/delete', methods=['GET','POST'])
@login_required  
def delete_post_sj(post_id):
    post = Post_sj.query.get_or_404(post_id)
    
    if post.author == current_user:
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], post.file)
        if os.path.exists(file_path):
            os.remove(file_path)
        db.session.delete(post)
        db.session.commit()
        return redirect(url_for('sj'))
    else:
        flash("You are not authorized to delete this post.",'danger')
        return redirect(url_for('edit_post_sj', post_id=post_id))
    
@app.route('/ju/post/<int:post_id>/delete', methods=['GET','POST'])
@login_required  
def delete_post_ju(post_id):
    post = Post_ju.query.get_or_404(post_id)
    
    if post.author == current_user:
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], post.file)
        if os.path.exists(file_path):
            os.remove(file_path)
        db.session.delete(post)
        db.session.commit()
        return redirect(url_for('ju'))
    else:
        flash("You are not authorized to delete this post.",'danger')
        return redirect(url_for('edit_post_ju', post_id=post_id))
    



@app.route('/sj/post/<int:post_id>', methods=['GET'])
@login_required 
def view_post_sj(post_id):
    post = Post_sj.query.get_or_404(post_id)
    return render_template('view_post_sj.html', post=post)

@app.route('/sj/post/<int:post_id>/edit', methods=['GET', 'POST'])
@login_required  
def edit_post_sj(post_id):
    post = Post_sj.query.get_or_404(post_id)
    
    if request.method == 'POST':
        if post.author == current_user:
            post.title = request.form['title']
            post.description = request.form['description']
            file = request.files['file']
            if file:
                filename = file.filename
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                post.file = filename
            db.session.commit()
            return redirect(url_for('sj'))
        else:
            flash("You are not authorized to edit this post.",'danger')
            return redirect(url_for('edit_post_sj', post_id=post_id))

          # Redirect to the main posts listing

    return render_template('edit_post_sj.html', post=post)

@app.route('/ju/post/<int:post_id>', methods=['GET'])
@login_required 
def view_post_ju(post_id):
    post = Post_ju.query.get_or_404(post_id)
    return render_template('view_post_ju.html', post=post)

@app.route('/ju/post/<int:post_id>/edit', methods=['GET', 'POST'])
@login_required  
def edit_post_ju(post_id):
    post = Post_ju.query.get_or_404(post_id)
    
    if request.method == 'POST':
        if post.author == current_user:
            post.title = request.form['title']
            post.description = request.form['description']
            file = request.files['file']
            if file:
                filename = file.filename
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                post.file = filename
            db.session.commit()
            return redirect(url_for('ju'))
        else:
            flash("You are not authorized to edit this post.",'danger')
            return redirect(url_for('edit_post_ju', post_id=post_id))

    return render_template('edit_post_ju.html', post=post)



@app.route('/login', methods=['GET','POST'])
def login():
    if request.method=='POST':
        username= request.form["username"]
        password= request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and user.password == password:
            login_user(user)
            next_page = request.args.get('next')
            return redirect(next_page or url_for('home'))
        else:
            flash('Login unsuccessful. Please check your username and password.', 'danger')
    return render_template('login.html')
    

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))
    
    

if __name__ == '__main__':
    app.run(port=5500, debug=True)

