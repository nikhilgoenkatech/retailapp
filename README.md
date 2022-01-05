# Django e-commerce website

E-commerce website built with Django. It has following functionality:
- user registration
- add / change user billing address
- add / remove item from cart
- change the default billing address during the checkout process
- apply a promotion code during the checkout process
- pay for a order using Stripe
- list all proceeded orders
- request a refund for a order

The purpose of this project was to learn Django Framework.

## Setup

- Run the `devinstall` startup script in the `/bin` folder. This script should create a Python virtual environment named `env`, activate it, then install all of the required project dependencies. You should be able to run all of the binaries in this folder from the root of the project.
```
./bin/devinstall
```

- After running the install script, your Python virtual environment should be activated. You'll notice an `(env)` in your terminal if the environment is successfully activated. If it isn't, activate it by running:
```
source env/bin/activate
```

- Run the `devstartup` script in the `/bin` folder to start the retailapp in development mode.
```
./bin/devstartup
```

## Example of app
Home page

![home-page](https://user-images.githubusercontent.com/32844693/67404105-27f79980-f5b3-11e9-9f9f-d8e7a9e8c401.PNG)

Product details page

![product-detail](https://user-images.githubusercontent.com/32844693/67404107-28903000-f5b3-11e9-9a02-e2767525eb69.PNG)

Shipping address form page

![shipping-address](https://user-images.githubusercontent.com/32844693/67404108-28903000-f5b3-11e9-9d68-a17805ac4efa.PNG)

Refund page

![refund-page](https://user-images.githubusercontent.com/32844693/67404109-28903000-f5b3-11e9-8650-88c071e2e605.PNG)

Cart page

![cart](https://user-images.githubusercontent.com/32844693/67404274-6b520800-f5b3-11e9-80fc-c9db7c7bb732.PNG)

Checkout page

![checkout-page-without-code](https://user-images.githubusercontent.com/32844693/67404275-6bea9e80-f5b3-11e9-8c98-8c6ae9397f46.PNG)

Checkout page with discount code

![checkout-page-with-code](https://user-images.githubusercontent.com/32844693/67404278-6bea9e80-f5b3-11e9-91a7-be595b128732.PNG)

Payment page

![payment](https://user-images.githubusercontent.com/32844693/67404276-6bea9e80-f5b3-11e9-94ec-5a9e2215cf55.PNG)

Success order page

![success-page](https://user-images.githubusercontent.com/32844693/67404277-6bea9e80-f5b3-11e9-987b-20c573e4fa74.PNG)

Orders page

![orders-list](https://user-images.githubusercontent.com/32844693/67404279-6bea9e80-f5b3-11e9-9bb3-513836cc76fc.PNG)

## Technologies

- Python 3.8
- Django 2.2.10
- HTML / JS
- Bootstrap 4.3.1
- Stripe API
- mailtrap.io
- AJAX