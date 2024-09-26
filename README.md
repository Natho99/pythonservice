# Python Service: Customer and Order Management API

This project is a simple Python-based REST API built with Django for managing customers and orders. The service allows you to create, retrieve, update, and delete customers and orders, with authentication via OpenID Connect and SMS notifications via Africa's Talking SMS gateway.

## Features

- **Customers**: Add, update, retrieve, and delete customers with basic details like name, code, and phone number.
- **Orders**: Manage orders with details such as item, amount, and order time.
- **Authentication**: The API is secured with OpenID Connect (OIDC) for authentication.
- **SMS Alerts**: When an order is created, the customer receives an SMS notification using Africa's Talking SMS gateway.
- **Unit Testing**: Comprehensive unit tests with coverage checking are provided.
- **CI/CD**: Continuous Integration (CI) is set up using GitHub Actions to automate testing. You can integrate Continuous Deployment (CD) with any platform of your choice.

## Technologies Used

- **Python**: The core language for the project.
- **Django**: Used for building the web framework.
- **Django REST Framework (DRF)**: To build the RESTful API.
- **PostgreSQL**: The database used in production (with SQLite used in development).
- **OpenID Connect (OIDC)**: For authentication and authorization.
- **Africa's Talking**: Used for sending SMS notifications.
- **GitHub Actions**: Set up for automated testing and CI.

## Prerequisites

Before you begin, ensure you have the following installed:

- Python 3.x
- pip (Python package manager)
- PostgreSQL (for production)
- Git

## Setup Instructions

1. **Clone the repository**:
   ```bash
   git clone https://github.com/Nathoo99/pythonservice.git
   cd pythonservice
