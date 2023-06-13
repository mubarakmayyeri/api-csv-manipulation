from decouple import config
import requests
import json
import os

def main():
    base_dir = os.path.dirname(os.path.abspath(__file__))

    result_dir = os.path.join(base_dir, 'results')

    if not os.path.exists(result_dir):
        os.makedirs(result_dir)

    results_path = result_dir

    ip_address = config('IP_ADDRESS')

    # API key
    api_key = config('API_KEY')

    url = f'http://{ip_address}/process_datasets'

    headers = {
        'X-API-Key': api_key
    }

    path_1 = os.path.join(base_dir, 'datasets/dataset_1.csv')
    path_2 = os.path.join(base_dir, 'datasets/dataset_2.csv')

    files = {'dataset_1': open(path_1, 'rb'), 'dataset_2': open(path_2, 'rb')}

    response = requests.post(url, headers=headers, files=files)
    
    if response.status_code == 500:
        print(f"Error: {response.status_code} - {response.text}")

        return

    response_data = response.json()

    if response.status_code == 201:

        # Extract the result data
        result_df1 = response_data.get('result_1')
        result_df2 = response_data.get('result_2')

        # Save result dataframes to local files
        with open(f'{results_path}/result_df1.json', 'w') as file:
            json.dump(result_df1, file)

        with open(f'{results_path}/result_df2.json', 'w') as file:
            json.dump(result_df2, file)

        print(f"Success: {response.status_code} - Result dataframes saved successfully.")

    else:
        print(f"Error: {response.status_code} - {response_data['detail']}")

if __name__ == '__main__':
    main()