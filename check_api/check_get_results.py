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

    response = requests.get(api_endpoint, stream=True)

    if response.status_code == 200:
        zip_file_path = os.path.join(results_path, "results.zip")
        with open(zip_file_path, "wb") as file:
            for chunk in response.iter_content(chunk_size=128):
                file.write(chunk)
        print("Results downloaded successfully.")
    else:
        response_data = response.json()
        print(f"Error: {response.status_code} - {response_data['detail']}")

if __name__ == '__main__':
    main()