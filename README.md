# Django SSO Engine

The Django SSO Engine is a Single Sign-On (SSO) solution that provides a centralized 
authentication service for all applications within your organization. It allows users 
to log in once and access multiple services without the need to re-enter their credentials.

## Features
- **Centralized Authentication**: Users authenticate in one place and gain access to all 
- **FineTuned Control**: Users in the system decides which all information (features) should be shared with the services connected to the SSO Engine.
- **Easy Integration**: Seamlessly integrate the SSO Engine with your Django applications and other web services.
- **Security**: Protect sensitive user information and ensure secure authentication and authorization.
- **User Management**: Manage users, roles, and permissions from a central dashboard.

## Getting Started
These instructions will help you get your Django SSO Engine up and running on your local 
machine for development and testing purposes. See deployment for notes on how to deploy the 
project on a live system.

### Prerequisites

- Python 3.10 []
- Django==4.2.6 
- Pillow==10.1.0
- requests==2.31.0

### Installation

1. Clone the repository:

   ```sh
   git clone https://github.com/your-organization/Django-SSO-Engine.git
   cd Django-SSO-Engine
   ```
2. Install dependencies:
    ```sh
    pip install -r requirements.txt
    ```
3. Configure your settings in `settings.py`.

4. Apply migrations:
    ```sh
    python manage.py migrate
    ```
5. Run the development server:
    ```sh
    python manage.py runserver
    ```

Now, you should have your SSO Engine up and running on http://localhost:8000/. 
You can access the admin interface at http://localhost:8000/admin/ to manage users 
and configure services.

## Usage
This is an independent SSO Server, Which can be used with any of your web application, regardless of PHP, Python, NodeJs or any of your favorite one.

### How to use
1. Deploy `Django SSO Engine` into your server.
2. Create a super admin account and Login.
3. Log on to `/admin/sso/client/add/` to create a new Client
   - Redirection URL is the complete url where you want to get the call back with get parameters.
   - On Saving, You will get an `APP_KEY` and `APP_SECRET`, Using which you can communicate to the server anytime.
4. From your frontend, you can redirect to SSO Server. (`/sso/web/{api_key}/`) 
   - Your user will login to the account, 
   - Will give the permissions, 
   - and get back to you with a `txn_token` to your "`redirection_url`"  
   - This webhook will contains 2 parameters `auth_token` and `state`
   - `state` will be having one of `SUCCESS` or `TERMINATED`
   - You can use `auth_token` to get the user details using API (`/sso/web/{auth_token}/verify-details/`). But this requires both `APP_KEY` as `X-ApiKey` Header and `APP_SECRET` as `X-ApiSecret` Header.
5. The response on `verify-details` API, will be having the following response structure in API Documentation
6. If you are using python, (Or you can implement the same logic in your native language and update in this code inside `/contrib/clients/<compiler>/` folder )
   - Feel free to use this `SSOAgent` snippet to control the packages.
   - Feel free to use the `sso_callback_for_other_python_frameworks` view function.

7. If you are using Django, there is another snippet for Authentication Backend, along with the



### Example Implementation
I can get a sample repository which used this sso service: 
**[Django SSO Engine Client](https://github.com/jerinisready/django-sso-engine--client)**

### How to integrate
For Python, Add the service file into `ssoengine/service.py` and refer each folder for more details.
- [Django](./contrib/clients/python/django_view)
- [FastAPI](./contrib/clients/python/fastapi_view)
- [Flask](./contrib/clients/python/flask_view)



## Deployment
Describe how to deploy the Django SSO Engine on a live system. This might include information 
on setting up a production database, web server, and other deployment-specific steps.



## API Documentation

### verify-details:: API Structure

| Field                       | Datatype             | Description                                                                                                         |
|-----------------------------|----------------------|---------------------------------------------------------------------------------------------------------------------|
| `state`                     | `str`                | Will be detailed in the below table                                                                                 |
| `auth`                      | `Optional[obj]`      | Will be there only if state is `VERIFIED`                                                                           |
| `auth.features`             | `obj`                |                                                                                                                     |
| `auth.features.username`    | `Any`                | Any of the things inside Features is decided by the Feature model entry, and user have to give access for the same. |
| `auth.features.first_name`  | `Any`                |                                                                                                                     |
| `auth.features.last_name`   | `Any`                |                                                                                                                     |
| `auth.features.email`       | `Any`                |                                                                                                                     |
| `auth.permitted_features`   | `List[str]`          | list of permitted features by the User.                                                                             |
| `txn_date`                  | `Optional[datetime]` | datetime of transaction in GMT if valid.                                                                            |
| `txn_id`                    | `Optional[str]`      | txn_id, which you have shared.                                                                                      |
|                             |                      |                                                                                                                     |
  

### verify-details:: STATES  in detail
| State                 | Description                                                                                                   |
|-----------------------|---------------------------------------------------------------------------------------------------------------|
| `VERIFIED`            | All Ok                                                                                                        |
| `EXPIRED`             | You have to collect information within preconfigured time (defaults to 8 minutes)                             |
| `INCOMPLETE`          | User have not completed authentication                                                                        |
| `INVALID_ID`          | `auth_token` provided is an invalid one                                                                       |
| `UNAUTHORIZED`        | You are not authorized to access this `auth_token` as this token is generated as a part of some other client. |
| `INVALID_CREDENTIALS` | Your `APP_KEY` or `APP_SECRET` is wrong.                                                                      |



## Contributing
We welcome contributions from the community. Please read our Contribution Guidelines for 
details on how to contribute to this project.

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.


## Contact
For questions or support, please contact `Jerin John` at [jerinisready@gmail.com](mailto:jerinisready@gmail.com).

For bug reports or feature requests, please open an issue on the GitHub repository.

