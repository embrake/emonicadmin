import os
import argparse
import json
import secrets
import ast
import shutil
import random
import time

def create_project(project_name):
    project_path = os.path.join(os.getcwd(), project_name)

    try:
        os.makedirs(project_path, exist_ok=True)

        # Create folders and files
        open(os.path.join(project_path, '__init__.py'), 'a').close()
        open(os.path.join(project_path, 'urls.py'), 'a').close()
        open(os.path.join(project_path, 'settings.py'), 'a').close()
        open(os.path.join(project_path, 'gradle.py'), 'a').close()

        # Add content to settings.py
        settings_content = f'''
INSTALLED_APPS = [
    '@emonic.core',
    '@emonic.mail',
    '@emonic.contrib',
    '@emonic.Restful',
    '@emonic.security',
    '@emonic.utils',
    '@emonic.components',
    '@emonic.structer',
    '@emonic.builder',
    '{project_name}.admin',
]

ALLOWED_HOSTS = ['0.0.0.0', '127.0.0.1']
        '''
        with open(os.path.join(project_path, 'settings.py'), 'w') as settings_file:
            settings_file.write(settings_content)

        # Add content to urls.py
        urls_content = f'''
from {project_name}.urls import path

urlpatterns = [
    path('{project_name}')
]
        '''
        with open(os.path.join(project_path, 'urls.py'), 'w') as urls_file:
            urls_file.write(urls_content)

        # Delete existing config.py if it exists
        config_path = os.path.join(os.getcwd(), 'config.py')
        if os.path.exists(config_path):
            os.remove(config_path)

        unique_key = secrets.token_hex(16)
        unique_checksum = secrets.token_hex(32)

        # Create config.py
        config_content = f'''APP = [
    {{
        "project": {{
            "project": "{project_name}",
            "path": "{project_path}",
            "gradle": {{
                "version": 1.1,
                "path": "{project_path}?gradle.key{unique_key}",
                "projectSecrets": ["myadmin", "root", "builder"],
                "checksum": "{unique_checksum}"
            }},
            "projectKey": "{unique_key}",
            "projectAdmin": "emonic.root",
            "alice": None
        }}
    }}
]

GRADLE = []
        '''
        with open(config_path, 'w') as config_file:
            config_file.write(config_content)

        message = f'''Project {project_name} intitiazed. \n 
APP = [
    {{
        "project": {{
            "project": "{project_name}",
            "path": "{project_path}",
            "gradle": {{
                "version": 1.1,
                "path": "{project_path}?gradle.key{unique_key}",
                "checksum": "{unique_checksum}"
            }},
            "projectKey": "{unique_key}",
        }}
    }}
] \n

run ^ `emonic-admin setup --migrate` # Migrate your project
>> emonic-admin 1.0.1
        '''

        print(message)
    except Exception as e:
        print(f'Error creating project "{project_name}": {e}')

def fetch_project_name():
    config_path = os.path.join(os.getcwd(), 'config.py')
    if os.path.exists(config_path):
        with open(config_path, 'r') as config_file:
            config_content = config_file.read()

            # Extract project name using string manipulation
            project_name_start = config_content.find('"project": "') + len('"project": "')
            project_name_end = config_content.find('"', project_name_start)
            project_name = config_content[project_name_start:project_name_end]
            
            return project_name
    else:
        print('config.py does not exist.')
        return None

