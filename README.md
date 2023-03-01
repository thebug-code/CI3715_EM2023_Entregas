# SAGTMA

Sistema Automatizado de Gestión del Taller Mecánico Automotriz de Alta Gama Holiday International.

## Comenzando :rocket:

Estas instrucciones le permitirán obtener una copia del proyecto en funcionamiento en su máquina local para fines de desarrollo y prueba.

Necesitará tener Python instalado en su sistema. Puede descargarlo desde [aquí](https://www.python.org/downloads/).

También necesitará tener pip, el administrador de paquetes para Python, instalado. Puede aprender más sobre pip [aquí](https://pip.pypa.io/en/stable/).

## Instalación :coffee:

Para poner en marcha el proyecto, siga estos pasos:

1. Comience clonando el repositorio en su máquina local y navegando a él:

```bash
git clone https://github.com/thebug-code/SAGTMA.git
cd SAGTMA
```

2. Cree y active un entorno virtual para el proyecto

```powershell
python -m venv venv
source venv/bin/activate # o simplemente .\venv\Scripts\Activate.bat en Windows
```

3. Instale las dependencias del proyecto:

```bash
pip install -r requirements.txt
```

4. Inicialice la base de datos y luego el servidor de desarrollo de Flask:

```bash
flask --app SAGTMA init-db
flask --app SAGTMA --debug run
```

5. ¡Listo! La aplicación ahora debería estar en funcionamiento en <http://localhost:5000>.

## Construido con

- [Flask](https://flask.palletsprojects.com/en/2.0.x/) - El framework utilizado.
- [SQLite3](https://www.sqlite.org/index.html) - El motor de base de datos utilizado.
- [Flask-SQLAlchemy](https://flask-sqlalchemy.palletsprojects.com/en/3.0.x/) - El ORM utilizado.
