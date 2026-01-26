from fastapi import FastAPI
from testdebiritservice.api.routes import router

app = FastAPI(title="Deribit Price Service")

app.include_router(router)
