import requests
import os

def main():

    ip_address = 'localhost'

    # Path for storing result csv files
    base_dir = os.path.dirname(os.path.abspath(__file__))
    result_dir = os.path.join(base_dir, 'results')

    if not os.path.exists(result_dir):
        os.makedirs(result_dir)

    results_path = result_dir

    api_endpoint = f'http://{ip_address}:8000/get_results'

    response = requests.get(api_endpoint)

    if response.status_code == 200:
        files_data = response.json()

        for i, file_data in enumerate(files_data):
            file_path = file_data['path']
            filename = f'result_{i+1}.csv'
            
            try:
                with open(file_path, 'rb') as file:
                    file_content = file.read()
                    with open(os.path.join(result_dir, filename), 'wb') as result_file:
                        result_file.write(file_content)
                print(f"File '{filename}' downloaded successfully.")

            except FileNotFoundError:
                print(f"Error occurred while retrieving file '{filename}'. File not found.")
            except IOError:
                print(f"Error occurred while reading file '{filename}'.")

    else:
        print("Error occurred while retrieving the result files.")
        response_data = response.json()
        print(response_data['detail'])

if __name__ == '__main__':
    main()