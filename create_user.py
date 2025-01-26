from app import create_app, db
from app.models import User
from werkzeug.security import generate_password_hash

def create_user():
    # Datos del nuevo usuario
    username = 'nuevo_usuario'  # Cambia el nombre de usuario
    password = 'contraseña_segura'  # Cambia la contraseña

    # Hashear la contraseña
    hashed_password = generate_password_hash(password, method='pbkdf2:sha256')

    # Crear el nuevo usuario
    new_user = User(username=username, password=hashed_password)
    
    # Agregar el usuario a la base de datos
    db.session.add(new_user)
    db.session.commit()

    print(f"Usuario {username} creado con éxito!")

if __name__ == '__main__':
    app = create_app()  # Crear la aplicación
    with app.app_context():  # Establecer el contexto de la aplicación
        create_user()  # Crear el usuario dentro del contexto