from prisma import Prisma
import inspect 

class PrismaAdapter:
    def __init__(self):
        self._prisma = Prisma(auto_register=True)

    def find_models(self):
        import prisma.models as model_module

        models = list()
        for name, obj in inspect.getmembers(model_module):
            if inspect.isclass(obj) and obj.__module__.startswith('prisma.models'):
                models.append(obj)
        return models
    
    def find_all(self, model):
        self._prisma.connect()
        res = model.prisma().find_many()
        self._prisma.disconnect()
        return res

    def create(self, model, data):
        self._prisma.connect()
        model.prisma().create(data)
        self._prisma.disconnect()

if __name__ == "__main__":
    adapter = PrismaAdapter()

    models = adapter.find_models()
    print(models)

    # adapter.create(models[1],{
    #     'username':'nnehdi',
    #     'email':'nnehdi@example.com',
    #     'password':'something',
    #     'role': 'seller'
    # })

    print(adapter.find_all(models[1]))
    