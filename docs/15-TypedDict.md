# TypedDict

Repository layer: Returns the dictionary to the service using the `.mappings()` method(have not do yet)

Service layer: Receives the dictionary, uses TypedDict to get type hints, executes some code, and returns a dictionary.

Route layer: Receives a dictionary, validates it based on validator, and returns a JSON response.