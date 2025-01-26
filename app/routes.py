from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from .models import User, Task
from .forms import LoginForm, RegisterForm, TaskForm

main = Blueprint('main', __name__)

# Ruta principal (Página de inicio)
@main.route('/')
def index():
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))
    return render_template('index.html')

# Ruta de inicio de sesión
@main.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))  # Redirigir al dashboard si ya está autenticado

    form = LoginForm()

    if form.validate_on_submit():  # Si el formulario es válido al enviarse
        user = User.query.filter_by(username=form.username.data).first()
        if user and check_password_hash(user.password, form.password.data):
            login_user(user)
            return redirect(url_for('main.dashboard'))
        else:
            flash('Nombre de usuario o contraseña no válidos', 'danger')
    else:  # Si hay errores de validación
        for field, errors in form.errors.items():
            for error in errors:
                flash(f"Error in {field}: {error}", 'danger')

    # Si es una solicitud GET o hubo errores, renderizamos el formulario
    return render_template('login.html', form=form)


# Ruta de registro de usuario
@main.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))  # Redirigir al dashboard si ya está autenticado
    
    form = RegisterForm()
    if form.validate_on_submit():
        # Cambiar el método a 'pbkdf2:sha256'
        hashed_password = generate_password_hash(form.password.data, method='pbkdf2:sha256')
        new_user = User(username=form.username.data, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        flash('Cuenta creada exitosamente!')
        return redirect(url_for('main.login'))
    
    return render_template('register.html', form=form)

# Ruta del dashboard (interfaz principal después de iniciar sesión)
@main.route('/dashboard', methods=['GET', 'POST'])
@login_required
def dashboard():
    form = TaskForm()
    tasks = Task.query.filter_by(user_id=current_user.id).all()
    if form.validate_on_submit():
        new_task = Task(
            title=form.title.data,
            description=form.description.data,
            completed=form.completed.data,
            user_id=current_user.id
        )
        db.session.add(new_task)
        db.session.commit()
        flash('Nueva tarea agregada!')
        return redirect(url_for('main.dashboard'))  # Redirigir para mostrar la tarea recién añadida
    return render_template('dashboard.html', form=form, tasks=tasks)

# Ruta de cierre de sesión
@main.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))

@main.route('/edit_task/<int:task_id>', methods=['GET', 'POST'])
@login_required
def edit_task(task_id):
    task = Task.query.get_or_404(task_id)
    if task.user_id != current_user.id:  # Asegurar que el usuario actual es el propietario de la tarea
        flash('Acceso no autorizado', 'danger')
        return redirect(url_for('main.dashboard'))

    form = TaskForm(obj=task)  # Rellenar el formulario con los datos actuales de la tarea
    if form.validate_on_submit():
        task.title = form.title.data
        task.description = form.description.data
        task.completed = form.completed.data
        db.session.commit()
        flash('Tarea actualizada exitosamente!', 'success')
        return redirect(url_for('main.dashboard'))

    return render_template('edit_task.html', form=form)


@main.route('/delete_task/<int:task_id>', methods=['POST'])
@login_required
def delete_task(task_id):
    task = Task.query.get_or_404(task_id)
    if task.user_id != current_user.id:  # Asegurar que el usuario actual es el propietario de la tarea
        flash('Acceso no autorizado', 'danger')
        return redirect(url_for('main.dashboard'))

    db.session.delete(task)
    db.session.commit()
    flash('Tarea eliminada exitosamente!', 'success')
    return redirect(url_for('main.dashboard'))
