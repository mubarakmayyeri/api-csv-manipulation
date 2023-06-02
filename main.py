from fastapi import FastAPI, UploadFile, File
import pandas as pd
import uvicorn

app = FastAPI()

@app.post("/read_datasets")
async def process_csv(dataset_1: UploadFile = File(...), dataset_2: UploadFile = File(...)):
    # Read CSV files and convert to DataFrames
    df1 = pd.read_csv(dataset_1.file)
    df2 = pd.read_csv(dataset_2.file)

    print(f'Dataset 1: {df1.head()}')
    print("-------------------------------------")
    print(f'Dataset 2: {df2.head()}')

    return {"message": "CSV files processed successfully"}


if __name__ == '__main__':
    uvicorn.run("main:app", host="localhost", port=8000, reload=True)