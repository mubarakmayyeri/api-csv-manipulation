from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import FileResponse
import pandas as pd
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

def process_data(df1: pd.DataFrame, df2: pd.DataFrame) -> None:
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


    # generate_result_files(result_df1, result_df2)

    return result_df1, result_df2

# Generating result files
def generate_result_files(result_df1: pd.DataFrame, result_df2: pd.DataFrame) -> None:

    # Adding time delay of 60s
    time.sleep(60)

    result_df1.to_csv(f'{results_path}/result_1.csv', index=False)
    result_df2.to_csv(f'{results_path}/result_2.csv', index=False)

@app.post("/read_data")
async def read_data(dataset_1: UploadFile = File(...), dataset_2: UploadFile = File(...)):

    df1 = read_csv_file(dataset_1.file)
    df2 = read_csv_file(dataset_2.file)

    result_df1, result_df2 = process_data(df1, df2)

    generate_result_files(result_df1, result_df2)

    return {"message": "CSV files read and processed successfully"}

@app.get("/get_results")
async def get_result_files():

    file_path_1 = os.path.join(results_path, 'result_1.csv')
    file_path_2 = os.path.join(results_path, 'result_2.csv')

    if not os.path.exists(file_path_1) or not os.path.exists(file_path_2):
        raise HTTPException(status_code=404, detail="Result files not found.")

    # Return both csv files as FileResponse
    response = [
        FileResponse(file_path_1, filename='result_1.csv'),
        FileResponse(file_path_2, filename='result_2.csv')
    ]

    return response



if __name__ == '__main__':
    uvicorn.run("main:app", host="localhost", port=8000, reload=True)