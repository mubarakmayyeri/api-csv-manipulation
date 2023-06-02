from fastapi import FastAPI, UploadFile, File
import pandas as pd
import uvicorn

app = FastAPI()

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

        # Calculate the sum of columns A and B from both CSV files
        sum_A = df1['A'] + df2['A']
        sum_B = df1['B'] + df2['B']

        # Calculate the product of columns C and D from both CSV files
        product_C = df1['C'] * df2['C']
        product_D = df1['D'] * df2['D']

        # Create a new DataFrame to store the results
        result_df = pd.DataFrame({'E': sum_A, 'F': sum_B, 'G': product_C, 'H': product_D})

        print("-------------------------------------")
        print("-------------------------------------")
        print("-------------------------------------")
        print(f'Results:\n{result_df.head()}')

        return {"message": "CSV files processed successfully"}

    except pd.errors.ParserError:
        raise HTTPException(status_code=400, detail="Invalid CSV file format.")



if __name__ == '__main__':
    uvicorn.run("main:app", host="localhost", port=8000, reload=True)