*Note:* This steps should be executed inside a virtual environment

2. `cd internal-pricing-service/`
3. `pip install -r config/requirements.pip`
4. `cd src/`
5. `python manage.py makemigrations`
6. `python manage.py makemigrations orders`
7. `python manage.py migrate`
8. `python manage.py import_data ../config/pricing.json`
9. `python manage.py runserver`


10. To run the tests: `python manage.py behave`

*Note:* Python 3.6 on MacOS uses an embedded version of OpenSSL,
which does not use the system certificate store. Because of this
urlfecth gives problems. If it happens to you run this command.
`/Applications/Python\ 3.6/Install\ Certificates.command`