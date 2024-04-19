# DistributedLab_Orderbook
The DL Trading is a trading service where you can exchange currency.  
About `30` hours were spent on this project.

## Features
- after user registration, wallets are automatically created for all possible currencies in the database (using signals);
- the user can deposit funds to any of his wallets (manually - not implemented);
- the user can create an order for currency exchange: when creating, he indicates from which wallet he wants to transfer money, how many units of the new currency he wants to receive and the price for 1 unit or for all together;
- after creating an order with the help of signals, there is an exchange of already existing orders, according to the user's needs (first of all, the most profitable exchanges take place, limited to the price specified by the user in the new order).

## Tech Features
- Used Docker Compose for containerization.
- Error handling and other protections related to data security and authorization were used.
- Optimized and protected against N+1 problems.
- For security, funds are stored in pennies to prevent inaccuracies such as 0.2+0.1 in interpreted programming languages.
- The project is developed as Web 1 application.
- Availability of a separate Postgres database.


## Start project
- Clone this repository to your local device.
- Complete the `.env` file according to `.env.sample`.
- Run the Docker Engine.
- Build images using `docker-compose build` command in Terminal.
- Up containers using `docker-compose up` command in Terminal.

## Other
To create superuser, use the `python manage.py createsuperuser` command in Terminal and follow the next steps.
