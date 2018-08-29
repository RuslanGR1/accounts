# accounts

## Quickstart:
```
$ mkdir sites
$ cd sites 
$ git clone https://github.com/RuslanGR1/accounts.git
$ cd accounts

$ virtualenv --no-site-packages venv
$ cd venv/Scripts
$ activate
$ cd ../..
$ cd website
$ pip install --upgrade -r requirements.txt

$ python manage.py migrate
$ python manage.py createsuperuser
...

$ python manage.py runserver
```

### Settings update:
> Add your qiwi phone number and qiwi api token (permission to view payment history)

../website/website/settings.py
```
base_num = ''

token = ''
```
