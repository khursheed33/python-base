# app/routers/user_route.py

from fastapi import APIRouter,HTTPException
from app.models.user_model import UserModel
from app.constants.route_paths import RoutePaths
from app.routers.route_tags import RouteTags
from app.utils.extract_data import extract_data
from pathlib import Path
import subprocess
from datetime  import datetime
import time
from app.utils.file_system import FileSystem

class TestRouter():
    def __init__(self):
        self.router = APIRouter(prefix=RoutePaths.API_PREFIX)
        self.setup_routes()

    def setup_routes(self):
        @self.router.get(RoutePaths.TESTS, tags=[RouteTags.TESTS])  # Update the path to include the prefix
        async def tests():
            try:
                start = time.time()
                test_command = ["pytest", 'tests']
                subprocess.call(test_command)
                create_converage_commnad = ['coverage', 'json', '-i', '--pretty-print']
                subprocess.check_output(create_converage_commnad)
                time.sleep(1.0)

                coverage_totals = extract_data(path=Path("coverage.json"))
                end = time.time()
                elapsed = end - start
                coverage_totals.update({'elapsed_time': elapsed})
                # Delete coverage file after use
                FileSystem.delete_file(file_path='coverage.json')
                return coverage_totals
            except Exception as e:
                print(f"Error: {e}")
                raise HTTPException(status_code=500, detail=f"Error running pytest: {e}")
        
        # @self.router.get(RoutePaths.CONVERAGE,tags=[RouteTags.PING])
        # async def get_coverage_report(response: Response):
        #     with open("htmlcov/index.html", "r") as f:
        #         html_content = f.read()
        #         return HTMLResponse(content=html_content, status_code=200)
            
        # @self.router.get(f"{RoutePaths.CONVERAGE}/{{file_path:path}}")  
        # async def serve_static_file(file_path: str):
        #     try:
        #         return FileResponse(f"htmlcov/static/{file_path}")
        #     except FileNotFoundError:
        #         raise HTTPException(status_code=404, detail="File not found")
