1. What is a property manager company and what is their role? Please provide the
names of 3 property management companies.
 - Property manager company is a midlmen between the property owner and tenant.
 Some companies:
    Greystar Real Estate Partners,
    Lincoln Property Company,
    Asset Living
2. What is a property management software company? Please provide the names of
3 property management software companies.
    - A company that provides software solutions designed for property managers. Basicly creates a software infrastructure that allows property manager company to work more efficient.
    - Companies:
        LVBLE,
        AppFolio,
        Innago
3. What is greystar? How many apartments do they manage? Tell us something
interesting about them that we might not know. Do they use property
management software? If so, which one? How did you get to that answer?
    - Greystar is a largets property manager company. According to them, they manage more than 996,900 multifamily units. They do use the property management software. It seems, that they are in partnership with Yardi Systems (found with GPT 4.0). 
     I believe you know more than me, but they are investing a lot in enegry savings, like LED loghting, carbon footprint and more.


How to run task:
run `docker-compose up --build`
you can validate that docker is running by executing `docker ps`
it will create a container
copy the following command into your shell or postman
```sh
curl -X 'POST' \
  'http://localhost:8000/save_data/' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "tenant_portal": "click_pay",
  "username": "micael.lasry@gmail.com",
  "password": "Micael123"
}'
```

Validate the data at the DB:
 Connect to container and run `sqlite3 /data/mydatabase.db`
 run `SELECT * FROM users;`
You can run tests.
check <container_id> from `docker ps`
connect into container `docker exec -it <container_id> /bin/bash`
run `pytest`
