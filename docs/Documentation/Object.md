## Object Class Documentation for TimeBandit

### Overview
An object in TimeBandit is a fundamental component represented as a specialized node within the simulation. 

It is designed to hold and update its state over time, existing within a defined Space and anchored to a specific Point in Time. 

Objects can be interconnected with other agents in the same space, allowing for the modeling of various phenomena such as weather patterns, population growth, city traffic flow, or disease spread.

### Class: `Object`
The `Object` class encapsulates the state and behavior of an object within the simulation, including its temporal dynamics and interactions with other components.

#### Attributes
- **steps_size (int)**: Defines the number of steps per cycle. For example, if `steps_size` is 5, a cycle is counted every 5 steps.
- **clock (Clock)**: Manages the relative time of the object in terms of cycles and steps.
- **root_id (str)**: A unique identifier for the object.
- **temporal_id (str)**: A unique identifier that combines the `root_id` and the current state of the clock, representing a specific instance of the object.
- **state (TemporalState)**: Holds buffered previous states of the object.

#### Methods
- **update()**: Updates the state of the object.
- **encode()**: Encodes the current state of the object into a unique identifier.
- **id(root: bool = False)**: Returns the identifier of the object. By default, it returns the `temporal_id`; if `root` is `True`, it returns the `root_id`.
- **save(path: str)**: Serializes the object and saves it to a file specified by the path.
- **load(path: str)**: Deserializes and loads the object from a specified file.

#### Properties
- **record_state**: Returns the current state of the object as a `State` instance.
- **cycle**: Returns the current cycle of the object.
- **step**: Returns the current step of the object.

### Detailed Method Descriptions

#### `__init__(self, steps_size: int = 1) -> None`
Initializes a new instance of the `Object` class.
- **Parameters**:
  - `steps_size (int)`: Number of steps per cycle.

#### `__str__(self) -> str`
Returns a string representation of the object.
- **Returns**: `str`

#### `__repr__(self) -> str`
Returns a detailed string representation of the object for debugging purposes.
- **Returns**: `str`

#### `update(self) -> dict`
Updates the state of the object and increments the clock.
- **Returns**: `dict`: The updated state of the object.

#### `encode(self) -> str`
Generates a unique identifier based on the current state of the object.
- **Returns**: `str`: The encoded identifier.

#### `id(self, root: bool = False) -> str`
Returns the identifier of the object.
- **Parameters**:
  - `root (bool)`: If `True`, returns the `root_id`; otherwise, returns the `temporal_id`.
- **Returns**: `str`: The object's identifier.

#### `save(self, path: str) -> str`
Serializes the object and saves it to a specified file path.
- **Parameters**:
  - `path (str)`: The file path where the object will be saved.
- **Returns**: `str`: The full path of the saved file.

#### `load(cls, path: str) -> "Object"`
Class method to load an object from a specified file.
- **Parameters**:
  - `path (str)`: The file path from where the object will be loaded.
- **Returns**: `Object`: The loaded object instance.

#### `record_state(self) -> State`
Property to return the current state of the object.
- **Returns**: `State`: A dict-like object containing the current state.

#### `cycle(self) -> int`
Property to return the current cycle of the object.
- **Returns**: `int`

#### `step(self) -> int`
Property to return the current step of the object.
- **Returns**: `int`