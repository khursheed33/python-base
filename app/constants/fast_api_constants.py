class FastAPIConstants:
    TITLE="Python Base | Server"
    DESCRIPTION="""
Welcome to the Python Base Server with FastAPI! This base server is designed to provide you with all the necessary components to kickstart your development process. Whether you're building a web application, API, or leveraging Generative AI, this base server has got you covered.

## Features

### Generative AI Wrapper
- **Langchain Wrapper**: Includes various Language Model (LLM) wrappers, allowing you to easily integrate Generative AI capabilities into your applications. With pre-built models and utilities, you can harness the power of Generative AI with ease.

### Database Wrapper
- **MongoDB**: Utilize MongoDB, a popular NoSQL database, for flexible and scalable data storage.
- **PostgreSQL**: Benefit from the robustness and reliability of PostgreSQL, a powerful open-source relational database system.
- **MSSQL**: Seamlessly integrate with Microsoft SQL Server for enterprise-grade database management.
- **Local**: Access a lightweight local database option for rapid development and testing.

    """
    SUMMARY="Project Summary"
    VERSION="1.0.0"
    T_N_C="https://github.com/khursheed33"
    CONTACT={
        "name": "Khursheed",
        "url": "https://github.com/khursheed33",
        "email": "gaddi33khursheed@gmail.com",
    }
    LICENSE_INFO={
        "name": "Apache 2.0",
        "url": "https://www.apache.org/licenses/LICENSE-2.0.html",
    }

    OPENAPI_TAGS_METADATA = [
    {
        "name": "API Testings",
        "description": "Provides a route to run tests at deployment time."
    },
    {
        "name": "Authentication",
        "description": "Authentication and Authorization of Users"
    },
    {
        "name": "Health",
        "description": "Check health of the server"
    },
    {
        "name": "Ingestion",
        "description": "Manager Vector Embeddings: Create, Search and Delete"
    },
    {
        "name": "Chat",
        "description": "Chat with the ingested document"
    },
]