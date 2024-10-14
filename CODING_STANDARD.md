# Coding standard for Python projects

## Python Project Guidelines

## Table of Contents
1. [Project Naming Conventions](#project-naming-conventions)
    - [Classes](#classes)
    - [Variables](#variables)
    - [Functions](#functions)
    - [Enums](#enums)
    - [Constants](#constants)
2. [Secret Management](#secret-management)
3. [Project Management and Redundancy Minimization](#project-management-and-redundancy-minimization)
4. [OOP Best Practices](#oop-best-practices)
5. [Folder Structure](#folder-structure)
6. [API Naming Conventions](#api-naming-conventions)
7. [Generic Methods](#generic-methods)
8. [Reading Credentials from Environment Variables](#reading-credentials-from-environment-variables)

---

## Project Naming Conventions

Maintaining consistent naming conventions is crucial for code readability and maintainability.

### Classes
- Class names should use the `CamelCase` convention.
- Example:
  ```python
  class UserProfile:
      pass
  ```

### Variables
- Variable names should be in `snake_case`.
- Example:
  ```python
  user_age = 25
  ```

### Functions
- Function names should also use `snake_case`.
- Example:
  ```python
  def calculate_total(price, quantity):
      return price * quantity
  ```

### Enums
- Enum names should use `CamelCase`, and members should use `UPPER_SNAKE_CASE`.
- Example:
  ```python
  from enum import Enum

  class UserRole(Enum):
      ADMIN = "admin"
      USER = "user"
  ```

### Constants
- Constant names should be in `UPPER_SNAKE_CASE`.
- Example:
  ```python
  MAX_CONNECTIONS = 100
  ```

## Secret Management

Managing secrets is crucial for maintaining application security. Use the following practices:
- Store sensitive information (API keys, database passwords) in environment variables or secret management tools (like HashiCorp Vault, AWS Secrets Manager).
- Use libraries like `python-dotenv` to load environment variables from a `.env` file.

### Example
Create a `.env` file:
```
DATABASE_URL=postgres://user:password@localhost:5432/mydatabase
SECRET_KEY=my_secret_key
```

Load it in your Python code:
```python
import os
from dotenv import load_dotenv

load_dotenv()

database_url = os.getenv('DATABASE_URL')
secret_key = os.getenv('SECRET_KEY')
```

## Project Management and Redundancy Minimization

To minimize redundancy and improve maintainability, follow these guidelines:
- **DRY Principle (Don't Repeat Yourself)**: Avoid duplicating code. Use functions or classes to encapsulate reusable logic.
- **SOLID Principles**: Adhere to SOLID principles to ensure your code is well-structured and maintainable:
  - **S**ingle Responsibility Principle: Each class/function should have one responsibility.
  - **O**pen/Closed Principle: Code should be open for extension but closed for modification.
  - **L**iskov Substitution Principle: Subtypes must be substitutable for their base types.
  - **I**nterface Segregation Principle: Prefer small, client-specific interfaces over large, general-purpose ones.
  - **D**ependency Inversion Principle: Depend on abstractions, not concretions.

## OOP Best Practices

To achieve OOP best practices:
- Use encapsulation: Keep data private and expose it via public methods.
- Utilize inheritance wisely to promote code reuse.
- Implement polymorphism to define methods in subclasses that have the same name but different behaviors.

### Example
```python
class Animal:
    def speak(self):
        raise NotImplementedError("Subclasses must implement this method")

class Dog(Animal):
    def speak(self):
        return "Woof!"

class Cat(Animal):
    def speak(self):
        return "Meow!"
```

## Folder Structure

A well-organized folder structure enhances the manageability of the project. Here’s a suggested structure:

```
my_project/
│
├── app/               # Main application code
│   ├── __init__.py
│   ├── main.py        # Entry point of the application
│   ├── routes/        # API routes
│   ├── services/      # Business logic
│   └── models/        # Data models
│
├── databases/         # Database-related code
│   ├── __init__.py
│   ├── connection.py   # Database connection logic
│   └── schemas.py      # Database schemas
│
├── enums/             # Enum definitions
│   ├── __init__.py
│   └── user_roles.py   # User roles enumeration
│
├── constants/         # Constant values
│   ├── __init__.py
│   └── config.py       # Application constants
│
├── prompts/           # Predefined prompts for LLM or other services
│   ├── __init__.py
│   └── prompt_templates.py
│
├── tests/             # Test cases
│   ├── __init__.py
│   ├── test_models.py
│   └── test_services.py
│
└── utils/             # Utility functions
    ├── __init__.py
    └── helpers.py      # Helper functions
```

## API Naming Conventions

Follow REST API standards for naming conventions:
- Use nouns for resources (e.g., `/users`, `/orders`).
- Use HTTP methods to define actions:
  - `GET` for fetching data.
  - `POST` for creating data.
  - `PUT` for updating data.
  - `DELETE` for deleting data.

### Example
```python
from fastapi import FastAPI

app = FastAPI()

@app.get("/users/{user_id}")
def get_user(user_id: int):
    return {"user_id": user_id}

@app.post("/users")
def create_user(user: UserProfile):
    return {"message": "User created", "user": user}
```

## Generic Methods

Creating generic methods can improve code reusability. Use Python's `typing` module to define generic types.

### Example
```python
from typing import TypeVar, List

T = TypeVar('T')

def get_first_element(elements: List[T]) -> T:
    return elements[0]

numbers = [1, 2, 3]
first_number = get_first_element(numbers)  # Returns 1
```

## Reading Credentials from Environment Variables

As shown in the Secret Management section, always read credentials from environment variables instead of hardcoding them in your application.

### Example
```python
import os

API_KEY = os.getenv("API_KEY")
```

---

# Dos and Don'ts for Python Project Guidelines

## Naming Conventions

### **Dos:**
- **Do** use `CamelCase` for class names.
  - Example:
    ```python
    class UserProfile:
        pass
    ```
- **Do** use `snake_case` for variables and function names.
  - Example:
    ```python
    def calculate_total(price, quantity):
        return price * quantity
    ```
- **Do** use `UPPER_SNAKE_CASE` for constants.
  - Example:
    ```python
    MAX_CONNECTIONS = 100
    ```
- **Do** use descriptive names that convey meaning.
  - Example:
    ```python
    user_age = 25  # Clear and descriptive variable name
    ```

### **Don'ts:**
- **Don't** use single-letter variable names unless in short loops or very small scopes.
  - Bad Example:
    ```python
    def add(a, b):
        return a + b
    ```
  - Good Example:
    ```python
    def add_numbers(first_number, second_number):
        return first_number + second_number
    ```
- **Don't** use ambiguous names that don't convey meaning.
  - Bad Example:
    ```python
    def f(x):
        return x * 2
    ```
  - Good Example:
    ```python
    def double_value(value):
        return value * 2
    ```

## Class Design

### **Dos:**
- **Do** follow the Single Responsibility Principle. Each class should have one responsibility.
  - Example:
    ```python
    class UserManager:
        def create_user(self, username, password):
            pass

        def delete_user(self, user_id):
            pass
    ```
- **Do** use inheritance and interfaces appropriately to promote code reuse.
  - Example:
    ```python
    class Animal:
        def make_sound(self):
            raise NotImplementedError("Subclasses must implement this method")

    class Dog(Animal):
        def make_sound(self):
            return "Woof!"

    class Cat(Animal):
        def make_sound(self):
            return "Meow!"
    ```

### **Don'ts:**
- **Don't** create classes with too many responsibilities.
  - Bad Example:
    ```python
    class UserManager:
        def create_user(self, username, password):
            pass

        def delete_user(self, user_id):
            pass

        def send_email(self, user_id):
            pass  # Mixing responsibilities
    ```
  - Good Example:
    ```python
    class UserManager:
        def create_user(self, username, password):
            pass

    class EmailService:
        def send_email(self, user_id):
            pass
    ```
- **Don't** use public attributes unnecessarily; prefer encapsulation.
  - Bad Example:
    ```python
    class User:
        def __init__(self, name):
            self.name = name  # Public attribute
    ```
  - Good Example:
    ```python
    class User:
        def __init__(self, name):
            self.__name = name  # Private attribute

        def get_name(self):
            return self.__name  # Access via method
    ```

## Abstractions

### **Dos:**
- **Do** define abstract classes to enforce a contract for subclasses.
  - Example:
    ```python
    from abc import ABC, abstractmethod

    class Shape(ABC):
        @abstractmethod
        def area(self):
            pass

    class Circle(Shape):
        def __init__(self, radius):
            self.radius = radius

        def area(self):
            return 3.14 * self.radius ** 2
    ```

### **Don'ts:**
- **Don't** implement logic in abstract classes.
  - Bad Example:
    ```python
    class Shape(ABC):
        def area(self):  # Not allowed, as it's supposed to be abstract
            return 0
    ```
  - Good Example:
    ```python
    class Shape(ABC):
        @abstractmethod
        def area(self):
            pass  # Correctly defined as abstract
    ```

## General OOP Best Practices

### **Dos:**
- **Do** use composition over inheritance when appropriate.
  - Example:
    ```python
    class Engine:
        def start(self):
            print("Engine started")

    class Car:
        def __init__(self):
            self.engine = Engine()

        def start(self):
            self.engine.start()
    ```
- **Do** ensure classes are loosely coupled by depending on abstractions.
  - Example:
    ```python
    class NotificationService:
        def notify(self, message):
            print(f"Notification: {message}")

    class User:
        def __init__(self, notification_service: NotificationService):
            self.notification_service = notification_service

        def alert_user(self):
            self.notification_service.notify("This is an alert")
    ```

### **Don'ts:**
- **Don't** tightly couple classes, which makes testing and maintenance harder.
  - Bad Example:
    ```python
    class User:
        def __init__(self):
            self.notification_service = NotificationService()  # Tight coupling

        def alert_user(self):
            self.notification_service.notify("This is an alert")
    ```
  - Good Example:
    ```python
    class User:
        def __init__(self, notification_service: NotificationService):
            self.notification_service = notification_service
    ```
