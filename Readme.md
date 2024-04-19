# Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/CaptainVee/divic.git
    ```
2. Create and activate a virtual environment:

   ```sh
   $ python3 -m venv venv && source venv/bin/activate
   ```

3. Install dependencies:
    ```bash
    cd divic
    pip install -r requirements.txt
    ```

4. Apply migrations:
    ```bash
    python manage.py makemigrations
    python manage.py migrate
    ```

5. Start the development server:
    ```bash
    python manage.py runserver
    ```



# Features
1. **Hook System:**
You can find the hooks in  [core/signals.py](core/signals.py)

once the applications is started with the `runserver` command, it executes 3 functions which prints out a text

Also when you run the migration command using `python manage.py migrate`, the `before_migrate` and `after_migrate` hooks are called before and after the migration respectively. All functions in the hooks are awaited using asynchronous programming

2. **CLI for Model Creation**

The `create_model` command helps create new models with basic structure
```bash
python manage.py create_model User
```
You can also specify fields to add to the model using the --fields flag

```bash
python manage.py create_model User --fields name:str age:int
```
This will create a directory named `models/User` with the following files:

* `User.py`: A model class inheriting from `Document`.
* `User.json`: A JSON file for defining model properties.


3. **API Endpoint:**
You can access the API endpoint through Postman using the url `api/v1/retrieve-data/`
and pass in your payload in the body eg
```json
{
    "modelName": "Document",
    "fields": ["file_name", "id"],
    "filters": {"file_name": ["==", "book"],
                "created_at": [">=", "1-1-2023"]}

}
```