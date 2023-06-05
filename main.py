from fastapi import FastAPI, UploadFile, File, HTTPException, status
import pandas as pd
import json
import time
import os
import uvicorn

app = FastAPI()

# Path for storing result csv files
base_dir = os.path.dirname(os.path.abspath(__file__))
result_dir = os.path.join(base_dir, 'results')

if not os.path.exists(result_dir):
    os.makedirs(result_dir)

results_path = result_dir

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
    time.sleep(60)

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

# Generating result files
def generate_result_files(result_df1: pd.DataFrame, result_df2: pd.DataFrame) -> None:
    result_json_1 = result_df1.to_json(orient='records')
    result_json_2 = result_df2.to_json(orient='records')

    with open(f'{results_path}/result_1.json', 'w') as file:
        file.write(result_json_1)

    with open(f'{results_path}/result_2.json', 'w') as file:
        file.write(result_json_2)

@app.get('/')
async def index():
    return {"message": "API is running succesfully"}

# Endpoint for reading and processing CSV files
@app.post("/read_data", status_code=status.HTTP_201_CREATED)
async def read_data(dataset_1: UploadFile = File(...), dataset_2: UploadFile = File(...)):
    validate_csv(dataset_1)
    validate_csv(dataset_2)

    df1 = read_csv_file(dataset_1.file)
    df2 = read_csv_file(dataset_2.file)

    result_df1, result_df2 = process_data(df1, df2)

    generate_result_files(result_df1, result_df2)

    return {"message": "CSV files read and processed successfully"}

@app.get("/get_results")
async def get_result_files():

    try:
        file_path_1 = os.path.join(results_path, 'result_1.json')
        file_path_2 = os.path.join(results_path, 'result_2.json')

        with open(file_path_1) as file:
            result_json_1 = file.read()

        with open(file_path_2) as file:
            result_json_2 = file.read()

        # Removing the sotred result JSON files
        os.remove(file_path_1)
        os.remove(file_path_2)

        return {"result_df1": json.loads(result_json_1), "result_df2": json.loads(result_json_2)}

    except FileNotFoundError:
        raise HTTPException(detail="Result files not found.", status_code=status.HTTP_404_NOT_FOUND)

    except FileNotFoundError:
        raise HTTPException(detail="Result files not found.", status_code=status.HTTP_404_NOT_FOUND)



if __name__ == '__main__':
    uvicorn.run("main:app", host="localhost", port=8000, reload=True)