# Bookly API - Repository Description

## Short Description (for GitHub/GitLab)
```
A FastAPI-based REST API for book management with JWT authentication, role-based access control, and review system
```

## Medium Description
```
Bookly - A modern REST API built with FastAPI for managing books, users, and reviews. Features JWT authentication, role-based access control, token revocation via Redis, and PostgreSQL database.
```

## Full Description

**Bookly** is a comprehensive REST API application built with FastAPI for managing a book catalog system. The application provides secure book management, user authentication, and review functionality with modern best practices.

### Key Features

- **Book Management**: Full CRUD operations for books with metadata (title, author, publisher, ISBN, price, availability)
- **User Authentication**: JWT-based authentication with access and refresh tokens
- **Role-Based Access Control**: Admin and user roles with protected endpoints
- **Token Management**: Redis-powered token blocklist for secure token revocation
- **Review System**: Users can create and manage book reviews
- **Database**: PostgreSQL with SQLModel ORM and Alembic migrations
- **Async Operations**: Fully asynchronous API using asyncpg and async SQLAlchemy

### Tech Stack

- **Framework**: FastAPI
- **Database**: PostgreSQL with SQLModel
- **Cache/Blocklist**: Redis
- **Authentication**: JWT (JSON Web Tokens)
- **Migrations**: Alembic
- **Python**: 3.14+

### API Endpoints

- `/api/v1/books` - Book management (protected)
- `/api/v1/auth` - Authentication (register, login, refresh)
- `/api/v1/reviews` - Review management (protected)
- `/health` - Health check endpoint
