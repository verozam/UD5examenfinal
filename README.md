# Proyecto Flask

## Requisitos

1. Python 3.8+ instalado.
2. Tener `venv` habilitado para crear un entorno virtual.

## Pasos para levantar el proyecto

1. Clona este repositorio:

   ```bash
   git clone https://github.com/verozam/UD5examenfinal.git
   cd UD5examenfinal
   ```

2. Crea y activa un entorno virtual:

   ```bash
   python -m venv venv
   # En Windows
   venv\Scripts\activate
   ```

3. Instala las dependencias:

   ```bash
   pip install -r requirements.txt
   ```

4. Inicializa la base de datos:

   ```bash
    flask db init
    flask db migrate
    flask db upgrade
   ```

5. Corre el servidor:
   ```bash
    flask run
   ```
