# FinalProject

## Set Up

1. Move to directory holding project
```
$ cd final_project
```
2. Create virtail environment (only required on initial setup)
```
$ python3 -m venv myvenv
```
3. Activate virtual environment
```
$ source myvenv/bin/activate
```
If this fails try this command instead:
```
. myvenv/bin/activate
```
4. Install Django (only required on initial setup)
```
$ pip install Django
```
5. Install Crispy Form
```
pip install django-crispy-forms
```

6. Make migrations (only required on inital setup)
```
$ python3 manage.py makemigrations
$ python3 manage.py migrate
```
7. Launch Final Project
```
$ python3 manage.py runserver --insecure
```
8. Open browser and navigate to local server
(http://localhost:8000/)
