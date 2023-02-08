"# todo" 
1. Requirements for project:\
    - First create venv using python -m venv "{env_name}"
    - activate the env. According to the system.
    - Install from requirements.txt pip install -r requirements.txt
    - Do django migration using python manage.py migrate
    - Run django server to start the app. 
    - python manage.py runserver

2. APIs Available:
    - Auth APIs:
            ~ Add user: /api/register:
                {
                    "username": ,
                    "password": ,
                    "first_name":,
                    "last_name":,
                }
            ~ Delete User: api/account/{"user_id"}:
                    create own super user
                    python3 manage.py createsuperuser
            ~ Login : api/token/
                {
                    "username":,
                    "password":,
                }
            ~ Update refresh token: api/token/refresh/

    -  Task API:
            ~ Add Task: /api/task
                {
                    "title": "",
                    "description":"",
                    "created_by_name": "",
                    "created_by_id":3
                }
            ~