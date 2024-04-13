# Django REST Framework Project README

Welcome to the Django REST Framework project! This 
project is built using Django and Django REST Framework (DRF) 
to create a robust RESTful API.

## Getting Started

To run this project on your local machine, follow these steps:

### 1. Clone the Repository

First, clone this repository to your local machine using Git:

```bash
git clone https://github.com/your_username/django-rest-project.git
```

### 2. Navigate to the Backend Folder

Navigate to the backend folder in the project directory using the terminal:

```bash
cd backend
```

### 3. Set Up Virtual Environment

Navigate to the project directory and 
set up a virtual environment using `venv`:

```bash
python -m venv venv
```

Activate the virtual environment:

**For Windows:**

```bash
. venv/Scripts/activate
```

**For MacOS/Linux:**

```bash
source env/bin/activate
```

### 4. Install Dependencies

Once the virtual environment is activated, install the project 
dependencies using `pip` and the `requirements.txt` file:

```bash
pip install -r requirements.txt
```

### 5. Apply Database Migrations

Before running the server, apply the database migrations:

```
python manage.py migrate
```

### 6. Run the Server

After installing the dependencies, you can run the Django development server:

```bash
python manage.py runserver
```

This will start the development server at `http://127.0.0.1:8000/`.

### 7. Accessing the API

Once the server is running, you can access the API endpoints 
through your web browser or a tool like Postman. The base 
URL for API endpoints will be `http://127.0.0.1:8000/`.

## Database Migrations

This project utilizes Django's built-in migration system to manage 
changes to the database schema. Here's how to handle migrations:

### 1. Make Migrations

Whenever you make changes to the models in your Django project, 
you need to create migration files that represent those changes. 
To do this, run:

```bash
python manage.py makemigrations
```

This command will analyze the changes you've made to your 
models and create migration files in the `migrations` directory 
of each app within your project.

### 2. Apply Migrations

After creating migration files, you need to apply those changes to your database. 
To do this, run:

```bash
python manage.py migrate
```

This command will execute the migrations and modify the database 
schema to match the changes you've made to your models. It will 
create tables, add or remove fields, and perform other necessary operations.

### 3. Viewing Migration Status

You can view the status of migrations to see which migrations have been 
applied and which are pending by running:

```bash
python manage.py showmigrations
```

This command will display a list of all migrations and their status 
(applied or not applied).

By following these steps, you can effectively manage your 
database schema changes and keep your database in sync with 
your Django project's models.

## Contributing

If you would like to contribute to this project, feel free to fork the repository 
and submit pull requests. Make sure to follow the contribution guidelines 
outlined in the `CONTRIBUTING.md` file.

## License

This project is licensed under the MIT License - see the `LICENSE` file for details.

## Acknowledgments

Special thanks to the Django and DRF communities for 
their excellent documentation and resources.

Thank you for using our Django REST Framework project! 
If you have any questions or issues, please don't hesitate to reach out.

<!-- TODO: add admin login ..... -->
<!-- TODO: specify cd to backend  ..... -->
<!-- # Django Project Setup Guide

This comprehensive guide provides detailed steps for setting up a Django project, covering virtual environment creation, Django installation, Django Rest Framework integration, and management of project dependencies.

## Setting up Virtual Environment

1. **Create and Activate a Virtual Environment:**
    ```bash
    python -m venv [name]
    . [name]/Scripts/activate
    ```

   This ensures a clean and isolated environment for your Django project.

## Installing Django

2. **Install Django:**
    ```bash
    python -m pip install Django
    ```

3. **Create a New Django Project:**
    ```bash
    django-admin startproject [name] .
    ```

   This initializes a new Django project with the specified name.

## Installing Django Rest Framework

4. **Install Django Rest Framework:**
    ```bash
    pip install djangorestframework
    ```

5. **Configure Django Rest Framework:**
    Add 'rest_framework' to your `INSTALLED_APPS` setting in the `settings.py` file of your project:
    ```python
    INSTALLED_APPS = [
        # ...
        'rest_framework',
    ]
    ```

   This integrates the powerful Django Rest Framework into your project.

## Running the Django Development Server

6. **Start the Django Development Server:**
    ```bash
    python manage.py runserver
    ```

   Access your Django application at [http://127.0.0.1:8000/](http://127.0.0.1:8000/) in your web browser.

## Managing Dependencies with pip freeze

### Creating requirements.txt

7. **Output Installed Packages to `requirements.txt`:**
    ```bash
    python -m pip freeze > requirements.txt
    ```

   This creates a snapshot of your project's dependencies for easy replication.

### Installing Dependencies from requirements.txt

8. **Install Dependencies from `requirements.txt`:**
    ```bash
    python -m pip install -r requirements.txt
    ```

   This ensures consistency across development environments.

## After Cloning the Repository

9. **Create and Activate a Virtual Environment (if not already created):**
    ```bash
    python -m venv [name]
    . [name]/Scripts/activate
    ```

10. **Install Project Dependencies:**
    ```bash
    python -m pip install -r requirements.txt
    ```

   This is essential after cloning the repository to set up the environment with the required packages.

By following these detailed instructions, you'll have a well-structured 
Django project with virtual environment isolation, Django installation, 
Django Rest Framework integration, and proper dependency management. -->