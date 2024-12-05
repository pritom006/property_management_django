# Inventory-Management System

## Table of Contents
1. [Project Setup](#1-project-setup)
   - [Activate Virtual Environment](#activate-virtual-environment)
   - [Install Django](#install-django)
   - [Create Django Project and App](#create-django-project-and-app)
2. [Dockerization and Database Setup](#2-dockerization-and-database-setup)
   - [Build Docker Containers](#build-docker-containers)
   - [Start Docker Containers](#start-docker-containers)
   - [Running Containers Together](#running-containers-together)
3. [How to Run the Server](#3-how-to-run-the-server)
4. [Migrations](#4-migrations)
5. [Create Superuser](#5-create-superuser)
6. [CLI Commands](#6-cli-commands)
   - [Populate Locations](#populate-locations)
   - [Create Property Owners Group](#create-property-owners-group)
   - [Generate Sitemap](#generate-sitemap)
7. [Access Database](#7-access-database)
   - [Connect to Database](#connect-to-database)
   - [List All Tables](#list-all-tables)
   - [View Schema of Specific Table](#view-schema-of-specific-table)
   - [Add 3 Images](#add-3-images)
8. [Unit Testing](#8-unit-testing)
   - [Run Tests with Coverage](#run-tests-with-coverage)
   - [View Coverage Report](#view-coverage-report)

---

## 1. Project Setup

### Activate Virtual Environment
To begin, create and activate a virtual environment:

```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

## Install Django

Run the following command to install Django:

```bash
pip install django
```
## Create Django Project and App

Run the following commands to create a new Django project and app:

```bash
django-admin startproject inventory-management .
django-admin startapp property
```

## Create Django Project and App

Run the following commands to create a new Django project and app:

```bash
django-admin startproject inventory-management .
django-admin startapp property
```

---
## 2. Dockerization and Database Setup

Build the Docker containers:

```bash
docker-compose build
```
### Start Docker Containers

To start the Docker containers:

```bash
docker-compose up
```
### Running Containers Together

```bash
docker-compose up --build
```

## 3. How to Run the Server

The server will automatically start once the Docker containers are running. You can access the application at the following URLs:

- Home: [http://0.0.0.0:8000](http://0.0.0.0:8000)
- Signup: [http://0.0.0.0:8000/signup](http://0.0.0.0:8000/signup)

## 4. Migrations

To set up and update the database schema, follow these steps:

- **Create Migration Files**  
  Run the following command to create migration files:  
  ```bash
  docker-compose exec web python manage.py makemigrations
  docker-compose exec web python manage.py migrate
 ```
 
## 5. Create Superuser

To create a superuser for the Django admin interface, use the following command:

```bash
docker-compose exec web python manage.py createsuperuser
```

## 6. CLI Commands

The project includes custom Django management commands. You can run them using Docker.

- **Populate Location Data**  
  To populate location data, use:  
  ```bash
  docker-compose exec web python manage.py populate_locations
  ```
- **Create Property Owners Group**  
  To create a property owners group in the database, run:  
  ```bash
  docker-compose exec web python manage.py create_property_owners_group
  ```
- **Create Sitemap**  
  To generate a sitemap for the project, use:  
  ```bash
  docker-compose exec web python manage.py generate_sitemap
  ```
  

## 7. Access Database

You can access the PostgreSQL database directly within the Docker container.

- **Connect to the Database**  
  To access the database, run:  
  ```bash
  docker exec -it inventory-db bash
  psql -U inventory_user -d inventory_db
  ```
  
  ### List All Tables
  To list all tables in the PostgreSQL database, run the following command inside the PostgreSQL console:

  ```bash
  \dt
  \d <table_name>
  
  ![Property_accommodation table](https://ibb.co.com/47CXJmH)
  ![property_location property_localizeaccommodation table](https://ibb.co.com/6rG2KZy)
  ```
  
## 8. Unit Testing

### Run Tests with Coverage
```bash
docker-compose exec web coverage run --source='.' manage.py test
docker-compose exec web coverage report
```
