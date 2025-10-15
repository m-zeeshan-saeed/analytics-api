# 🚀 FastAPI + PostgreSQL + Docker Project

This project uses **FastAPI** as the backend framework with a **PostgreSQL** database.
It supports both **local development using a Python virtual environment** and **containerized deployment using Docker and Docker Compose**.

---

## 🧰 Prerequisites

Make sure you have installed:

- [Python 3.10+](https://www.python.org/downloads/)
- [pip](https://pip.pypa.io/en/stable/installation/)
- [Docker](https://www.docker.com/get-started)
- [Docker Compose](https://docs.docker.com/compose/install/)

---

## 🐍 Local Setup (Python Virtual Environment)

### 1. Clone the repository

```bash
git clone https://github.com/m-zeeshan-saeed/analytics-api.git
cd analytics-api
```

### 2. Create and activate a virtual environment

**For macOS/Linux:**

```bash
python3 -m venv venv
source venv/bin/activate
```

**For Windows (PowerShell):**

```bash
python -m venv venv
venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### 4. Run FastAPI app locally

```bash
uvicorn app.main:app --reload
```

Then open: [http://127.0.0.1:8000](http://127.0.0.1:8000)

---

## 🐘 PostgreSQL Setup (Local)

You can install PostgreSQL manually or use Docker (recommended).

**Manual installation (optional):**

- Default port: `5432`
- Default database: `mydatabase`
- Create a `.env` file in your project root:

```env
DATABASE_URL=postgresql://username:password@localhost:5432/mydatabase
```

---

## 🐳 Docker Setup

### 1. Build the Docker image

```bash
docker build -t fastapi-app .
```

### 2. Run the container

```bash
docker run -d -p 8000:8000 fastapi-app
```

Now your app should be available at [http://localhost:8000](http://localhost:8000)

---

## ⚙️ Docker Compose Setup

### 1. Example `docker-compose.yml`

```yaml
version: "3.9"

services:
  db:
    image: postgres:15
    container_name: postgres_db
    restart: always
    environment:
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: password
      POSTGRES_DB: mydatabase
    volumes:
      - postgres_data:/var/lib/postgresql/data
    ports:
      - "5432:5432"

  web:
    build: .
    container_name: fastapi_app
    command: uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
    volumes:
      - .:/code
    ports:
      - "8000:8000"
    depends_on:
      - db
    env_file:
      - .env

volumes:
  postgres_data:
```

### 2. Run both containers

```bash
docker-compose up --build
```

### 3. Stop containers

```bash
docker-compose down
```

---

## 📦 Project Structure Example

```
.
├── app
│   ├── main.py
│   ├── models.py
│   ├── routers/
│   ├── schemas/
│   └── database.py
├── requirements.txt
├── Dockerfile
├── docker-compose.yml
├── .env
└── README.md
```

---

## 🧪 Useful Commands

| Description          | Command                               |
| -------------------- | ------------------------------------- |
| Run FastAPI locally  | `uvicorn app.main:app --reload`       |
| Run Docker container | `docker run -p 8000:8000 fastapi-app` |
| Run Docker Compose   | `docker-compose up --build`           |
| Stop Docker Compose  | `docker-compose down`                 |
| View Docker logs     | `docker logs fastapi_app`             |

---

## 🧾 License

This project is licensed under the [MIT License](LICENSE).

---

## 🧠 Author

💻 GitHub: [@m-zeeshan-saeed](https://github.com/m-zeeshan-saeed)
📧 Email: zeeshansheikh0313@gmail.com
