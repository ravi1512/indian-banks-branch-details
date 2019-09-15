# Sample Flask App with Heroku

This service exposes two GET APIs to fetch a bank's branch details based on IFSC Code and list all branches of a bank in a city. It uses PostgreSQL as database.

- GET /branch/ifsc/{ifsccode}
- GET /branch/bank/{bank name}/city/{city}

We have used this dataset in our database - https://github.com/snarayanank2/indian_banks
