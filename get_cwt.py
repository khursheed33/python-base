import os

def get_project_directory():
    # Get the absolute path of the current script
    current_script_path = os.path.abspath(__file__)

    # Navigate up two levels to reach the project directory
    project_directory = os.path.dirname(os.path.dirname(current_script_path))

    return project_directory