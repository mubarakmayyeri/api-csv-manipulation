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
    response_data = response.json()

    if response.status_code == 200:

        print(response_data)

        # # Extract the result data
        # result_df1 = response_data.get('result_df1')
        # result_df2 = response_data.get('result_df2')

        # # Process or display the result data as needed
        # print("Result DataFrame 1:")
        # print(result_df1)

        # print(("------------------------------------------------"))
        # print(("------------------------------------------------"))
        # print(("------------------------------------------------"))

        # print("Result DataFrame 2:")
        # print(result_df2)

    else:
        print(f"Error: {response.status_code} - {response_data['detail']}")

if __name__ == '__main__':
    main()