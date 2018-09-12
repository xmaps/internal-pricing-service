# Internal Pricing Service API

## Getting Started

Please clone the project to your local machine and follow this README.

### Prerequisites
1. Set up a virtual environment
2. Clone the repo
3. `cd internal-pricing-service/`

### Installing Requirements

`pip install -r config/requirements.pip`

### Make the initial set up of the database

4. `cd src/`
5. `python manage.py makemigrations`
6. `python manage.py makemigrations orders`
7. `python manage.py migrate`

### Import pricing information (can be done to add as many as wanted)
8. `python manage.py import_data ../config/pricing.json`

### Run the Server locally
9. `python manage.py runserver`


### Run the tests
10. `python manage.py behave`

*Note:* Python 3.6 on MacOS uses an embedded version of OpenSSL,
which does not use the system certificate store. Because of this
urlfecth gives problems. If it happens to you run this command.
`/Applications/Python\ 3.6/Install\ Certificates.command`