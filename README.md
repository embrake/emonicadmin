## Emonic-Admin 

Emonic-Admin a battery startup for newly emonic v1.0.1

[![IMG-20230823-151908.jpg](https://i.postimg.cc/Vsd2Qym0/IMG-20230823-151908.jpg)](https://postimg.cc/dDc5rx7J)

## Available scripts

```bash
emonic-admin create-project {projectname}
```

```bash
emonic-admin setup --migrate
```

```bash
emonic-admin build -p {root_project_name}
```

```bash
emonic-admin manage engine
```

```bash
emonic-admin gradle --production
```

- emonic-admin createproject {project_name} for building the floor of Emonic app.
- emonic-admin setup --migration for setting up the migration to root project.
- emonic-admin build -p {root_project_name} building the root project.
- emonic-admin manage engine for setting up all the templates and static files.
- emonic-admin gradle --production for production usage.