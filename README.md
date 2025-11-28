# MVP FastAPI + React test project
## To run:
Clone repository on your computer:
```bash
git clone https://github.com/RynhAleh/rynh-aleh-test-project-mvp.git && cd rynh-aleh-test-project-mvp
```
Clone secrets, if you don't have your own:
```bash
cp .env.example .env --update=none
```
Run:
```bash
docker-compose up --build
```
Access frontend at http://localhost:3000 (backend at http://localhost:8000).
Navigation supports back button via React Router.
For testing, use curl as in the task.
Unique selects in Page3 fetch all possible names by querying history with today's date (minimal, no extra endpoint).