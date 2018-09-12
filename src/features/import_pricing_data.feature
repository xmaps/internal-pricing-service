Feature: Import Pricing Data
    In order to have orders processed and info to serve on the api
    As the Maintainer
    I want to import data and save database items

    Scenario: Imported products and vat band from data

      When I import the data from file ../config/pricing.json

      Then I should have a VatBand object with name standard
      Then I should have a VatBand object with name zero
      Then I should have Product objects with 1 and 599
      Then I should have Product objects with 2 and 250
      Then I should have Product objects with 3 and 250
      Then I should have Product objects with 4 and 1000
      Then I should have Product objects with 5 and 1250

