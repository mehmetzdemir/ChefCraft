# ChefCraft
Recipes Website

## INSTALL

 - Clone the repository: `git clone https://github.com/mehmett420/ChefCraft.git chefcraft`
 - `cd chefcraft`
 - Make a virtual enviromment: `virtualenv venv -p python3`
 - Activate: `source venv/bin/activate`
 - Install dependencies: `pip install -r requirements.txt`
 - Setup the database: `python manage.py migrate`
 - Add admin user: `python manage.py createsuperuser`
 - Run server: `python manage.py runserver`

## Database

Project uses MySQL in PythonAnywhere

 - Install mysql client: `pip install mysqlclient`
 - Set database settings in the `local_settings.py` file:
   - `ENGINE: django.db.backends.mysql`
   - `NAME: chefcraft`
   - `USER: <db_user>`
   - `PASSWORD: <db_password>`
   - `HOST: <mysql_host>`
   - `PORT: 3306`
