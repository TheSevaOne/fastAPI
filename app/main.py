import fastapi
from .app import app_router

def router(obj):
	obj.include_router(app_router)
def start():
	app = fastapi.FastAPI(title='test_task',version='1.0')
	router(app)
	return app 

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:start", port=5000, log_level="info")