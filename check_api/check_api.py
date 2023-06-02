import requests

def main():
    url = 'http://localhost:8000/read_datasets'
    path_1 = 'datasets/dataset_1.csv'
    path_2 = 'datasets/dataset_2.csv'


    files = {'dataset_1': open(path_1, 'rb'), 'dataset_2': open(path_2, 'rb')}
    response = requests.post(url, files=files)

    if response.status_code == 200:
        response_data = response.json()
        if 'message' in response_data:
            print("Response message:", response_data['message'])

    else:
        print("An error occurred.")

if __name__ == '__main__':
    main()