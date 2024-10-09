# C-317 Project API

This API was developed with the aim of
interact with the project database, having user group tables and forms.

## User Routes
### `/users` [GET, POST]

- **GET**: Returns a list of all users.
- **POST**: Creates a new user with the data sent in the request body (name, phone_number, email, password, role, is_adm).

### `/users/`<int:id> [GET, PUT, DELETE]

- **GET**: Returns data from a specific user based on id.
- **POST**: Updates an existing user.
- **DELETE**: Removes a user from the database.

### Request Example
#### Create a user (POST `/users`)
```json
{
    "name": "John Doe",
    "phone_number": "+123456789",
    "email": "john.doe@example.com",
    "password": "securepassword",
    "role": "user",
    "is_adm": false
}
``` 

#### Get a specific user (GET `/users/1`)
This endpoint retrieves the user with ID 1.

#### Update a user (PUT `/users/1`)
```json
{
    "name": "John Doe Updated",
    "phone_number": "+987654321",
    "email": "john.updated@example.com",
    "role": "admin",
    "is_adm": true,
    "password": "newsecurepassword"
}
```
#### Delete a user (DELETE `/users/1`)
This endpoint removes the user with ID 1 from the database.

## Group routes
### `/groups` [GET, POST]

- **GET**: Returns a list of all groups.
- **POST**: Creates a new group with the data sent in the request body (name and description).

### `/groups/`<int:group_id> [GET, PUT, DELETE]

- **GET**: Returns data from a specific group based on `group_id`.
- **PUT**: Updates an existing group.
- **DELETE**: Removes a group from the database.

### `/groups/`<int:group_id>/users/<int:user_id> [POST, DELETE]

- **POST**: Adds a user (`user_id`) to a specific group (`group_id`).
- **DELETE**: Removes a user from a group.

### Request Example

#### Create a group (POST /groups)

```json
{
    "name": "Study Group",
    "description": "Group to discuss advanced topics."
}
```

#### Add a user to a group (POST `/groups/1/users/3`):
This endpoint adds user ID 3 to group ID 1.