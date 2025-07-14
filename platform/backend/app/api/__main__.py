import uvicorn
from main import app

# Used for starting in IDE
uvicorn.run(app, host="0.0.0.0", port=8000)
