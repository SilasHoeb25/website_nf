# website\_nf

A Django Project built with **HTMX + Tailwind**, running in **Docker**
The Website is available on localhost:8000

## RUN MY PROJECT --> TEACHER INSTRUCTION

The application is built with docker compose.

### 0) Requirements

 - Install **Docker Desktop** on Windows or **Docker Engine** if you use Linux
 - If you use Linux, u might have to install **Docker Compose** seperately
 - Make sure, **nothing is running** on the Ports: **:8000** or **:5432**

### 1) Clone REPO --> Open in Terminal

 - clone my Github Repo and save it on your Computer. 
 - Open a Terminal as Admin (recommended, not required)

### 2) Build the Docker Containers

move the Terminal into the base Folder **"website_nf"** on your computer
Run this Command:

```bash
docker compose up --build
```
Docker is finished building when you see:
```bash
website_nf   | Watching for file changes with StatReloader
```
In the Terminal

### 3) Create the Database Tables

Now that we have Django and the Postgres DB up and running, we need to Create the Database tables.

Open a *NEW Terminal* in the Folder **website_nf**

Run the following Command:

```bash
docker exec -it website_nf python manage.py makemigrations
```
This command creates the Database migrations for the Database. it most likely says:
```bash
No changes detected
```
Since the Migrationsfolder is also in the Repo. After that run the migrations:
```bash
docker exec -it website_nf python manage.py migrate
```
it creates the Table in the Postgres Database.

### 4) Create a Superuser

To be able to create Timeslots, You need a superuser (admin), since you can't create one from the Register Form.

run the following command:
```bash
docker exec -it website_nf python manage.py createsuperuser
```
Follow the instructions in the Terminal. Emailadress is not required and you can Bypass the Password validation.

### 5) Open the APP

The app is now fully usable and you can access it on **localhost:8000** in your Browser!



## Start for Development

 - Dockervolume is stored in a volume, persists across restarts
 - code changes are automatically copied into the Container due to volume mounting

  ### First Startup for DEV on a New Environment

 - You cloned the repository for the first time
 - No Docker images or containers yet

 1. Run Docker Engine
 2. From the project root run:
 ```console
 docker compose up --build
 ```
    keep it running!
    
 3. From the project root run database migrations in the container:

 ```console
docker exec -it website_nf python manage.py makemigrations
  ```

 ```console
 docker exec -it website_nf python manage.py migrate
 ```

 4. Create a superuser (admin)
 ```console
 docker exec -it website_nf python manage.py createsuperuser
 ```
 5. open new Terminal, from the Project root run tailwind in Watchmode:
 ```console
 C:\dev\website_nf> npx tailwindcss -i .\website\static\src\tailwind.css -o .\website\static\css\tailwind.css --watch
 ```
    keep it running!

 **Happy Coding!**

### Second Startup

 1. Start Docker Engine
 2. open new Terminal, from the Project root run: 
 ```console
 docker compose up
 ```
    keep it running!

 3. open new Terminal, from the Project root run tailwind in Watchmode:
 ```console
 C:\dev\website_nf> npx tailwindcss -i .\website\static\src\tailwind.css -o .\website\static\css\tailwind.css --watch
 ```
    keep it running!

 **Happy Coding!**