def create_migration():
    project_name = fetch_project_name()

    if project_name:
        project_path = os.path.join(os.getcwd(), project_name)
        migration_path = os.path.join(project_path, 'Gradle')

        try:
            os.makedirs(migration_path, exist_ok=True)

            # Create files inside migration_path
            open(os.path.join(migration_path, '__init__.py'), 'a').close()
            open(os.path.join(migration_path, 'migration.py'), 'a').close()
            open(os.path.join(migration_path, 'build.py'), 'a').close()

            # Add content to migration.py
            migration_content = f'''BUILDER = [
    {{
        "project": {{
            "init": "main:{project_name}:gradle",
            "migration": "gradle.migrate",
            "entry_point": {{
                "root": "{project_path}",
                "secure": True
            }},
            "connection": {{
                "connect": "http://emonic.vvfin.in/connect/migration/{{secret_key}}",
                "CORS": "Keep-Alive-3.0",
                "setup": ['on', 'disconnect']
            }},
            "gradle": {{
                "name": "gradle.com.1",
                "version": 1.1,
                "key": "",
                "entry": "BUILDER"
            }}
        }}
    }}
]
            '''
            with open(os.path.join(migration_path, 'migration.py'), 'w') as migration_file:
                migration_file.write(migration_content)

            print(f'Migration of {project_name} in progress...')

            # Add content to build.py
            build_content = f'''GRADLE_BUILD = ["{project_name}", "{project_path}"]
            '''
            with open(os.path.join(migration_path, 'build.py'), 'w') as build_file:
                build_file.write(build_content)
                time.sleep(5)

            message = f'''Migration setup for {project_name} is completed. \n
BUILDER = [
    {{
        "project": {{
            "init": "main:{project_name}:gradle",
            "migration": "gradle.migrate",
            "entry_point": {{
                "root": "{project_path}",
                "secure": True
            }}
        }}
    }}
]

run ^ `emonic-admin build --p <gradle_project_name>` ## For build core project.
>> emonic-admin 1.0.1
'''

            print(message)
        except Exception as e:
            print(f'Error creating migration for "{project_name}": {e}')
    else:
        print('Error: Project name not found in config.py.')

def build_project(project_name):
    gradle_project_name = fetch_project_name()
    project_path = os.path.join(os.getcwd(), gradle_project_name)
    root_project_path = os.path.join(os.getcwd(), project_name)
    migration_path = os.path.join(project_path, 'Gradle')
    migration_file_path = os.path.join(migration_path, 'migration.py')

    if os.path.exists(migration_file_path):
        with open(migration_file_path, 'r') as migration_file:
            migration_content = migration_file.read()
            if 'BUILDER' in migration_content:
                if f'"init": "main:{gradle_project_name}:gradle"' in migration_content and \
                   '"migration": "gradle.migrate"' in migration_content:

                    # Update INSTALLED_APPS in settings.py
                    settings_path = os.path.join(project_path, 'settings.py')
                    with open(settings_path, 'r') as settings_file:
                        settings_content = settings_file.read()
                    if f"'@{project_name}.gradle'" not in settings_content:
                        new_settings_content = settings_content.replace(
                            'INSTALLED_APPS = [',
                            f"INSTALLED_APPS = [\n'@{project_name}.gradle',"
                        )
                        with open(settings_path, 'w') as settings_file:
                            settings_file.write(new_settings_content)

                    # Create a new folder outside {project_name}
                    new_project_path = os.path.join(os.getcwd(), project_name)
                    os.makedirs(new_project_path, exist_ok=True)
                    os.makedirs(os.path.join(new_project_path, 'app'), exist_ok=True)

                    open(os.path.join(new_project_path, '__init__.py'), 'a').close()
                    open(os.path.join(new_project_path, 'views.py'), 'a').close()
                    open(os.path.join(new_project_path, 'settings.py'), 'a').close()

                    # Create views.py
                    views_content = f'''from emonic.core.branch import Emonic

app = Emonic(__name__)

@app.route('/')
def emonic(request):
    return "Welcome to Emonic server!"

if __name__ == "__main__":
    app.run()
    '''
                    with open(os.path.join(new_project_path, 'views.py'), 'w') as views_file:
                        views_file.write(views_content)

                    # Create settings.py
                    settings_content = f'''HOST = 'localhost'
PORT = 8000
DEBUG = True
SECRET_KEY = "your_secret_key"
STATIC_FOLDER = "static"

TEMPLATES = [
    {{
        'BACKEND': 'emonic.backends.EmonicTemplates',
        'DIRS': ['views'],
    }}
]

DATABASES = {{
    'default': {{
        'ENGINE': 'emonic.db.backends.electrus',
        'HOST': 'localhost',
        'PORT': 37017,
        'USER': 'root',
        'PASSWORD': 'root'
    }}
}}

MAILER = [
    {{
        "SMTP": "VALUE",
        "PORT": "VALUE",
        "USERNAME": "VALUE",
        "PASSWORD": "VALUE",
        "SSL": True,
        "DEFAULT_SENDER": "VALUE"
    }}
]

PATH = [
    {{
        "project": {{
            "name": "{project_name}",
            "path": "{root_project_path}"
        }},
        "gradle": {{
            "name": "{gradle_project_name}",
            "path": "{project_path}"
        }}
    }}
]

SCRIPT = [
    {{
        "config": {{
            "wsgi": "emonic.wsgi.http",
            "host": "localhost",
            "port": "8000",
            "debug": "True"
        }},
        "apps": {{
            "emonic",
            "emonic-admin"
            # add more emonic apps for e.g, electrus nexusdb etc...
        }}
    }}
]
    '''
                    with open(os.path.join(new_project_path, 'settings.py'), 'w') as settings_file:
                        settings_file.write(settings_content)

                    # Update config.py with GRADLE_PROJECT
                    config_path = os.path.join(os.getcwd(), 'config.py')
                    with open(config_path, 'r') as config_file:
                        config_content = config_file.read()
                    new_config_content = config_content.replace(
                        'GRADLE = [',  # Update this line
                        f'''GRADLE = [
    {{
        "gradle": {{
            "project": "{project_name}",
            "path": "{root_project_path}",
            "dev": {{
                "host": "localhost",
                "port": 8000,
                "debug": True,
                "key": {random.randint(10000000000, 99999999999)},
                "script": "run {project_name}/wsgi.py",
                "console": "",
                "version": 1.1
            }},
            "prod": {{
                "host": "0.0.0.0",
                "port": 8000,
                "server": ['gunicorn', 'uWSGI'],
                "prod-key": None,
                "script": "run {project_name}/wsgi.py",
                "build": "gradle {project_name}",
                "version": 1.1
            }}
        }}
    }}
'''
                    )

                    print("Runnig builder...")
                    with open(config_path, 'w') as config_file:
                        config_file.write(new_config_content)

                    message = f'''
GRADLE = [
    {{
        "gradle": {{
            "project": "{project_name}",
            "path": "{root_project_path}",
            "dev": {{
                "host": "localhost",
                "port": 8000,
                "debug": True,
                "key": {random.randint(10000000000, 99999999999)},
                "script": "run {project_name}/wsgi.py",
                "console": "",
                "version": 1.1
            }},
            "prod": {{
                "host": "0.0.0.0",
                "port": 8000,
                "server": ['gunicorn', 'uWSGI'],
                "prod-key": None,
                "script": "run {project_name}/wsgi.py",
                "build": "gradle {project_name}",
                "version": 1.1
            }}
        }}
    }}
]

Builder completed, Gradle project: {project_name}.
run ^ `emonic-admin gradle --production` # Setup your project for production.
run ^ `emonic-admin manage engine` # For setup your Emonic Static and Templating Engine.
run ^ `emonic-admin create electrus cli -u root -p root` # Creating the Electrus CLI Engine.
>> emonic-admin 1.0.1
'''
                    time.sleep(5)
                    print(message)
                else:
                    print('Error: Invalid migration configuration in migration.py.')
            else:
                print('Error: BUILDER list is missing in migration.py.')
    else:
        print('Error: migration.py does not exist.')

