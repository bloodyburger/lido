 # Lido Reporting
![GitHub all releases](https://img.shields.io/github/downloads/Steakhouse-Financial/lido-reports/total?style=for-the-badge)![GitHub pull requests](https://img.shields.io/github/issues-pr/Steakhouse-Financial/lido-reports?style=for-the-badge)![GitHub forks](https://img.shields.io/github/forks/Steakhouse-Financial/lido-reports?style=for-the-badge)![GitHub Repo stars](https://img.shields.io/github/stars/Steakhouse-Financial/lido-reports?style=for-the-badge)![GitHub last commit](https://img.shields.io/github/last-commit/Steakhouse-Financial/lido-reports?style=for-the-badge)

-- Description goes here

## Components
[![Python 3.9](https://img.shields.io/badge/python-3.9-blue.svg?style=for-the-badge)](https://www.python.org/downloads/release/python-360/) ![Django](https://img.shields.io/badge/django-%23092E20.svg?style=for-the-badge&logo=django&logoColor=white)

## 🔧 How to Install

### 🐳 Docker


```bash
docker run \
	--name lido \
	-p 8000:8000 \
	-e SNOWFLAKE_USER=user \
	-e SNOWFLAKE_PASSWORD=password \
	-e SNOWFLAKE_ACCOUNT=account \
	-e SNOWFLAKE_WAREHOUSE=<XL,X-Small> \
	-e SNOWFLAKE_DATABASE=database \
	-e SNOWFLAKE_SCHEMA=schema \
	 bloodyburger/lido:latest
```
Lido reports is now running on http://localhost:8000

### 🐳 Docker-Compose
```bash
mkdir /opt/lido
cd /opt/lido
nano docker-compose.yml
```

Create docker-compose.yml with below contents
```
version: '3'

services:
    python:
        image: bloodyburger/lido:latest
        container_name: lido
        volumes:
            - ./db:/lido/db
        env_file:
            - ./config.env    
        ports:
            - 8000:8000
```
Maintain environment variables as described above and 

```bash
docker-compose up -d
```

Wait until you see the message on the logs
```
lido  | Django version 4.1.7, using settings 'lido.settings'
lido  | Starting development server at http://0.0.0.0:8000/
lido  | Quit the server with CONTROL-C.
```

Now run the migrations using
```
docker exec -it lido python manage.py migrate
```


Lido reports is now running on http://localhost:8000

You can check the docker logs by using
```bash 
docker logs lido
```

### :bust_in_silhouette: Creating admin user
```bash
docker exec -it lido bash
cd /lido
python manage.py createsuperuser
```

### Report configuration
The configuration data is stored on sqlite database and when you bind mount local path, the database file is saved on your local machine. If you do not mount local volume, the configurations will be lost and you have to redo all over again. There are three models created on the backend for storing the configurations. 

Login to admin panel using http://localhost:8000/admin with the username/password created in above step.

- Step 1 , Navigate to Reports model and maintain report name and it's description.
- Step-2, Navigate to Reports sources and maintain the source table name from where you want to pull the information. You can have multiple entries created and choose the appropriate one during the configuration on next step.
- Step-3, Navigate to Reports config and maintain config for each report you want to render dynamically. The various config options are as per below table,

| Option              | Value                                                                                                                                                                   |
| ------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Report              | choose the report name created already                                                                                                                                  |
| Primary filters     | comma separated values to filter, for example 3.1. Protocol Capital,3.2. Operating Performance                                                                          |
| Secondary filters   | comma separated values to filter, for example 3.1. Protocol Capital,3.2. Operating Performance                                                                          |
| Account filters     | comma separated values to filter, for example 3.1. Protocol Capital,3.2. Operating Performance                                                                          |
| Category filters    | comma separated values to filter, for example 3.1. Protocol Capital,3.2. Operating Performance                                                                          |
| Subcategory filters | comma separated values to filter, for example 3.1. Protocol Capital,3.2. Operating Performance                                                                          |
| Show primary        | Yes or No depending on whether you want to see this column in the output                                                                                                |
| Show secondary      | Yes or No depending on whether you want to see this column in the output                                                                                                |
| Show account        | Yes or No depending on whether you want to see this column in the output                                                                                                |
| Show category       | Yes or No depending on whether you want to see this column in the output                                                                                                |
| Show category       | Yes or No depending on whether you want to see this column in the output                                                                                                |
| Show token          | Yes or No depending on whether you want to see this column in the output                                                                                                |
| Value col           | The column from database that holds the value, for example VALUE_ETH or VALUE_USD                                                                                       |
| Field chooser       | Display or hide field chooser for the report                                                                                                                            |
| Row total           | Display or hide grand totals for rows                                                                                                                                   |
| Column total        | Display or hide grand totals for columns                                                                                                                                |
| Source table        | Choose the source table to pull the information from the database                                                                                                       |
| Show as dollar      | If you select Yes, dollar symbol will be shown as prefix to the values displayed                                                                                        |
| Value as cumulative | if Yes, values displayed will be cumulative across each year                                                                                                            |
| Filter known tokens | if Yes, data will be filtered for tokens ETH,DAI,MATIC,USDC,USDT,SOL,LDO                                                                                                |
| Fold primary        | Values displayed on this level will be folded by default and cannot be expanded. Specify the level value when the folding should happen. If not required, mark it as No |
| Expand primary      | if Yes, the hierarchy level will shown expanded else it will be collapsed by default and can be expanded once rendered                                                  |
| Expand secondary    | if Yes, the hierarchy level will shown expanded else it will be collapsed by default and can be expanded once rendered                                                  |
| Expand account      | if Yes, the hierarchy level will shown expanded else it will be collapsed by default and can be expanded once rendered                                                  |
| Expand category     | if Yes, the hierarchy level will shown expanded else it will be collapsed by default and can be expanded once rendered                                                  |
| Expand subcategory  | if Yes, the hierarchy level will shown expanded else it will be collapsed by default and can be expanded once rendered                                                  |
| Drilldown Cols  | Columns to be displayed on the drilldown popup separated by comma if there are more than 1                                                  |
