http://127.0.0.1:8000/api/users/register/

http://127.0.0.1:8000/api/products/
http://127.0.0.1:8000/api/products/?limit=3&offset=2
http://127.0.0.1:8000/api/products/?ordering=category
http://127.0.0.1:8000/api/products/?ordering=name
http://127.0.0.1:8000/api/products/?ordering=price
http://127.0.0.1:8000/api/products/?name=Marchewka
http://127.0.0.1:8000/api/products/?price=1
http://127.0.0.1:8000/api/products/?description=cebulowe
http://127.0.0.1:8000/api/products/?category=Chrupki

http://127.0.0.1:8000/api/products/1/

http://127.0.0.1:8000/api/orders/
mail w konsoli


{
  "customer_name": "Kornel",
  "customer_surname": "Chodnik",
  "delivery_address": "c",
  "products": [
    {
      "product": 3,
      "quantity": 4
    },
    {
      "product": 4,
      "quantity": 5
    }
  ]
}

http://127.0.0.1:8000/api/statistics/products/
http://127.0.0.1:8000/api/statistics/products/?products-number=4&from=2023-10-8&to=2023-10-9
