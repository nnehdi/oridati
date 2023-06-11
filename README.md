**It's a Draft project**

# Data Origami

Data Origami is going to be a minimal python tool for designing data model and exposing it via API at the speed of light. The magic happens behind the scene leveraging the power of Generative Language Models.

## Visions
- Bootstraping the base design based on the requirements.
- Helping to clear out the requirements by asking multiple questions.
	- Keeping the project requirement in a file. 
	- Creating a session by starting asking multiple question based on the requirements to create a new version of the requirements. Help users to figure out what needs to be clear and what should be changed.
	- Showing a diff between the old and the new requirements. Apply all or part of the changes to update the requirements.
- Generate sample data both for documentation and for prototyping 
- User requirements and sample data are actually part of the code base.
- A library of pre-defined project and data models.

### CLI
```shell
origami req 

origami model 

origami data

origami code
```

## Design
The project includes three domain each one containing different entities. Command line interfce provide tools for managing and translating these entities.
<-> Requirements in plain text 
<-> Data Model in a declarative language + Sample Data 
<-> Static or dyanamic code generation

### Requirements  
In a specific layout(?), written and maintained in Markdown.
- Layout
	- Summary
	- User stories
	- Users
	- Entities
- reqs.md <=> models.prisma
	- Updateing the req file via CLI 
		- update the model to reflect the changes.
	- editing the .prisma
		- update the req file
	- using diff or the whole file?
- A workflow to clarify and expand the model.


### Data model and sample data
schemas are defined in .Prisma format. Examples are in .json format.

### Code
Using Prisma Python as the ORM and FastAPI to dynamically create the APIs.


### Tasks
- reqs.md <=> models.prisma
	- Expriement with OpenAI API to develop a requirement (in plain English) to datamodel (.Prisma) model. 
	- Find an efficient requirement layout.
- Develop a workflow for expanding the requirements

