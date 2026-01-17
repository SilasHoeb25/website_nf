# website\_nf

A Django Project built with **HTMX + Tailwind**, running in **Docker**
The Website is available on localhost:8000

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


