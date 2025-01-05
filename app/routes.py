from flask import Blueprint, jsonify, request, render_template, redirect, url_for, session, flash
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from .models import User

main = Blueprint('main', __name__)


@main.route('/', methods=['GET'])
def home():
    if 'loggedin' in session:
        page = request.args.get('page', 1, type=int)
        per_page = 5
        users = User.query.paginate(page=page, per_page=per_page)
        return render_template('index.html', username=session['username'], role=session['role'], users=users)
    else:
        flash('Please log in to access this page.', 'warning')
        return redirect(url_for('main.login'))

@main.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirm_password']
        
        if password == confirm_password:
            existing_email = User.query.filter_by(email=email).first()
            existing_username = User.query.filter_by(username=username).first()
            
            if existing_email:
                flash('Email already exists!', 'danger')
                return render_template('register.html')
            
            if existing_username:
                flash('Username already exists!', 'danger')
                return render_template('register.html')
            
            hashed_password = generate_password_hash(password)
            new_user = User(username=username, email=email, hashed_password=hashed_password)
            db.session.add(new_user)
            db.session.commit()

            flash('You have successfully registered! Please log in.', 'success')
            return redirect(url_for('main.login'))
        else:
            flash('Passwords do not match!', 'danger')
            return render_template('register.html')
        
    return render_template('register.html')

@main.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = User.query.filter_by(username=username).first()

        if user and check_password_hash(user.hashed_password, password):
            session['loggedin'] = True
            session['id'] = user.id
            session['username'] = user.username
            session['role'] = user.role
            flash('Login successful!', 'success')
            return redirect(url_for('main.home'))
        else:
            flash('Invalid email or password!', 'danger')

    return render_template('login.html')


@main.route('/logout', methods=['POST'])
def logout():
    session.clear()
    flash('You have been logged out.', 'success')
    return redirect(url_for('main.login'))

@main.route('/create', methods=['GET', 'POST'])
def create():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirm_password']
        
        if password == confirm_password:
            existing_email = User.query.filter_by(email=email).first()
            existing_username = User.query.filter_by(username=username).first()
            
            if existing_email:
                flash('Email already exists!', 'danger')
                return render_template('create.html')
            
            if existing_username:
                flash('Username already exists!', 'danger')
                return render_template('create.html')
            
            hashed_password = generate_password_hash(password)
            new_user = User(username=username, email=email, hashed_password=hashed_password)
            db.session.add(new_user)
            db.session.commit()

            flash(f'You have successfully added a user with username: {new_user.username}', 'success')
            return redirect(url_for('main.create'))
        else:
            flash('Invalid confirmation password!', 'danger')
            return render_template('create.html')
        
    return render_template('create.html')

@main.route('/edit/<int:user_id>', methods=['GET', 'POST'])
def edit_user(user_id):
    user = User.query.get(user_id)
    if not user:
        flash('User not found.', 'danger')
        return redirect(url_for('main.home'))

    if request.method == 'POST':
        user.username = request.form['username']
        user.email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirm_password']
        
        if password:
            if password == confirm_password:
                user.hashed_password = generate_password_hash(password)
            else:
                flash('Passwords do not match!', 'danger')
                return render_template('edit.html', user=user)
        
        db.session.commit()
        flash(f'User {user.username} has been updated.', 'success')
        return redirect(url_for('main.home'))

    return render_template('edit.html', user=user)

@main.route('/delete_all', methods=['POST']) #html tidak support method delete secara langsung jadi make post
def delete_all_users():
    users = User.query.all()
    if not users:
        flash('Tidak ada data user', 'warning')
        return redirect(url_for('main.home'))

    for user in users:
        db.session.delete(user)
    db.session.commit()
    flash('Semua data pengguna telah dihapus.', 'success')
    return redirect(url_for('main.login'))



@main.route('/delete/<int:user_id>', methods=['POST'])
def delete_user(user_id):
    user = User.query.get(user_id)
    if user:
        db.session.delete(user)
        db.session.commit()
        flash(f'User {user.username} has been deleted.', 'success')
        if user.id == session.get('id'):
            session.clear()
            return redirect(url_for('main.login'))
    else:
        flash('User not found.', 'danger')
    return redirect(url_for('main.home'))
