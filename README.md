# adventure

Conceived as an airplane project (a diversion during long, typically delayed airline travel), adventure is a text adventure framework built on python and MongoDB. It will provide a series of classes defining characters, locations, etc. as well as a command parser to allow a player to interact with the created world. Game files will be persisted as JSON files that the engine will read and write on demand.

## Why MongoDB?

Typically, using a NoSQL database to model a series of relational entities is a Bad Idea. Nevertheless, MongoDB provides a fast and lightweight persistance layer that, with some thoughtful document-design, will not cause any major obstacles. The key here will be to minimize the number of relations that need to be loaded from any object at any given moment in time.

Besides, I wanted to experiment with Mongo. So there's that.
