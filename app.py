from data.PrismaAdapter import PrismaAdapter
from fastapi import FastAPI, APIRouter, Depends


def route_name(model):
    return model.__name__.lower()+'s'


def get_prisma_adapter():
    db_adapter = PrismaAdapter()
    return db_adapter


def build_get_by_id_route(model):
    async def handler(
        record_id: int,
        db_adapter: PrismaAdapter = Depends(get_prisma_adapter)
    ):
        return adapter.find_by_id(model, record_id)

    return {'methods': ['GET'], 'path': f'/{route_name(model)}/{{record_id}}', 'endpoint': handler}


def build_del_by_id_route(model):
    async def handler(
            record_id: int,
            db_adapter: PrismaAdapter = Depends(get_prisma_adapter)
    ):
        return adapter.delete(model, record_id)
    return {'methods': ['DELETE'], 'path': f'/{route_name(model)}/{{record_id}}', 'endpoint': handler}


def build_get_all_route(model):
    async def handler(
        skip: int = 0,
        limit: int = 100,
        db_adapter: PrismaAdapter = Depends(get_prisma_adapter)
    ):
        print(type(adapter.find_all(model)[0]))
        return adapter.find_all(model)
    return {'methods': ['GET'], 'path': f'/{route_name(model)}/', 'endpoint': handler}


def build_create_route(model):
    async def handler(record_id: int, record: model, adapter: PrismaAdapter = Depends(get_prisma_adapter)):
        return adapter.create(model, record_id, record)

    return {'methods': ['POST'], 'path': f'/{route_name(model)}/{{record_id}}', 'endpoint': handler}


ROUTES_PER_MODEL = [
    build_get_all_route,
    build_get_by_id_route,
    build_create_route,
    build_del_by_id_route
]


def create_router(model):
    model_router = APIRouter()
    for route_builder in ROUTES_PER_MODEL:
        model_router.add_api_route(**route_builder(model))
    return model_router


def create_app(adapter):
    app = FastAPI()

    async def root():
        return {'msg': 'root'}
    app.add_api_route('/', root)

    for model in adapter.find_models():
        model_router = create_router(model)
        app.include_router(model_router)

    return app


adapter = PrismaAdapter()
app = create_app(adapter)

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
