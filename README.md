# website\_nf

A Django Project built with **HTMX + Tailwind**, running in **Docker**
The Website is available on localhost:8000

## DEV

 - Dockervolume is stored in a volume, persists across restarts
 - code changes are automatically reflected due to volume mounting
Start:
 1. start Docker Engine
 2. open new Terminal, from the Project root run: ```docker compose up```
 keep it running!
 3. open new Terminal, from the Project root run tailwind in Watchmode:
 ```console C:\dev\website_nf> npx tailwindcss -i .\website\static\src\tailwind.css -o .\website\static\css\tailwind.css --watch```
 keep it running!

 Happy Coding!

 ### First startup on a New Environment

 - You cloned the repository for the first time
 - No Docker images or containers yet

 1. Run Docker desktop
 2. From the project root run:
 ```bash docker compose up --build ```
 3. Run database migrations in the container:
 ```bash docker exec -it website_nf python manage.py makemigrations```
 ```bash docker exec -it website_nf python manage.py migrate```
 4. Create a superuser (admin)
 ```bash docker exec -it website_nf python manage.py createsuperuser```


