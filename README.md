# Python API for CSV File Manipulation

## Description
This repository contains a Python API developed with FastAPI for CSV file manipulation. It provides endpoints for reading CSV files & processing data, and generating result files. The API is designed to handle two input datasets and return the processed results in CSV format.

## Dependencies
- Python 3.11.2
- FastApi 0.95.2

## Installation
1. Clone the repository:
```shell
git clone https://github.com/mubarakmayyeri/api-solar-bhai.git
```

2. Install the required dependencies using `pip`:
```shell
pip install -r requirements.txt
```

## Usage
1. Start the API server using the command:
```shell
python main.py
```

2. Access the API endpoints using the following URLs:

    - **Index** (GET method): http://localhost:8000/
      - This endpoint returns a JSON response indicating whether the API is running successfully.
      - Response:
        ```json
        {
        "message": "API is running succesfully"
        }
        ```
    - **Read data** (POST method): `http://localhost:8000/read_data`
      - This endpoint requires two CSV files as input datasets.
      - The API will read and process the data, generating result files.

    - **Get results** (GET method): `http://localhost:8000/get_results`
      - This endpoint returns a JSON file wihch contains the processed dataframes.

## Directory Structure
The repository has the following directory structure:

```
api-solar-bhai/
├── main.py
├── requirements.txt
├── datasets/
│ ├── datagenerator.ipynb
│ ├── dataset_1.csv
│ └── dataset_2.csv
├── check_api/
| ├── results/
│ ├── check_get_results.py
│ └── check_read_data.py
├── test_read_data.py
└── test_get_results.py
```


- `main.py`: The main FastAPI code file.
- `requirements.txt`: File containing the required dependencies.
- `datasets/`: Directory containing sample input CSV files.
- `check_api/`: Directory containing scripts for testing the API endpoints.
- `check_api/results/`: Directory where the result jspon files will be saved.


## Testing the API

1. Test `read_data` endpoint:
```shell
python .\check_api\check_read_data.py
```

2. Test `get_results` endpoint:
```shell
python .\check_api\check_get_results.py
```
- The result JSON files will be saved in the `./check_api/results/` directory.

The results directory will be dynamically created during the execution of the testing script and is not part of the repo.