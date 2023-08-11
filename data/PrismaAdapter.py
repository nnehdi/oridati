from prisma import Prisma
import inspect
from helpers import SingletonMeta

class PrismaAdapter(meta=SingletonMeta):
    def __init__(self):
        self._prisma = Prisma()
        self._models = dict()

    def find_models(self):
        if self._models:
            return list(self._models.values())

        import prisma.models as model_module

        for name, obj in inspect.getmembers(model_module):
            if inspect.isclass(obj) and obj.__module__.startswith("prisma.models"):
                self._models[name] = obj
        return list(self._models.values())

    def _db(self, model):
        return getattr(self._prisma, model.__name__.lower())

    def find_by_id(self, model, id):
        self._prisma.connect()
        res = self._db(model).find_first(where={"id": id})
        self._prisma.disconnect()
        return res

    def find_all(self, model):
        self._prisma.connect()
        res = self._db(model).find_many()
        self._prisma.disconnect()
        return res

    def create(self, model, id, object):
        obj_dict = dict()
        obj_dict["id"] = id
        for key, value in dict(object).items():
            if value and not isinstance(value, (list, dict)):
                obj_dict[key] = value

        res = None
        self._prisma.connect()
        res = self._db(model).create(dict(obj_dict))
        self._prisma.disconnect()
        return res

    def delete(self, model, id):
        self._prisma.connect()
        res = self._db(model).delete(where={"id": id})
        self._prisma.disconnect()
        return res

    def get_model(self, model_name):
        return self._models[model_name]

    def create_samples(self, sample_data):
        self._prisma.connect()
        batcher = self._prisma.batch_()
        for record in sample_data:
            command = record.pop("_command")
            model_name = record.pop("_type")
            print(f"processing {command} : {model_name}")
            if command == "create":
                print(f"creating {record}")
                clean_record = dict()
                for key, value in record.items():
                    if not isinstance(value, (list, dict)):
                        clean_record[key] = value
                getattr(self._prisma, model_name.lower()).create(clean_record)
            else:  # command == 'update':
                print(f"updating {record}")
                getattr(self._prisma, model_name.lower()).update(
                    where=record["where"], data=record["data"]
                )
        batcher.commit()
        self._prisma.disconnect()


if __name__ == "__main__":
    adapter = PrismaAdapter()

    models = adapter.find_models()
    print(models)

    user_model = adapter.get_model("User")
    # adapter.create(user_model, {
    #     'id': 6,
    #     'name': 'mehdi5',
    #     'email': 'mehdi6@example.com',
    #     'password': 'something',
    #     'location': 'somewhere',
    # })
    print(adapter.find_all(user_model))

    import json

    with open("samples.json", "r") as fn:
        adapter.create_samples(json.loads(fn.read()))
