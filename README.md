# Parser configuration

## Set up the project
### Create virtual environment

```bash
python -m venv venv
```

### Activate virtual environment

```bash
source venv/bin/activate
```

### Install dependencies

```bash
pip install -r requirements.txt
```

### Add environment variables
```bash
cp .env.example .env
```
fill in the variables in the .env file

### Run migration
```bash
alembic upgrade head
```

### Run the project
```bash
python main.py
```

## Extra commands:
### Run tests
```bash
pytest test.py
```
### Black formatting
```bash
python -m black .
```

### Import formatting
```bash
isort .
```