# Loan-Application-template
A simple loan application template using logistic regression to approve/disapprove the application.

Dataset: https://www.kaggle.com/altruistdelhite04/loan-prediction-problem-dataset

## How to Deploy
```console
foo@bar:~$ pip install -r requirements.txt
foo@bar:~$ pip install psycopg2
```
Setup your [postgresql account](https://pynative.com/python-postgresql-tutorial/#:~:text=Install%20Psycopg2%20using%20the%20pip%20command&text=This%20module%20is%20available%20on,pip%20command%20to%20install%20Psycopg2.&text=You%20can%20also%20install%20a%20specific%20version%20using%20the%20following%20command.).

Add your details to loan > settings.py :
```
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'loan',
        'USER': '<username>',
        'PASSWORD': '<password>',
        'HOST': 'localhost'
    }
}
```
```console
foo@bar:~$ python manage.py makemigrations
foo@bar:~$ python manage.py migrate
foo@bar:~$ python manage.py runserver
```
You're all set to go. Feedback is welcome :)
