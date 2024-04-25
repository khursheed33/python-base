# FastAPI Project Template

This repository contains a template for creating a FastAPI project with structured organization and key features like error logging, environment variable configuration, and class-based API organization.

## Getting Started

Follow these instructions to set up and run the project on your local machine.

### Prerequisites

Make sure you have the following software installed on your machine:

- Python 3.7+
- pip (Python package manager)

### Installation

1. Clone the repository to your local machine:

   ```bash
   git clone https://github.com/yourusername/fastapi-project-template.git
   ```

2. Navigate to the project directory:

   ```bash
   cd fastapi-project-template
   ```

3. Install project dependencies using pip:

   ```bash
   pip install -r requirements.txt
   ```
4. Running the Server

To run the FastAPI server, execute the following command:

   ```bash
   uvicorn app:app --host ${APP_HOST} --port ${APP_PORT} --reload
   ```

### Configuration

1. Create a `.env` file in the root directory of the project.

2. Define your configuration variables in the `.env` file. Here's an example:

   ```plaintext
   # FastAPI settings
   APP_HOST=0.0.0.0
   APP_PORT=8000

   # Logging settings
   LOG_LEVEL=DEBUG
   LOG_FILE=log.log
   ```

### Running the Server

To run the FastAPI server, execute the following command:

   ```bash
   python app/main.py
   ```

By default, the server will listen on `0.0.0.0:8000` (or as configured in the `.env` file).

## Usage

Once the server is running, you can access the API documentation at `http://localhost:8000/docs`.

## Project Structure

- `app/`: Main application directory.
  - `main.py`: Entrypoint for the FastAPI application.
  - `routers/`: Directory to store router modules.
    - `user.py`: Router module for user-related endpoints.
    - `docs.py`: Router module for serving API documentation.
  - `templates/`: Directory to store HTML templates.
    - `swagger_ui.html`: HTML template for Swagger UI.
  - `settings.py`: Configuration settings for the application.
  - `decorators.py`: Custom decorators for error logging and other functionalities.
- `.env`: File to store environment variables.
- `requirements.txt`: List of Python dependencies for the project.

## Contributing

Feel free to contribute to this project by opening issues or pull requests. Any feedback or improvements are welcome!

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
