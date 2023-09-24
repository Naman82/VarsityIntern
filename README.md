# VarsityPro-Blogs

A backend application which consists of different APIs including User-Authentication, Blogs, Comments and the Search Functionality according to the assignment given.


## Hosted Link

`https://varsitypro-blog-naman.onrender.com/docs/`

### credentials
```bash
{
  "client_id": "37uBM0ge6W93vOIDunvvAjTg9DH9OqVyqDAj5A5C",
  "client_secret": "sLZ2jojtaFdfKSkliUVcCckkhTY0Ry7jEewfYzk50Ne3zxUweYXXJ8kZLq8Ut8zNUtkHMOce0OxQ7AKDt9CBAVHza9UmeuehgzcQuK2TrrkXSwg0ASQPNSEEL5lL7NMg",
  "grant_type": "password",
  "username": "user@example.com",
  "password": "string"
}

ADMIN PANEL : 

email: admin@mail.com
password: password
```

## Setup

To run application on your local machine, follow these steps:

1. Clone the repository from GitHub:
```bash
git clone https://github.com/Naman82/VarsityIntern.git
cd VarsityIntern
git branch development
```

2. Set up a virtual environment (optional but recommended):

```bash
python -m venv venv
source venv/bin/activate # On Windows: venv\Scripts\activate
```

3. Install the required Python packages:
```bash
pip install -r requirements.txt
```
4. Run the Django development server:
```bash
python manage.py runserver
```
5. Open your web browser and go to `http://localhost:8000/docs` to access APIs

6. Create a superuser using terminal:
```bash
python manage.py createsuperuser
```
```bash
email: admin@mail.com
user-type: 0 
password: abcd
```
user-type should be 0 for admin permissions.

7. Create client_id and client_secret, open your browser and go to `http://localhost:8000/admin`, using the above created credentials login into the admin panel.

8. Go to 'Applications' option and create a new entry, save/write-down the client_id and client_secret before saving the entry.
-user : choose admin
-client type : confidential
-authorization grant type : resource owner password-based

9. Test the APIs in Swagger or Postman.

# API Reference

This section provides details on how to interact with the API endpoints of our service.

## Base URL

All API endpoints are relative to the base URL:
`http://localhost:8000/api/` 
or
`https://varsitypro-blog-naman.onrender.com/docs/`

##Endpoints

### 1. Create New User

- **URL**: `/user-signup`
- **Method**: `POST`
- **Description**: User Signup API.

**Request:**
```http
POST /api/user-signup
Content-Type: application/json

{
  "email": "user@example.com",
  "password": "string"
}

```

### 2. User Login

- **URL**: `/user-login`
- **Method**: `POST`
- **Description**: User login API.

**Request:**
```http
POST /api/user-login
Content-Type: application/json

{
  "client_id": "YOUR_CLIENT_ID",
  "client_secret": "YOUR_CLIENT_SECRET",
  "grant_type": "password",
  "username": "user@example.com",
  "password": "string"
}

```
### 3.  Authentication

To access the API, you need to include your API key in the request headers:

```http
Authorization: Bearer YOUR_API_KEY
```

### 4. Get Blogs

- **URL**: `/blogs/`
- **Method**: `GET`
- **Description**: Get list of all blogs.

**Request:**
```http
GET /api/blogs/
```

### 5. Create Blog

- **URL**: `/blogs/`
- **Method**: `POST`
- **Description**: Create a new blog.

**Request:**
```http
POST /api/blogs/
Content-Type: application/json

{
  "title": "string",
  "meta_title": "string",
  "body": "string",
  "tags": "string"
}
```

### 6. Get a blog by ID

- **URL**: `/blog/{blog_id}`
- **Method**: `GET`
- **Description**: Get a blog by ID.

**Request:**
```http
GET /api/blog/{blog_id}
```

### 7. Edit Blog

- **URL**: `/blog/{blog_id}`
- **Method**: `PATCH`
- **Description**: Edit a existing blog.

**Request:**
```http
PATCH /api/blog/{blog_id}
Content-Type: application/json

{
  "title": "string", (optional)
  "meta_title": "string", (optional)
  "body": "string", (optional)
  "tags": "string" (optional)
}
```

### 8. Delete Blog

- **URL**: `/blog/{blog_id}`
- **Method**: `DELETE`
- **Description**: Delete a existing blog.

**Request:**
```http
DELETE /api/blog/{blog_id}
```


### 9. Create Comment

- **URL**: `/comment/{blog_id}`
- **Method**: `POST`
- **Description**: Create a new comment.

**Request:**
```http
POST /api/comment/{blog_id}
Content-Type: application/json

{
  "blog": 0,
  "parent": null, (null if it is not a reply to other comment)
  "text": "string"
}
```

### 10. Get comments by blog ID

- **URL**: `/comment/{blog_id}`
- **Method**: `GET`
- **Description**: Get  comments by blog ID.

**Request:**
```http
GET /api/comment/{blog_id}
```

### 11. Edit Comment

- **URL**: `/comment/{blog_id}`
- **Method**: `PATCH`
- **Description**: Edit a existing comment.

**Request:**
```http
PATCH /api/comment/{blog_id}
Content-Type: application/json

{
  "text": "string"
}
```

### 12. Delete Comment

- **URL**: `/comment/{blog_id}`
- **Method**: `DELETE`
- **Description**: Delete a existing comment.

**Request:**
```http
DELETE /api/comment/{blog_id}
```


### 13. Get User-Profile

- **URL**: `/user-profile/`
- **Method**: `GET`
- **Description**: Get logged-in user profile.

**Request:**
```http
GET /api/user-profile/
```
### 14. Update User-Profile

- **URL**: `/user-profile/`
- **Method**: `PATCH`
- **Description**: Edit a existing profile.

**Request:**
```http
PATCH /api/user-profile/
Content-Type: multipart/form-data

name : Naman (optional)
bio  : bio text (optional)
profile_pic : file/image (optional)
```

### 15. Search Functionality

- **URL**: `/blog/search/?query={query}`
- **Method**: `GET`
- **Description**: Edit a existing profile.

**Request:**
```http
GET api/blog/search/?query={query}
```

