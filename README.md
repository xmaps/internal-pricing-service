# Internal Pricing Service API

## Getting Started

Please clone the project to your local machine and follow this README.

#### Prerequisites
1. Set up a virtual environment
2. Clone the repo
3. `cd internal-pricing-service/`

#### Installing Requirements

`pip install -r config/requirements.pip`

#### Make the initial set up of the database

4. `cd src/`
5. `python manage.py makemigrations`
6. `python manage.py makemigrations orders`
7. `python manage.py migrate`

#### Import pricing information (can be done to add as many as wanted)
8. `python manage.py import_data ../config/pricing.json`

#### Run the Server locally
9. `python manage.py runserver`

#### Run the tests
10. `python manage.py behave`

*Note:* Python 3.6 on MacOS uses an embedded version of OpenSSL,
which does not use the system certificate store. Because of this
urlfecth gives problems. If it happens to you run this command.
`/Applications/Python\ 3.6/Install\ Certificates.command`

## Ideas for improvements
There's always room for improvements. And since this task had a time limit here follows some ideas to improve:

* Add `total_vat` and `vat_price` as properties, but couldn’t get them to show on the serializer for the response
* I like behave but I would add more unit tests with coverage (and mock the currency api so it doesn't get different responses every time)
* Check the import data command does not in fact duplicate info
* Figure out how to proper handle the `request.data`. It seems that with the tests it goes 
directly to the content of the request but with the Django rest framework page on the browser 
send more information than just the JSON of the request
* Since the currency data keeps changing, testing the currency response keeps giving errors so I would use mock for this
* I'm still divided in the way Django rest framework works. Another library that could be checked is google endpoints (because it uses ProtoBuf), it allows to define sets of messages for request and response for each api without being connected to models. Allows separations, enforces rules and in terms of code it works almost as documentation.
* More security and error handling
* Figure out how to use serializers to force the request to the apis like docs from Django rest framework do.
* Better documentation on the code and on the README.

## What bits did you find the toughest? What bit are you most proud of? In both cases, why?

Setting up the BDD tests was tough, I still don’t have much experience using behave and behave-django and took time and some trial and error. 
And also tough was the usage of Django rest framework, it's something that I never have the opportunity to use and that 
correlates to the fact i'm most proud of. I used the Serializers and it helps to take out logic from the view 
and simplify it (despite the fact I still don't know how to use Serializers to force request parameters only response).

## What one thing could we do to improve this test?
Give more time to do the test. If someone wants to make a good work and maybe use something they never used before I don't 
think 90mins is realistic. I would probably make the requirements more clear. Like a set of goals to achieve and a set of nice to have features.
