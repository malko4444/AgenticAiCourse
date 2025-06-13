how to init and install of the alembic 
- pip install alembic 
- pip install psycopg2-binary
for init 
- python -m alembic init alembic
- creat a model folder and creat a table odel file that how one column is look like and what coloum is in the table now connect this moddle in the alembic using the metadata available in the env.py and import model there 

for auto migration 
- python -m alembic revision --autogenerate -m "create change todos table"
- this command save this which version is running on the db if we run this its updated the changes done i the model file and save it in the revision folder
- python -m alembic upgrade head
- 
- 