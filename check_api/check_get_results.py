from decouple import config
import requests
import os
import json

def main():

    ip_address = config('IP_ADDRESS')

    # API key
    api_key = config('API_KEY')

    # Path for storing result csv files
    base_dir = os.path.dirname(os.path.abspath(__file__))
    result_dir = os.path.join(base_dir, 'results')

    if not os.path.exists(result_dir):
        os.makedirs(result_dir)

    results_path = result_dir

    api_endpoint = f'http://{ip_address}/get_results'

    headers = {
        'X-API-Key': api_key
    }

    response = requests.get(api_endpoint, headers=headers)

    if response.status_code == 500:
        print(f"Error: {response.status_code} - {response.text}")

        return

    response_data = response.json()

    if response.status_code == 200:

        # Extract the result data
        result_df1 = response_data.get('result_df1')
        result_df2 = response_data.get('result_df2')

        # Save result dataframes to local files
        with open(f'{results_path}/result_df1.json', 'w') as file:
            json.dump(result_df1, file)

        with open(f'{results_path}/result_df2.json', 'w') as file:
            json.dump(result_df2, file)

        # # Process or display the result data as needed
        # print("Result DataFrame 1:")
        # print(result_df1)

        # print(("------------------------------------------------"))
        # print(("------------------------------------------------"))
        # print(("------------------------------------------------"))

        # print("Result DataFrame 2:")
        # print(result_df2)

        print("Result dataframes saved successfully.")

    else:
        print(f"Error: {response.status_code} - {response_data['detail']}")

if __name__ == '__main__':
    main()