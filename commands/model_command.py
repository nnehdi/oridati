import asyncio
from prisma import Prisma

import asyncio
from prisma import Prisma
import prisma.models as m
import inspect


def find_models(model_module):
    models = list()
    for name, obj in inspect.getmembers(model_module):
        if inspect.isclass(obj) and obj.__module__.startswith("prisma.models"):
            models.append(obj)
    return models


async def list_models():
    prisma = Prisma()
    await prisma.connect()

    models = find_models(m)
    await prisma.disconnect()

    return [model.__name__ for model in models]


def model_command(args):
    models = asyncio.run(list_models())
    print(models)
