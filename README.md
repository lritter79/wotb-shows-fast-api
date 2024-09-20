"""
This module sets up a FastAPI application with MongoDB integration using Motor, an async MongoDB driver.

Functions:

- lifespan(app: FastAPI): Async context manager for managing the application's lifespan, including connecting to and disconnecting from MongoDB.
- root(): Endpoint that returns a simple "Hello World" message.
- read_shows(): Endpoint that retrieves a list of shows from the database.
- read_show(show_id: str): Endpoint that retrieves a specific show by its ID.
- create_show(show: Show): Endpoint that creates a new show in the database.
- update_show(show_id: str, show: Show): Endpoint that updates an existing show in the database.
- delete_show(show_id: str): Endpoint that deletes a show from the database.
- get_dummy(): Endpoint that returns a dummy response with a generated ObjectId and the current datetime.
- main(argv): Main function to run the FastAPI application, currently commented out.

Classes:

- NewShowResponse: Pydantic model for the response of creating a new show.
- DummyResponse: Pydantic model for the dummy response.
  """

How To Run:

- Activate python virtual environment
- Install requirements with `pip install -r requirements.txt`
- Run `fastapi dev main.py`
