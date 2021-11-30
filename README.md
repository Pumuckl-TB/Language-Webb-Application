# Language-WebApp

Web application prototype for a language school including many functionalities and machine learning. This app was developed for a seminar at the University of Zurich, hosted by Radu Tanase and Debora Costa.

The Application consists of 3 main parts:
1. PostgreSQL Database (ommited from GitHub)
2. Flask Backend
3. Dash Frontend

The app was developed for personal-german.ch according to their requirements. It offers the following functionality:
    - Admin functions:
        - View, Add, and Delete students
        - Assign topics to students (exercises for them to solve)
    - Dashboard:
        - View Student Progress
    - Student Functions:
        - Solve exercises that are assigned to them by the teacher
        - Solve exercises that are assigned via a Machine Learning algorithm


## Setup instructions

For this project to work you will need to have python3 installed. Additionally, you will need access to a PostgreSQL database. As the data comes from personal-german.ch and is confidential, we have ommitted the database schemas and data from this repository. If you really want to test out the app, please contact one of the contributors via GitHub.

1. Create a virtual environment (optional)
    `python3 -m venv /path`
2. Install requirements.txt
    `pip install -r requirements.txt`
3. Create and fill PostgreSQL database (contact authors for more information)
4. Adjust backend server script with your database credentials 
5. Start backend server by running file `TIMON PLS SPECIFY`
6. Adjust link to backend by changing `url_backend` in `frontend\links.py`
6. Start frontend by running file `frontend\index.py`
7. Open the website in your browser (default: 'http://127.0.0.1:8050/')


## Folder Structure
    .
    ├── backend                     # Backend folder
    │   ├── ...                     # ...
    │   ├── ...                     # ...
    │   ├── ...                     # ...
    │   ├── ...                     # ...
    │   └── ...    
    ├── frontend                    
    │   ├── apps                    # Contains all pages (layouts, callbacks, functions)
    │   │   ├── __init__.py         # Necessary for multipage apps
    │   │   ├── admin.py            # Admin layout, callbacks, functions
    │   │   ├── dashboard.py        # Dashboard layout, callbacks, functions
    │   │   ├── exercise.py         # Exercise layout, callbacks, functions
    │   │   └── upload.py           # Upload layout, callbacks, functions
    │   ├── assets                  # Contains assets used by all pages
    │   │   └── style.css           # Stylesheet                  
    │   ├── app.py                  # Creates app and server
    │   └── index.py                # Main frontend file which renders everything
    ├── requirements.txt            
    └── readme.md

## Architecture

![Architecture](https://raw.githubusercontent.com/feljost/Language-WebApp/main/pictures/architecture.JPG?token=APCQ7XGRMHSTIQSL53I4A3TBUYHUO)
