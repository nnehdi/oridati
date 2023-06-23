
# Web Origami
Web origami gives you a working API after helping you with analysing your requirements and desinging the datamodel.
It generates the data model (.prisma) based on user requirements, then it will use Python Prisma library and Fast API to dynamically create a set RESTful API endpoints. 

### How to use it
1. Have a conversation with a chatbot which helps you in analysing you requirements and designing the data model.
```shell
manage.py talk
``` 
Or edit the conversation file in the editor and get the response with the following command.
```shell
manage.py talk --complete
``` 
2. Generate the schema.prisma file, as well as the orm code. Then reflect the changes on the database.
```shell
manage.py talk --generate-schema
prisma db push
``` 
3. Generate some sample data and insert them into the database.
```shell
manage.py talk --generate-data
``` 
4. Launch daynamically created FastAPI app exposes endpoints for performing CRUD operation on different entities in the introduced datamodel. You can see an interactive OpenAPI documentaion by going to '/docs' path.
```shell
uvicorn app:app
``` 

### Visions
- Generating OpenAPI compatible clients in different languages.
- An ORM enabled interactive shell for playing with data.
- Deployable with containers to bare metal and clouds
- Standard configuration file
- CDN
- Auth
- Access management
- User management
- Emulating user interviews using chatbots
- Serverless function to support extended logics
- A library of pre-defined project and data models.
- Use Typer for command line
- Use Langchain 
- Pulblish the package on Pypy

## Tasks
- Put together all the implemented parts to work as described in the 'How to use it' section.
- 

