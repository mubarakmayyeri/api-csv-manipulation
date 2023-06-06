# Python API for CSV File Manipulation

This repository contains a Python API developed with FastAPI for CSV file manipulation. It provides endpoints for reading  & processing CSV files, and retrieving result files. The API is designed to handle two input datasets and return the processed results in JSON format.

## Table of Contents
- [Dependencies](#dependencies)
- [Installation](#installation)
- [Usage](#usage)
- [Directory Structure](#directory-structure)
- [Environment Variables](#environment-variables)
- [Testing the API](#testing-the-api)
- [API Server on AWS EC2](#api-server-on-aws-ec2)
- [Demonstration](#demonstration)

## Dependencies
- Python 3.11.2
- FastApi 0.95.2

## Installation
1. Clone the repository:
```shell
git clone https://github.com/mubarakmayyeri/api-csv-manipulation.git
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

    - **Index** (GET): http://localhost:8000/
      - This endpoint returns a JSON response indicating whether the API is running successfully.
      - Response:
        ```json
        {
        "message": "API is running succesfully"
        }
        ```
    - **Read data** (POST): http://localhost:8000/read_data
      - This endpoint requires two CSV files as input datasets.
      - The API will read and process the data, generating result files.

    - **Get results** (GET): http://localhost:8000/get_results
      - This endpoint returns a JSON file wihch contains the processed dataframes.

## Directory Structure
The repository has the following directory structure:

```
api-csv-manipulation/
├── main.py
├── requirements.txt
├── demonstration.txt/
│ └── api_demo.ipynb
└── check_api/
  ├── datasets/
  │ ├── datagenerator.ipynb
  │ ├── dataset_1.csv
  │ └── dataset_2.csv
  ├── results/
  ├── check_get_results.py
  └── check_read_data.py

```


- `main.py`: The main FastAPI code file.
- `requirements.txt`: File containing the required dependencies.
- `demonstration/`: Directory containing Jupyter notebook for demonstrating usage of API.
- `check_api/`: Directory containing scripts for testing the API endpoints.
- `check_api/datasets/`: Directory containing CSV file generator and  sample input CSV files.
- `check_api/results/`: Directory where the result jspon files will be saved.

## Environment Variables
The API and testing scripts utilize environment variables for certain configurations. Please make sure to set the following environment variables before running the API or testing scripts:

* API_KEY: The API key for authentication and access control. Make sure to keep this value confidential and do not expose it publicly.
* IP_ADDRESS: The IP address of the API server.

You can set these environment variables in different ways depending on your operating system or deployment environment. For local development, you can create a .env file in the root directory and define the variables as shown below:

```makefile
API_KEY=your_api_key
IP_ADDRESS=your_ip_address
```

Make sure not to commit the `.env` file to version control to keep the sensitive information secure.


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

## API Server on AWS EC2
The API has been deployed on an AWS EC2 instance with Nginx.

**Server Details:**

- IP Address: [Your EC2 Instance IP Address]

To access the API endpoints, use the following URLs:

- **Index**: https://3.108.61.108/
- **Read data**: https://3.108.61.108/read_data
- **Get results**: https://3.108.61.108/get_results

When calling the `read_data` and `get_results` endpoints, include the following header in your request:
```json
{
"X-API-Key": "Your_API_Key"
}
```

Replace `"Your_API_Key"` with the actual API key value.

## Demonstration
You can find the demo of how to use the Live API on this [Jupyter Notebook](https://github.com/mubarakmayyeri/api-csv-manipulation/blob/main/demonstration/api_demo.ipynb)