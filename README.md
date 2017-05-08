# Backend Project

## Description:
Backend API written in Flask that queries a MySQL database and returns JSON objects. This project may be hosted on AWS for a short period of time.

SQLAlchemy was not used because the queries were simple and only has GET requests. By choosing not to use an ORM, there are several advantages and disadvantages:

Advantages:
 - Performance: ORM is sometimes considered middleware that adds overhead.
 - Greater control over query optimization.
 - Less dependencies to worry about (Only a thin wrapper for mysqlclient is needed).

Disadvantages:
 - If table columns names are subject to change, an ORM is more appropriate.
 - An ORM comes with features that saves time.
 - Arguably easier to maintain

## Tips on Using AWS EC2, Elastic Beanstalk, RDS

To avoid WSGI pathing errors, initialize the Flask application as `application.py` and use `application = Flask(__name__)`. It is also possible to change the path through `eb config`.

Create an application of Elastic Beanstalk first then set up a database instance on RDS after.

MySQL dump file was transferred to the application's EC2 instance via scp. SSH into the EC2 instance then login with (the already proloaded) mysqlclient.

```
mysql -h db.instance.endpoint -P 3306 -u db.user -p

mysql> use db.name;
mysql> source /path/to/filename.mysql.dump;
```

## How it works:
```
http://hostname/api/v1/shipments
```
Make GET request through the URI with these supported parameters:

company_id: Required for all searches. Must be an integer.
```
/api/v1/shipments?company_id=2
```

page / per: Pagination of returned results. Default page contains 4 objects. Exceeding end page limits returns object on last page.
```
/api/v1/shipments?company_id=2&page=2&per=2
```

international\_transportation_mode: ocean or truck
```
/api/v1/shipments?company_id=2&international_transportation_mode=ocean
```

sort / direction: Must pass column and direction. Accepted columns for sorting are name, international\_departure\_date, created\_at, updated\_at
```
/api/v1/shipments?company_id=2&sort=international_departure_date&direction=asc
```

## Tests:
Tests are in Ruby; installation instructions and additional information [here](https://github.com/flexport/glexport-test).

## File structure:
```
/rankscience
    app.py
    config.py
    requirements.txt
    README.md
    /rankscience
        __init__.py
        helpers.py
        /templates
            index.html
    /glexport-test
        ...
```

## Table Structure:

**companies**
```
+------------+--------------+------+-----+---------+----------------+
| Field      | Type         | Null | Key | Default | Extra          |
+------------+--------------+------+-----+---------+----------------+
| id         | int(11)      | NO   | PRI | NULL    | auto_increment |
| name       | varchar(255) | NO   |     | NULL    |                |
| created_at | datetime     | NO   |     | NULL    |                |
| updated_at | datetime     | NO   |     | NULL    |                |
+------------+--------------+------+-----+---------+----------------+
```

**products**
```
+-------------+--------------+------+-----+---------+----------------+
| Field       | Type         | Null | Key | Default | Extra          |
+-------------+--------------+------+-----+---------+----------------+
| id          | int(11)      | NO   | PRI | NULL    | auto_increment |
| sku         | varchar(255) | NO   |     | NULL    |                |
| description | varchar(255) | NO   |     | NULL    |                |
| company_id  | int(11)      | NO   |     | NULL    |                |
| created_at  | datetime     | NO   |     | NULL    |                |
| updated_at  | datetime     | NO   |     | NULL    |                |
+-------------+--------------+------+-----+---------+----------------+
```

**shipment_products**
```
+-------------+----------+------+-----+---------+----------------+
| Field       | Type     | Null | Key | Default | Extra          |
+-------------+----------+------+-----+---------+----------------+
| id          | int(11)  | NO   | PRI | NULL    | auto_increment |
| product_id  | int(11)  | NO   |     | NULL    |                |
| shipment_id | int(11)  | NO   |     | NULL    |                |
| quantity    | int(11)  | NO   |     | NULL    |                |
| created_at  | datetime | NO   |     | NULL    |                |
| updated_at  | datetime | NO   |     | NULL    |                |
+-------------+----------+------+-----+---------+----------------+
```
**shipments**
```
+-----------------------------------+--------------+------+-----+---------+----------------+
| Field                             | Type         | Null | Key | Default | Extra          |
+-----------------------------------+--------------+------+-----+---------+----------------+
| id                                | int(11)      | NO   | PRI | NULL    | auto_increment |
| name                              | varchar(255) | NO   |     | NULL    |                |
| company_id                        | int(11)      | NO   | MUL | NULL    |                |
| created_at                        | datetime     | NO   |     | NULL    |                |
| updated_at                        | datetime     | NO   |     | NULL    |                |
| international_transportation_mode | varchar(255) | NO   |     | NULL    |                |
| international_departure_date      | date         | NO   |     | NULL    |                |
+-----------------------------------+--------------+------+-----+---------+----------------+
```

## To do:
 - Compare performance using SQLAlchemy ORM vs passing raw SQL string.
 - Support searching for multiple company_id at once
 - Return header metadata on total number of results
 - Fix paginate behavior to abort if exceeded number of pages
