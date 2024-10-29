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

## Form Routes
### `/forms` [GET, POST]
- **GET**: Returns a list of all forms.
- **POST**: Creates a new form with the data sent in the body of the request, including title, color, image, associated group ID, and a list of components. the forms.
### `/forms/<int:form_id>` [GET, PUT, DELETE]
- **GET**: Returns data for a specific form based on form_id.
- **PUT**: Update an existing form.
- **DELETE**: Remove a form from the database.
### `/forms/<int:form_id>/components` [GET, POST]
- **GET**: Returns all components of a specific form.
- **POST**: Adds a new component to the form, including type, title, and options if any.
### `/forms/<int:form_id>/components/<int:component_id>` [DELETE]
- **DELETE**: Removes a specific component from a form.
### `/components/<int:component_id>/options` [GET, POST]
- **GET**: Returns all options for a specific component.
- **POST**: Adds a new option to the component.
### `/components/<int:component_id>/options/<int:option_id>` [DELETE]
- **DELETE**: Removes a specific option from a component.
### Request Examples

#### Create a form (POST /forms)
```json
{
    "title": "Pesquisa de Satisfação",
    "color": "#ff5733",
    "image": "",
    "group": 1,
    "components": [
        {
            "type": "multiple",
            "title": "Como você avalia o ambiente de trabalho?",
            "options": ["Excelente", "Bom", "Razoável", "Ruim"]
        },
        {
            "type": "text_field",
            "title": "Sugestões para melhorias",
            "options": []
        }
    ]
}
```
#### Add a component to a form (POST /forms/1/components)
```json
{
    "type": "single_field",
    "title": "Qual é o seu setor de trabalho?",
    "options": []
}
```
#### Add an option to a component (POST /components/1/options)
```json
{
    "option": "Muito Satisfeito"
}
```