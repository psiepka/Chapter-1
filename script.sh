virtualenv venv
source venv/Scripts/activate
cd sheets_manager
pip install -r requirements.txt
python manage.py makemigrations
python manage.py migrate
python manage.py loaddata db.json
python manage.py runserver