def fetch_gradle_project_name():
    config_path = os.path.join(os.getcwd(), 'config.py')
    if os.path.exists(config_path):
        with open(config_path, 'r') as config_file:
            config_content = config_file.read()

            # Find the index of the "GRADLE" key within the config content
            gradle_index = config_content.find('GRADLE = [')
            if gradle_index != -1:
                # Extract the content of the GRADLE list
                gradle_list_start = gradle_index + len('GRADLE = [')
                gradle_list_end = config_content.find(']', gradle_index) + 1
                gradle_list_content = config_content[gradle_list_start:gradle_list_end]

                # Find the index of the "project" key within the GRADLE list content
                project_key_index = gradle_list_content.find('"project": "')
                if project_key_index != -1:
                    project_name_start = project_key_index + len('"project": "')
                    project_name_end = gradle_list_content.find('"', project_name_start)
                    project_name = gradle_list_content[project_name_start:project_name_end]

                    return project_name
                else:
                    print('"project" key not found in GRADLE list.')
                    return None
            else:
                print('GRADLE list not found in config.py.')
                return None
    else:
        print('config.py does not exist.')
        return None

def fetch_static_dirs(project_name):
    project_path = os.path.join(os.getcwd(), project_name)
    settings_path = os.path.join(project_path, 'settings.py')
    static_folder = None
    dirs_value = None

    if os.path.exists(settings_path):
        with open(settings_path, 'r') as settings_file:
            settings_content = settings_file.read()
            static_start = settings_content.find('STATIC_FOLDER = ') + len('STATIC_FOLDER = ')
            static_end = settings_content.find('\n', static_start)
            static_folder = settings_content[static_start:static_end].strip('"')

            dirs_start = settings_content.find("'DIRS': [") + len("'DIRS': [")
            dirs_end = settings_content.find(']', dirs_start)
            dirs_value = settings_content[dirs_start:dirs_end]

            # Remove enclosing quotes from dirs_value if present
            dirs_value = dirs_value.strip(" '\"")

    return static_folder, dirs_value

