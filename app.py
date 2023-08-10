from data.PrismaAdapter import PrismaAdapter
from fastapi import FastAPI, APIRouter, Depends
from fastapi.responses import RedirectResponse
from collections import namedtuple

RouteConfig = namedtuple('Route Config', ['methods', 'path', 'endpoint'])
def route_name(model):
    return model.__name__.lower() + "s"


def get_prisma_adapter():
    db_adapter = PrismaAdapter()
    return db_adapter


def build_get_by_id_route(model):
    async def handler(
        record_id: int, db_adapter: PrismaAdapter = Depends(get_prisma_adapter)
    ):
        return adapter.find_by_id(model, record_id)

    return RouteConfig(
        ["GET"],
         f"/{route_name(model)}/{{record_id}}",
         handler,
    )


def build_del_by_id_route(model):
    async def handler(
        record_id: int, db_adapter: PrismaAdapter = Depends(get_prisma_adapter)
    ):
        return adapter.delete(model, record_id)

    return RouteConfig( 
        ["DELETE"],
        "/{route_name(model)}/{{record_id}}",
        handler,
     )


def build_get_all_route(model):
    async def handler(
        skip: int = 0,
        limit: int = 100,
        db_adapter: PrismaAdapter = Depends(get_prisma_adapter),
    ):
        print(type(adapter.find_all(model)[0]))
        return adapter.find_all(model)

    return RouteConfig(["GET"], f"/{route_name(model)}/", handler)


def build_create_route(model):
    async def handler(
        record_id: int,
        record: model,
        adapter: PrismaAdapter = Depends(get_prisma_adapter),
    ):
        return adapter.create(model, record_id, record)

    return RouteConfig( 
        ["POST"], f"/{route_name(model)}/{{record_id}}",
        handler,
     )


ROUTES_PER_MODEL = [
    build_get_all_route,
    build_get_by_id_route,
    build_create_route,
    build_del_by_id_route,
]


def create_router(model):
    model_router = APIRouter()
    for route_builder in ROUTES_PER_MODEL:
        model_router.add_api_route(**route_builder(model))
    return model_router


def create_root_router():
    async def redirect_docs():
        return "/docs"
    redirect_docs = app.get("/", response_class=RedirectResponse)(redirect_docs)

    root_router = APIRouter()
    root_router.add_api_route("/", redirect_docs)
    return root_router


def create_app(prisma_adapter):
    app = FastAPI()
    app.include_router(create_root_router())
    for model in prisma_adapter.find_models():
        app.include_router(create_router(model))
    return app


adapter = PrismaAdapter()
app = create_app(adapter)
