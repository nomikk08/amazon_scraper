# Amazon Product Scraper

## Introduction

The Amazon Product Scraper is a Django-based web application designed to manage and scrape product information for specified brands from Amazon. This application leverages web scraping techniques using Beautiful Soup and asynchronous task processing with Celery and Redis. It provides an intuitive admin interface for managing brands and their associated products, along with periodic scraping capabilities to keep the product information up to date.

## Features

- **Brand Management**: Easily add, edit, and delete brands from the admin interface.
- **Product Scraping**: Automatically scrape product details, including name, ASIN, SKU, and image URL for a specified brand.
- **Periodic Updates**: Use Celery to schedule scraping tasks that run periodically to keep product information up to date.
- **Pagination Handling**: The scraper dynamically handles pagination to retrieve all products associated with a brand.
- **Error Handling**: Gracefully handles errors, including retries for failed scraping tasks.

## Technologies Used

- **Django**: Web framework for building the application.
- **Celery**: Asynchronous task queue for handling scraping in the background.
- **Redis**: Message broker for Celery, used for managing task queues.
- **Beautiful Soup**: Library for web scraping and parsing HTML content.
- **Gunicorn**: WSGI HTTP server for serving the Django application.

## Installation

Follow the steps below to set up the project locally:

### Prerequisites

- Docker and Docker Compose installed on your machine.
- Basic knowledge of Django and web scraping.

### Steps to Install

1. **Clone the Repository**:

   ```bash
   git clone <repository-url>
   cd amazon_scraper
   ```

2. **Build the Docker Containers**:

   ```bash
   docker-compose build
   ```

3. **Start the Services**:

   ```bash
   docker-compose up
   ```

4. **Run Migrations**:

   If you have made changes to your `models.py` file, you can make and run migrations, execute:

   ```bash
   docker-compose run web python manage.py makemigrations
   docker-compose run web python manage.py migrate
   ```

5. **Create a Superuser**:

   To access the Django admin interface, create a superuser:

   ```bash
   docker-compose run web python manage.py createsuperuser
   ```

6. **Access the Application**:

   Open your web browser and go to `http://localhost:8000`. You can access the admin interface at `http://localhost:8000/admin` using the superuser credentials you just created.

## Usage

1. **Add Brands**: Navigate to the Brands section in the Django Admin interface to add new brands you want to scrape.

2. **Scrape Products**: The application will automatically scrape products for each brand based on the scheduled Celery tasks. You can manually trigger scraping by calling the appropriate Celery task.

3. **View Products**: Products associated with each brand can be viewed and managed in the Django Admin interface.

## Configuration

- The scraping frequency can be adjusted in the `Brand` model, allowing you to customize how often each brand's products are scraped.
- Ensure the `CELERY_BROKER_URL` in your `settings.py` file is configured to point to the Redis service.


## Acknowledgments

- [Django](https://www.djangoproject.com/) - The web framework used.
- [Celery](https://docs.celeryproject.org/en/stable/) - For handling asynchronous tasks.
- [Redis](https://redis.io/) - Used as a message broker.
- [Beautiful Soup](https://www.crummy.com/software/BeautifulSoup/) - For web scraping.

```

### Summary

This `README.md` provides a clear overview of this project, including its purpose, features, installation instructions, and usage guidelines.