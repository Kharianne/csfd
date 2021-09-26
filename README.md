# CSFD search
Simple walkthrough:
1) Clone this repository
2) Create virtual env ```python -m venv <path_to_env>```, activate and install requirements.txt ```pip install -r requirements.txt```
3) Run:
```python manage.py runserver```

## Load data
Database is prepopulated, so the initial load is not necessary.

To delete existing data and query for new one run:

```python manage.py load_data```
