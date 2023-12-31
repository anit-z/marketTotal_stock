import requests
import json
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import rcParams
rcParams['font.family'] = 'SimHei'


# The API endpoint for the POST request
url = "https://v1.cn-abs.com/ajax/ChartMarketHandler.ashx"

# Headers
headers = {
    "Accept": "application/json, text/javascript, */*; q=0.01",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7",
    "Connection": "keep-alive",
    "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
    "Host": "v1.cn-abs.com",
    "Origin": "https://v1.cn-abs.com",
    "Referer": "https://v1.cn-abs.com/",
    "X-Requested-With": "XMLHttpRequest",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36",
}

# Payload for the POST request
payload = {    
    'type': 'marketTotal' # 产品存量规模
}


def fetch_data(url, headers, data):
    """
    Fetches data from the URL using a POST request.
    
    Args:
        url (str): The URL to which the POST request is made.
        headers (dict): Headers to include in the request.
        data (dict): Data to send in the body of the POST request.
        
    Returns:
        The response from the server.
    """
    response = requests.post(url, headers=headers, data=data)
    
    if response.status_code == 200:
        # Assuming the response's content is JSON, parse and return it.
        # If the response is in another format, this line will need to change.
        res = response.json()
        return res
    else:
        print("Failed to retrieve content, status code:", response.status_code)
        return None


def main(data):
    # Fetch and process data from the API
    response = fetch_data(url, headers, data)
    
    if response is not None:
        print("Response from server:", response)
        # Further processing can be done here depending on the structure of response
    return response


def data_parse(data):
    """
    Parses the given data and returns a dictionary containing the parsed information.
    
    Parameters:
        data (list): A list of dictionaries containing the data to be parsed.
        
    Returns:
        dict: A dictionary containing the parsed information. 
    """
    res = {'存量金额': []}
    for item in data:
        # print(item)
        if item['SeriesName']:
            type = item['SeriesName']
            # print('type: ', type)
            type_data = []
            points = item['Points']
            # print('points: ', points)
            value = points[1]['Y'][0]
            # print('value: ', value)
            res['存量金额'].append({type: value})
        
    return res


def data2df(data):
    """
    Convert data to a DataFrame.

    Args:
        data (dict): A dictionary containing the data.

    Returns:
        pandas.DataFrame: The DataFrame containing the converted data.
    """
    # Converting data to DataFrame
    # First, flatten the data into a list of tuples (category, value)
    flat_list = [(k, v) for d in data['存量金额'] for k, v in d.items()]

    # Create DataFrame
    df_financial_products = pd.DataFrame(flat_list, columns=['Product Type', 'Stock Amount'])
    df_financial_products = df_financial_products.sort_values(by='Stock Amount', ascending=False)

    # Reset index after sorting
    df_financial_products = df_financial_products.reset_index(drop=True)

    return df_financial_products


def save_to_csv(df, fileName):
    """
    Save DataFrame to CSV file.

    Parameters:
    - df (DataFrame): The DataFrame to be saved.

    Returns:
    - None
    """
    # Save DataFrame to CSV file
    df.to_csv('./data/{}.csv'.format(fileName))


def visualization(df):
    """
    Visualizes the data in a line plot.

    Parameters:
    - df: The data to be visualized.

    Returns:
    None
    """
    # Visualizing the data
    # Visualize with a bar chart
    plt.figure(figsize=(14, 8))
    plt.barh(df['Product Type'][::-1], df['Stock Amount'][::-1])  # Reverse the order for descending bar plot
    plt.xlabel('Value')
    plt.ylabel('Type')
    plt.title('Product stock scale')
    plt.grid(True)
    plt.show()


if __name__ == '__main__':
    payload = {    
        'type': 'marketTotal' # 产品存量规模
    }
    data = main(data=payload)
    print(data)

    data = data_parse(data)
    print(data)

    df = data2df(data)
    print(df)

    visualization(df)

    file_name = 'marketTotal_stock'
    save_to_csv(df, file_name)