from fastapi import FastAPI, Request, UploadFile, File, HTTPException, status, Depends
from fastapi.security import APIKeyHeader
from decouple import config
import concurrent.futures
import pandas as pd
import threading
import asyncio
import uvicorn
import uuid
import json
import time

app = FastAPI()

API_KEYS = config('API_KEYS').split(',')
api_key_header = APIKeyHeader(name="X-API-Key", auto_error=False)

results_dict = {}  # Dictionary to store result dataframes
results_lock = threading.Lock()  # Lock to synchronize access to results_dict


# Validate API token
def validate_api_key(api_key: str = Depends(api_key_header)):
    if api_key in API_KEYS:
        return api_key
    else:
        raise HTTPException(status_code=401, detail="Invalid API key.")

# Read csv files to pandas dataframe
def read_csv_file(file):
    try:
        df = pd.read_csv(file)

        return df

    except pd.errors.ParserError:

        raise HTTPException(status_code=400, detail="Invalid CSV file format.")

# Validate input files
def validate_csv(file):
    allowed_extensions = ["csv"]
    file_extension = file.filename.split(".")[-1]
    if file_extension not in allowed_extensions:
        raise HTTPException(status_code=400, detail="Invalid file format. Only CSV files are allowed.")

# Process the CSV files
def process_data(df1: pd.DataFrame, df2: pd.DataFrame) -> None:
    # Adding time delay of 60s
    # time.sleep(60)

    sum_df1 = df1['A'] + df1['B']
    sum_df2 = df2['A'] + df2['B']

    diff_df1 = df1['A'] - df1['B']
    diff_df2 = df2['A'] - df2['B']

    product_df1 = df1['C'] * df1['D']
    product_df2 = df2['C'] * df2['D']

    div_df1 = df1['C'] / df1['D']
    div_df2 = df2['C'] / df2['D']

    # Creating resultant dataframes
    result_df1 = pd.DataFrame({'E': sum_df1, 'F': diff_df1, 'G': product_df1, 'H': div_df1})
    result_df2 = pd.DataFrame({'E': sum_df2, 'F': diff_df2, 'G': product_df2, 'H': div_df2})

    return result_df1, result_df2

# Concurrently process the CSV files for each user
async def process_files(df1: pd.DataFrame, df2: pd.DataFrame, user_id: int) -> None:
    with concurrent.futures.ThreadPoolExecutor() as executor:
        loop = asyncio.get_event_loop()
        result_df1, result_df2 = await loop.run_in_executor(executor, process_data, df1, df2)

        # Convert the dataframes to JSON records
        result_json_1 = result_df1.to_json(orient='records')
        result_json_2 = result_df2.to_json(orient='records')

        # Store the result files in the results_dict
        with results_lock:
            results_dict[user_id] = {
                "result_1": json.loads(result_json_1),
                "result_2": json.loads(result_json_2)
            }


# -------------------------------API ENDPOINTS----------------------------------------------------------- #

# Base url
@app.get('/')
async def index():
    return {"message": "API is running succesfully"}

# Endpoint for reading and processing CSV files
@app.post("/read_data", status_code=status.HTTP_201_CREATED)
async def read_data(request: Request, dataset_1: UploadFile = File(...), dataset_2: UploadFile = File(...), user_id: str = Depends(validate_api_key)):
    validate_csv(dataset_1)
    validate_csv(dataset_2)

    df1 = read_csv_file(dataset_1.file)
    df2 = read_csv_file(dataset_2.file)

    await process_files(df1, df2, user_id)

    return {"message": "The CSV files have been read and processed successfully."}


# Endpoint for retrieving result Dataframes
@app.get("/get_results", status_code=status.HTTP_200_OK)
async def get_results(user_id: str = Depends(validate_api_key)):
    with results_lock:
        if user_id in results_dict:
            results = results_dict[user_id]
            del results_dict[user_id]

            return results
        else:
            raise HTTPException(status_code=404, detail="Result files not found.")






if __name__ == '__main__':
    uvicorn.run("main:app", host="localhost", port=8000, reload=True, workers=4)