# NL2SQL-LangChain

This project evaluates the **Natural Language to SQL (NL2SQL)** capabilities of **LangChain**.  
It allows users to ask questions in natural language and automatically generates SQL queries against different datasets (**crimes**, **hospitality**, **happiness**).  

The goal is to compare and test **LangChain’s SQLAgent** and **SQLDatabaseChain** modules in terms of how well they can query structured data from different databases.

---

## Usage

In the Streamlit frontend, users can:
- Select the LangChain module (SQLAgent or SQLDatabaseChain)
- Choose one of the available databases (Crimes, Hospitality, Happiness)
- Enter natural language queries and view both the generated SQL and the results
- Inspect verbose logs for debugging and comparison

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
git clone https://github.com/TutaevaIrina/nl2sql_langchain
```

### 2. Start the database with Docker

```bash
docker-compose up
```

Default credentials:

`User: root`

`Password: nl2sql`

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

`OPENAI_KEY=your-openai-api-key`

This key is required for the NL2SQL application to use the LLM (GPT-4o).

### 6. Run the Streamlit application
```bash
streamlit run app.py
```

## Data 

The required crime dataset is too large to be stored directly in this repository. Please download it manually from Kaggle and place it in the specified directory: 

### Crimes Data Source: 

Kaggle – 2019 Crimes Data (https://www.kaggle.com/datasets/edwardotieno/2019-crimes-data)

File: crimes-2001-to-present.csv

Location: data/crimes/ 

### Happiness Data

Already included in the repository (no external download required) 

### Hospitality Data 

Already included in the repository (no external download required)


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




