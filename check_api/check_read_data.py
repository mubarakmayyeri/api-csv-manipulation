import requests

def main():
    ip_address = 'localhost'

    url = f'http://{ip_address}:8000/read_data'
    path_1 = 'datasets/dataset_1.csv'
    path_2 = 'datasets/dataset_2.csv'


    files = {'dataset_1': open(path_1, 'rb'), 'dataset_2': open(path_2, 'rb')}
    response = requests.post(url, files=files)
    response_data = response.json()

    if response.status_code == 201:
        if 'message' in response_data:
            print(f"Success: {response.status_code} - {response_data['message']}")

    else:
        print(f"Error: {response.status_code} - {response_data['detail']}")

if __name__ == '__main__':
    main()