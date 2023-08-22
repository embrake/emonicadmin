import os
import sys
import pickle
import subprocess
import argparse

created_projects = [] 

def create_folder(project_name):
    if not os.path.exists(project_name):
        os.makedirs(project_name)
        print(f"Folder '{project_name}' created.")
    else:
        print(f"Folder '{project_name}' already exists.")

def create_file(file_path, content):
    with open(file_path, 'w') as f:
        f.write(content)
        print(f"File '{file_path}' created.")

def create_views_static(project_name):
    views_folder = f"{project_name}/views"
    static_folder = f"{project_name}/static"
    os.makedirs(views_folder)
    os.makedirs(static_folder)
    print("Folders 'views' and 'static' created.")

    index_html_code = '''<!DOCTYPE html>
<html>
<head>
    <title>Welcome to Emonic Web Framework</title>
</head>
<body>
    <div class="flex items-center justify-center h-screen bg-gray-100">
        <h1 class="text-4xl font-bold text-indigo-700">Welcome to Emonic Web Framework</h1>
    </div>
</body>
</html>
'''
    create_file(f"{views_folder}/index.html", index_html_code)
    create_file(f"{static_folder}/script.js", "")
    create_file(f"{static_folder}/style.css", "")

def update_modules_json(project_name):
    modules_json_file = f"{project_name}/modules.json"
    import json
    with open(modules_json_file, 'r') as f:
        data = json.load(f)
        data[0]["modules"].extend([
            {"name": "viewengine", "url": "http://emonic.vvfin.in/jit/23116933/modules/viewengine?pypi=True&connected=True"},
            {"name": "staticengine", "url": "http://emonic.vvfin.in/jit/23116933/modules/static?pypi=True&connected=True"},
            {"name": "pubsec", "url": "http://emonic.vvfin.in/jit/23116933/modules/pubsec?pypi=True&connected=True"}
        ])
    with open(modules_json_file, 'w') as f:
        json.dump(data, f, indent=4)
    print("modules.json updated.")

def load_created_projects():
    if os.path.exists("project.pkl"):
        with open("project.pkl", "rb") as f:
            return pickle.load(f)
    return []

def save_created_projects(projects):
    with open("project.pkl", "wb") as f:
        pickle.dump(projects, f)

def run_server(project_name):
    app_file = f"{project_name}/app.py"
    if os.path.exists(app_file):
        print(f"Running server for project '{project_name}'...")
        subprocess.run(["python", app_file])
    else:
        print(f"Error: 'app.py' file not found in project '{project_name}'.")


def main():
    global created_projects  # Declare the variable as global to modify it inside the function

    parser = argparse.ArgumentParser(description="EmonicAdmin - A Python project management tool for Emonic Web Framework.")
    subparsers = parser.add_subparsers(dest='command', help="Available commands")

    # Subparser for the 'startproject' command
    startproject_parser = subparsers.add_parser('startproject', help='Create a new project')
    startproject_parser.add_argument('-i', '--projectname', required=True, help='Name of the project')

    # Subparser for the 'runserver' command
    runserver_parser = subparsers.add_parser('runserver', help='Run the server for a project')
    runserver_parser.add_argument('projectname', help='Name of the project to run the server for')

    # Subparser for the 'manage' command
    manage_parser = subparsers.add_parser('manage', help='Manage startup engine')
    manage_parser.add_argument('engine', choices=['engine'], help='Manage the startup engine')

    args = parser.parse_args()

    if args.command == 'startproject':
        project_name = args.projectname
        create_folder(project_name)

        settings_code = '''HOST = 'localhost'
PORT = 8000
DEBUG = True
SECRET_KEY = "your_secret_key"
STATIC_FOLDER = "static"

TEMPLATES = [
    {
        'BACKEND': 'emonic.backends.EmonicTemplates',
        'DIRS': ['views'],
    }
]

DATABASES = {
    'default': {
        'ENGINE': 'emonic.db.backends.electrus',
        'HOST': 'localhost',
        'PORT': 37017,
        'USER': 'root',
        'PASSWORD': 'root'
    }
}

MAILER = [
    {
        "SMTP": "VALUE",
        "PORT": "VALUE",
        "USERNAME": "VALUE",
        "PASSWORD": "VALUE",
        "SSL": True,
        "DEFAULT_SENDER": "VALUE"
    }
]
'''
        create_file(f"{project_name}/settings.py", settings_code)

        app_code = '''from emonic.core.branch import Emonic, Response

app = Emonic(__name__)

@app.route('/', methods=['GET', 'POST'])
def home(request):
    return Response("Welcome to Emonic Web Framework")

if __name__ == "__main__":
    app.runs()
'''
        create_file(f"{project_name}/app.py", app_code)

        modules_json_code = '''[
    {
        "config": [
            {
                "$host": "127.0.0.1",
                "$port": 8000,
                "$debug": "True",
                "$http": "www.emonic.vvfin.in/conf/%connection%/devweb2?_uri=main&support=True&_ping=192.168.0.1"
            }
        ],
        "modules": [
            {
                "name": "emonic",
                "url": "http://emonic.vvfin.in/jit/23116933/modules/emonic?pypi=True&connected=True"
            },
            {
                "name": "mailer",
                "url": "http://emonic.vvfin.in/jit/23116933/modules/mailer?pypi=True&connected=True"
            },
            {
                "name": "JwT",
                "url": "http://emonic.vvfin.in/jit/23116933/modules/JwT?pypi=True&connected=True"
            },
            {
                "name": "blueprint",
                "url": "http://emonic.vvfin.in/jit/23116933/modules/blueprint?pypi=True&connected=True"
            },
            {
                "name": "chiper",
                "url": "http://emonic.vvfin.in/jit/23116933/modules/chiper?pypi=True&connected=True"
            },
            {
                "name": "session",
                "url": "http://emonic.vvfin.in/jit/23116933/modules/session?pypi=True&connected=True"
            },
            {
                "name": "limiter",
                "url": "http://emonic.vvfin.in/jit/23116933/modules/limiter?pypi=True&connected=True"
            },
            {
                "name": "BaseModals",
                "url": "http://emonic.vvfin.in/jit/23116933/modules/BaseModals?pypi=True&connected=True"
            }
        ],
        "database": [
            {"name": "Electrus", "$connection": "True"},
            {"name": "MongoDB", "$connection": "False"}
        ],
        "privilege": [
            {
                "role": "user",
                "control": "+055 wbr++",
                "$host": "127.0.0.1",
                "$port": "8080"
            }
        ]
    }
]
'''
        create_file(f"{project_name}/modules.json", modules_json_code)

        created_projects.append(project_name)
        save_created_projects(created_projects)

    elif args.command == 'runserver':
        project_name = args.projectname
        run_server(project_name)

    elif args.command == 'manage' and args.engine == 'engine':
        created_projects = load_created_projects()
        if len(created_projects) == 0:
            print("No projects have been created yet.")
            return

        project_name = created_projects[-1]
        create_views_static(project_name)
        update_modules_json(project_name)

    else:
        parser.print_help()

if __name__ == "__main__":
    main()
