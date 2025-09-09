# NL2SQL Application

This project demonstrates a **Natural Language to SQL (NL2SQL)** system.  
It allows users to ask questions in natural language and automatically generates SQL queries against different datasets (**crimes**, **hospitality**, **happiness**).

---

## Built with
- **Python**
- **LangChain**
- **SQLAlchemy**
- **Streamlit**
- **MariaDB**
- **Docker Compose** (for database)  

---

## Getting Started

### 1. Clone the repository
```bash
git clone <your-repo-url>
cd <your-repo-name>
```

### 2. Start the database with Docker

```bash
docker-compose up
```

Default credentials:

User: root

Password: nl2sql

### 3. Install dependencies

```bash
poetry install
```

### 4. Initialize databases and load data

```bash
poetry run python scripts/init_database.py
```

This will:

Create the databases (if missing)

Load CSV data into the corresponding tables

### 5. Configure environment variables

Create a `.env` file in the project root and add your OpenAI API key:
OPENAI_KEY=your-openai-api-key

This key is required for the NL2SQL application to use the LLM (GPT-4o).

### 6. Run the Streamlit application
```bash
streamlit run app.py
```


## Project Structure

```text

├── app.py                 # Streamlit front-end
├── scripts/
│   └── init_database.py   # Script to create DBs and load CSV data
├── data/                  # CSV datasets
│   ├── crimes/
│   ├── happiness/
│   └── hospitality/
├── docker-compose.yml     
├── pyproject.toml         # Poetry dependencies
└── README.md    
```

## Requirements

- Docker
- Python 3.12
- Poetry




