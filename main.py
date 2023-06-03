from fastapi import FastAPI, UploadFile, File
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

@app.post("/process_csv")
async def process_csv(dataset_1: UploadFile = File(...), dataset_2: UploadFile = File(...)):

    allowed_extensions = ['.csv']
    try:
        # Read the CSV files as DataFrames
        df1 = pd.read_csv(dataset_1.file)
        df2 = pd.read_csv(dataset_2.file)

        # Printing the datasets
        print(f'Dataset 1: {df1.head()}')
        print("-------------------------------------")
        print("-------------------------------------")
        print("-------------------------------------")
        print(f'Dataset 2: {df2.head()}')

        # Processing the dataframes
        sum_df1 = df1['A'] + df1['B']
        sum_df2 = df2['A'] + df2['B']

        diff_df1 = df1['A'] - df1['B']
        diff_df2 = df2['A'] - df2['B']

        product_df1 = df1['C'] * df1['D']
        product_df2 = df2['C'] * df2['D']

        div_df1 = df1['C'] / df1['D']
        div_df2 = df2['C'] / df2['D']

        # Adding time delay of 60s
        time.sleep(60)

        # Creating resulutant dataframes
        result_df1 = pd.DataFrame({'E': sum_df1, 'F': diff_df1, 'G': product_df1, 'H': div_df1})
        result_df2 = pd.DataFrame({'E': sum_df2, 'F': diff_df2, 'G': product_df2, 'H': div_df2})\

        # Printing the reulst dataframes
        print("-------------------------------------")
        print("-------------------------------------")
        print("-------------------------------------")
        print('Results:')
        print(f'Ouput_1:\n{result_df1.head()}')
        print("-------------------------------------")
        print(f'Ouput_1:\n{result_df2.head()}')

        # Generating output csv files
        result_1 = result_df1.to_csv(f'{results_path}/result_1.csv', index=False)
        result_2 = result_df1.to_csv(f'{results_path}/result_2.csv', index=False)

        return {"message": "CSV files processed successfully"}

    except pd.errors.ParserError:
        raise HTTPException(status_code=400, detail="Invalid CSV file format.")



if __name__ == '__main__':
    uvicorn.run("main:app", host="localhost", port=8000, reload=True)