def manage_engine():
    gradle_project_name = fetch_gradle_project_name()
    project_path = os.path.join(os.getcwd(), gradle_project_name)
    
    static_folder, dirs_value = fetch_static_dirs(gradle_project_name)

    if static_folder and dirs_value:
        static_path = os.path.join(project_path, static_folder)
        dirs_path = os.path.join(project_path, dirs_value)

        if not os.path.exists(static_path):
            os.makedirs(static_path)

            # Create css/ and js/ folders inside static_path
            os.makedirs(os.path.join(static_path, 'css'), exist_ok=True)
            os.makedirs(os.path.join(static_path, 'js'), exist_ok=True)

        if not os.path.exists(dirs_path):
            os.makedirs(dirs_path)

            # Create index.html file inside dirs_path
            with open(os.path.join(dirs_path, 'index.html'), 'w') as dirs_file:
                dirs_file.write('')

        print(f'Emonic template and static engine setup for {gradle_project_name} is completed.')
    else:
        print(f'Error: Static folder and/or DIRS value not found in settings.py for {gradle_project_name}.')

def gradle_build():
    gradle_project_name = fetch_gradle_project_name()
    root_project_name = fetch_project_name()
    
    if gradle_project_name and root_project_name:
        project_path = os.path.join(os.getcwd(), gradle_project_name)
        build_path = os.path.join(os.getcwd(), 'build')

        if os.path.exists(project_path):
            shutil.copytree(project_path, build_path)

            emonic_path = os.path.join(build_path, 'root')
            os.makedirs(emonic_path, exist_ok=True)

            for root, _, files in os.walk(os.path.join(project_path, 'build/root')):
                for file in files:
                    src_file = os.path.join(root, file)
                    dst_file = os.path.join(emonic_path, file)
                    shutil.copy2(src_file, dst_file)
            
            root_project_path = os.path.join(os.getcwd(), root_project_name)
            for root, dirs, files in os.walk(root_project_path):
                for dir in dirs:
                    src_dir = os.path.join(root, dir)
                    dst_dir = os.path.join(emonic_path, dir)
                    shutil.copytree(src_dir, dst_dir)
                for file in files:
                    src_file = os.path.join(root, file)
                    dst_file = os.path.join(emonic_path, file)
                    shutil.copy2(src_file, dst_file)

            print(f'Gradle build completed and copied to the build directory.')
        else:
            print(f'Error: {gradle_project_name} does not exist.')
    else:
        print(f'Error: gradle_project_name or project_name not found in config.py.')

def main():
    parser = argparse.ArgumentParser(description='Utility for managing projects and configurations.')
    subparsers = parser.add_subparsers(title='Available commands', dest='command', metavar='command')

    # Create Project
    create_parser = subparsers.add_parser('createproject', help='Create a new project')
    create_parser.add_argument('project_name', type=str, help='Name of the project')

    # Set Up Migration
    setup_parser = subparsers.add_parser('setup', help='Set up migration for a project')
    setup_parser.add_argument('--migrate', '-M', action='store_true', help='Set up migration')

    # Build Project
    build_parser = subparsers.add_parser('build', help='Build project setup')
    build_parser.add_argument('-p', '--project', type=str, help='Project name for build setup')

    # Manage Engine
    manage_parser = subparsers.add_parser('manage', help='Manage startup engine')
    manage_parser.add_argument('engine', choices=['engine'], help='Manage the startup engine')

    gradle_parser = subparsers.add_parser('gradle', help='Build emonic project for production')
    gradle_parser.add_argument('-s', '--production', action='store_true', help='Perform a production gradle build')

    args = parser.parse_args()

    if args.command == 'createproject':
        create_project(args.project_name)
    elif args.command == 'setup' and args.migrate:
        create_migration()
    elif args.command == 'build' and args.project:
        build_project(args.project)
    elif args.command == 'manage' and args.engine == 'engine':
        manage_engine()
    elif args.command == 'gradle' and args.production:
        gradle_build()
    else:
        parser.print_help()

if __name__ == '__main__':
    main()