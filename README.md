# Key notes
I recommend using browsable API for testing.
I have enabled basic and session authentication for the views that require authorization.
To authenticate with basic authentication please include username and password in each request.


# Instructions
* (Optional) Create a virtual enviroment:
  ```shell
  python3 -m venv .venv
  ```

* (Optional) Acivate the virtual environment:
  ```shell
  . .venv/bin/activate
  ```
* Install packages:
  ```shell
  pip install -r requirements.txt 
  ```

* Make migrations and migrate:
  ```shell
  python manage.py makemigrations
  python manage.py migrate
  ```

* Create superuser in order to use the Django admin panel
  ```shell
  python manage.py createsuperuser
  ```

* Run the application
  ```shell
  python manage.py runserver
  ```

* Create a new user with 'Seller' or 'Customer' permissions at:
  ```
  POST /api/users/register/
  ```
  Required fields:
  ```
  username, password, first_name, last_name, email, group ('Seller' | 'Customer')
  ```

* Create new product categories. Unfortunately it's only supported through the Django admin panel as it was not given in the requirements and I realised it too late.

* Create new product items either through Django admin panel or through an endpoint:
  ```
  POST /api/products/
  ```
  Required fields:
  ```
  category, name, description, price, image
  ```

# Endpoints
* Create new user
  ```
  POST /api/users/register/
  ```

* Create new product
  ```
  POST /api/products/
  ```

* List of products
  ```
  GET /api/products/
  ```
  Pagination parameters
  ```
  GET /api/products/?limit=3&offset=2
  ```
  Filtering parameters
  ```
  GET api/products/?name=dummy-name
  GET api/products/?price=1
  GET api/products/?description=dummy-description
  GET api/products/?category=dummy-category
  ```
  Sorting parameters
  ```
  GET /api/products/?ordering=category
  GET /api/products/?ordering=name
  GET /api/products/?ordering=price
  ```

* Product details
  ```
  GET /api/products/1/
  ```
  Update product
  ```
  PUT /api/products/1/
  ```
  Detele product
  ```
  DELETE /api/products/1/
  ```

* Create new order
  ```
  POST /api/orders/
  ```
  Example request:
  ```json
  {
    "customer_name": "Dummyname",
    "customer_surname": "Dummysurname",
    "delivery_address": "dummy@mail.com",
    "products": [
      {
        "product": 1,
        "quantity": 2
      },
      {
        "product": 2,
        "quantity": 3
      }
    ]
  }
  ```

* Product statistics
  ```
  GET /api/statistics/products/
  ```
  Filtering parameters
  ```
  GET /api/statistics/products/?products-number=4
  GET /api/statistics/products/?from=2023-10-8
  GET /api/statistics/products/?&to=2023-10-9
  ```