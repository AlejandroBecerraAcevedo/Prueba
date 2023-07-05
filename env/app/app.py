from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from beanie import init_beanie
from motor.motor_asyncio import AsyncIOMotorClient


from app.core.config import settings
from app.models.todo_model import Todo
from app.models.user_model import User
from app.api.api_v1.router import router


app = FastAPI(
    title = settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json"
)



@app.on_event("startup")
async def app_init():
    
    """
        initialize crucial aplication services
    """
    db_client = AsyncIOMotorClient(settings.MONGO_CONNECTION_STRING).fodoist # Conecion a la base de datos de nombre fodoist

    await init_beanie(   

        database=db_client,     # inicializar la libreria ODM( Object Document Mapper) para la base de datos con los modelos User y Todo
        document_models=[
            User,
            Todo
        ]    
    )

app.include_router(router,prefix=settings.API_V1_STR) # incluir el router de la api en la aplicacion
    
