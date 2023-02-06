"# todo" 
Requirements for project:\
    First create venv using python -m venv "{env_name}"
    activate the env. According to the system.
    Install from requirements.txt pip install -r requirements.txt
    Do django migration using python manage.py migrate
    Run django server to start the app. 
    python manage.py runserver

APIs Available:
    Auth APIs:
        Add user
            /api/register:
            {
                "username": ,
                "password": ,
                "first_name":,
                "last_name":,
            }
        Delete User
            /