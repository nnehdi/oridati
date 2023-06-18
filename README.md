**PROOF OF CONCEPT**

# Data Origami
Rquirements part of the code base
Data Origami is going to be a minimal python tool for designing data model and exposing it via API at the speed of light. It uses LLM to generate the data model (.prisma) based on user requirements, then it will Python Prisma library and Fast API to dynamically create the API to serve the data. 

```
Let's get started! What is the focus of your data model? Which entities or users do you want to focus on?
> A platform similar to Resident Advisor that provides information about upcoming music events, festivals, and concerts. The platform would allow users to search for events by location, genre, and date, and would provide detailed information about each event, including the lineup, venue, and ticket prices. Users could also create profiles to track their favorite artists and receive personalized recommendations for events based on their music preferences. The platform could generate revenue through ticket sales and partnerships with event organizers and sponsors. 
🪴 Great! Let's start by focusing on the entities involved in this platform. From what you've described, it seems like we have at least two entities: "Events" and "Users". Are there any other entities that you can think of?
> venues, promoters, artists, tickets, genere
🪴 Excellent! So we have five entities: "Events", "Users", "Venues", "Promoters", "Artists", "Tickets", and "Genre". 

Now let's move on to identifying the relationships between these entities. Can you think of any relationships between these entities? For example, does an event have a venue? Does a user have a favorite artist?
> Users can search for events based on the promoters, date , locations, line up , genre
🪴 Great! So we have a few relationships here:
- A user can search for events based on the promoter, date, location, lineup, and genre.
- An event has a venue.
- An event has a promoter.
- An event has a lineup of artists.
- An event has tickets.
- An event can have multiple genres.
- A user can have favorite artists.

Are there any other relationships that you can think of?
> users can attend events by buying tickets. promoters and veneue owners can create events. 
🪴 Great! So we have a few more relationships:
- A user can attend an event by buying tickets.
- A promoter can create an event.
- A venue owner can create an event.

Now that we have identified the relationships between the entities, let's move on to specifying the type of relationships and attributes. For example, what attributes does an event have? What attributes does a user have?
> an event can have genre, data, line up of artists. user can have favorite artists
🪴 Great! So we have a few attributes:
- An event has a genre, date, and lineup of artists.
- A user has favorite artists.

Are there any other attributes that you can think of? Also, let's specify the type of relationships between the entities. For example, is the relationship between an event and a venue a one-to-one relationship or a one-to-many relationship?
> idk, you guess
🪴 Sure, I can make some assumptions based on what we've discussed so far. 

Let's assume that:
- An event can have multiple genres, and a genre can be associated with multiple events. This is a many-to-many relationship.
- An event can have multiple artists in its lineup, and an artist can perform at multiple events. This is also a many-to-many relationship.
- An event can have multiple tickets, and a ticket can be associated with only one event. This is a one-to-many relationship.
- A user can have multiple favorite artists, and an artist can be favored by multiple users. This is a many-to-many relationship.
- An event can have only one venue, but a venue can host multiple events. This is a one-to-many relationship.
- A promoter can create multiple events, but an event can have only one promoter. This is a one-to-many relationship.
- A venue owner can create multiple events, but an event can have only one venue owner. This is also a one-to-many relationship.

Does this make sense to you?
> yes
🪴 Great! Now that we have specified the relationships and attributes, let's summarize the data model we have created so far:

model Event {
  id        Int       @id @default(autoincrement())
  name      String
  date      DateTime
  genres    Genre[]   @relation("EventGenres")
  lineup    Artist[] @relation("EventLineup")
  tickets   Ticket[]
  venue     Venue     @relation(fields: [venueId], references: [id])
  venueId   Int
  promoter  Promoter  @relation(fields: [promoterId], references: [id])
  promoterId Int
}

model User {
  id            Int       @id @default(autoincrement())
  name          String
  favoriteArtists Artist[] @relation("UserFavoriteArtists")
}

model Venue {
  id        Int       @id @default(autoincrement())
  name      String
  address   String
  events    Event[]   @relation("VenueEvents")
  owner     VenueOwner @relation(fields: [ownerId], references: [id])
  ownerId   Int
}

model Promoter {
  id        Int       @id @default(autoincrement())
  name      String
  events    Event[]   @relation("PromoterEvents")
}

model Artist {
  id        Int       @id @default(autoincrement())
  name      String
  events    Event[]   @relation("EventLineup")
  users     User[]    @relation("UserFavoriteArtists")
}

model Ticket {
  id        Int       @id @default(autoincrement())
  price     Float
  event     Event     @relation(fields: [eventId], references: [id])
  eventId   Int
}

model Genre {
  id        Int       @id @default(autoincrement())
  name      String
  events    Event[]   @relation("EventGenres")
}

model VenueOwner {
  id        Int       @id @default(autoincrement())
  name      String
  venues    Venue[]   @relation("VenueOwnerVenues")
}
```

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
manage.py gather # a chatbot to desgin and generate the datamodel by interviewing the user 

manage.py model # print the name of generated models.

manage.py data # create few sample data for all entities defined by datamodel.
```

## Design
The project includes three realm each one containing different entities. Command line interfce provide tools for managing and translating these entities.
<-> Conversations between users and AI agent. Conversations are used as the main requirements for the desing.
<-> Data Model in a declarative language + Sample Data 
<-> Static or dyanamic code generation

### Conversation  
conversation are the core assets of a Origami project and kept and maintainted as a part of the source code.
- They are representing the conversation that can happen in a requirement gathering or analysing and desiging session.
- They contain enough information for generating the final datamodel and API.
- They can be converted to different format for ease of read.
- They are usually generated or manipulated with the command line tools which powered by LLMs.

#### File format
A Domain Specific Language to store LLMs chat data. It's very simple for now.
I want to call it Talk Flow :)

```talkflow
User: Hello, how are you?
User: Can you recommend a good restaurant nearby?
Assistant: Sure! What type of cuisine are you interested in?
User: I'm in the mood for Italian food.
Assistant: There's a great Italian restaurant called 'Pasta Paradise' nearby. Would you like more information?
```


### Data model and sample data
schemas are defined in .Prisma format. Examples are in .json format.

#### File format
I'm using .prisma and .json format for models and data.
but I'm thinking to create a more concise format to present both models and samples.
[User(id=3, name='mehdi', email='mehdi@example.com', password='something', location='somewhere', events=None), User(id=4, name='mehdi4', email='mehdi4@example.com', password='something', location='somewhere', events=None)]

### Code
Using Prisma Python as the ORM and FastAPI to dynamically create the APIs.


### Tasks
- generate data sample and write it into database

