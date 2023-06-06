from decouple import config
import requests
import json
import os

def main():
    base_dir = os.path.dirname(os.path.abspath(__file__))

    ip_address = config('IP_ADDRESS')

    # API key
    api_key = config('API_KEY')

    url = f'http://{ip_address}/read_data'

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
        print(f'Success: {response.status_code}:', end=' ')
        if 'message' in response_data:
            print(f"- {response_data['message']}")

    else:
        print(f"Error: {response.status_code} - {response_data['detail']}")

if __name__ == '__main__':
    main()