from prisma import Prisma
import inspect


class PrismaAdapter:
    def __init__(self):
        self._prisma = Prisma(auto_register=True)
        self._models = dict()

    def find_models(self):
        if self._models:
            return list(self._models.values())

        import prisma.models as model_module
        for name, obj in inspect.getmembers(model_module):
            if inspect.isclass(obj) and obj.__module__.startswith('prisma.models'):
                self._models[name] = obj
        return list(self._models.values())

    def find_all(self, model):
        self._prisma.connect()
        res = model.prisma().find_many()
        self._prisma.disconnect()
        return res

    def create(self, model, data):
        self._prisma.connect()
        model.prisma().create(data)
        self._prisma.disconnect()

    def get_model(self, model_name):
        return self._models[model_name]

    def create_samples(self, sample_data):
        self._prisma.connect()
        batcher = self._prisma.batch_()
        for record in sample_data:
            command = record.pop('_command')
            model_name = record.pop('_type')
            print(f'processing {command} : {model_name}')
            if command == 'create':  
                print(f'creating {record}')
                for key, value in record.items():
                    if isinstance(value,(list,dict)):
                        record.pop(key)
                self.get_model(model_name).prisma().create(record)
            else: # command == 'update':  
                print(f'updating {record}')
                self.get_model(model_name).prisma().update(where = record['where'],data=record['data'])
        batcher.commit()
        self._prisma.disconnect()

if __name__ == "__main__":
    adapter = PrismaAdapter()

    models = adapter.find_models()
    print(models)

    user_model = adapter.get_model('User')
    # adapter.create(user_model, {
    #     'id': 6,
    #     'name': 'mehdi5',
    #     'email': 'mehdi6@example.com',
    #     'password': 'something',
    #     'location': 'somewhere',
    # })
    print(adapter.find_all(user_model))

    import json
    with open('samples.json', 'r') as fn:
        adapter.create_samples(json.loads(fn.read()))
    