import time
from typing import Final

import matplotlib.pyplot as plt
import requests
from pandas import DataFrame, Timestamp
from requests import Response
from tqdm import tqdm

from config import API_KEY, API_URL

PAGE_SIZE: Final[int] = 50
N_API_RETRIES: Final[int] = 5


def get_query(page_number: int) -> str:
    """
    Define the GraphQL query.

    :param page_number: Page number.
    :return: Query string.
    """
    query: str = """
            query {
                rekts(
                    pageNumber: %i
                    pageSize: %i
                ) {
                    id
                    date
                    projectName
                    category
                    fundsLost
                    issueType
                }
            }
        """ % (
        page_number,
        PAGE_SIZE,
    )
    return query


def get_data() -> list:
    """
    Collect all data from GraphQL API.

    :return: Data from rekts DB.
    """
    # Send the request to the API.
    headers: Final[dict] = {"X-Api-Key": str(API_KEY)}

    # First page = 50 items.
    query: str = get_query(page_number=1)
    response: Response = requests.post(API_URL, json={"query": query}, headers=headers)
    data: list = response.json()["data"]["rekts"]

    # NOTE: rate limit for "rekts" API endpoint is 100 calls / sec.
    total_batches: int = data[0]["id"] // PAGE_SIZE
    total_batches: int = (
        total_batches + 1 if data[0]["id"] % PAGE_SIZE else total_batches
    )
    for batch_it in tqdm(range(2, total_batches + 1)):
        # Get query string
        query: str = get_query(page_number=batch_it)

        # Retry the request
        for i in range(N_API_RETRIES):
            try:
                # Get partial data
                response: Response = requests.post(
                    API_URL, json={"query": query}, headers=headers
                )
                # If request is successful, break the loop.
                if response.status_code == 200:
                    break
            except requests.exceptions.RequestException:
                # If there is an exception, wait for 2 seconds before retrying.
                time.sleep(2)

        # Check if the request was successful.
        if response.status_code != 200:
            raise ValueError("Request failed after 5 retries.")

        # Append data
        partial_data: list = response.json()["data"]["rekts"]
        data: list = data + partial_data

    return data


def visualize_history(data: DataFrame, name: str) -> None:
    """
    Visualize historical graph for an 'name' type of incidents.

    :param data: Data issue incidents.
    :param name: Issue name.
    :return: None.
    """
    # Clear data.
    data: DataFrame = data.dropna(subset=["date"])
    # Set index.
    data.index = [Timestamp(x) for x in data["date"]]
    data: DataFrame = data.drop(columns="date")
    # Sort by index = date.
    data: DataFrame = data.sort_index()
    # Set datatypes
    data: DataFrame = data.astype(
        {
            "id": "int",
            "projectName": "str",
            "category": "str",
            "fundsLost": "int",
            "issueType": "str",
        }
    )
    # Calculate cumulative sums.
    data["cumsum"] = data["fundsLost"].cumsum()
    # Create new column 'occurrences' in DF and create a range.
    data: DataFrame = data.assign(occurrences=range(1, len(data) + 1))

    # Plots:
    plt.title(f"{name} - Cumulative Sum")
    plt.step(data.index, data["cumsum"])
    plt.xlabel("Time")
    plt.ylabel("Funds Lost in USD")
    plt.gcf().autofmt_xdate()
    plt.grid(True)
    plt.savefig(
        f"./graphs/cumsum_{name.lower().replace(' ', '_')}.pdf",
        format="pdf",
        bbox_inches="tight",
    )
    plt.show()

    plt.title(f"{name} - Cumulative Sum Log Scale")
    plt.step(data.index, data["cumsum"])
    plt.xlabel("Time")
    plt.ylabel("Funds Lost in USD")
    plt.gcf().autofmt_xdate()
    plt.yscale("log")
    plt.grid(True)
    plt.savefig(
        f"./graphs/logscale_cumsum_{name.lower().replace(' ', '_')}.pdf",
        format="pdf",
        bbox_inches="tight",
    )
    plt.show()

    plt.title(f"{name} - Cumulative Sum of Issue Occurrences")
    plt.step(data.index, data["occurrences"])
    plt.xlabel("Time")
    plt.ylabel("Number of Issues")
    plt.gcf().autofmt_xdate()
    plt.grid(True)
    plt.savefig(
        f"./graphs/occurrences_{name.lower().replace(' ', '_')}.pdf",
        format="pdf",
        bbox_inches="tight",
    )
    plt.show()


if __name__ == "__main__":
    """
    Main entrypoint.

    The script gather data from 'rekts' GraphQL API endpoint and plots:
    1) Cumulative sums of lost funds in specific issue type.
    2) Cumulative sums of issue occurrences.
    """
    print("Getting data from 'rekts' API endpoint:")
    full_data: DataFrame = DataFrame(get_data())
    grouped_data = full_data.groupby("issueType")

    names: list[str] = list(map(str, grouped_data.groups.keys()))
    for issue_name in names:
        print(f"Processing: {issue_name}")
        visualize_history(data=grouped_data.get_group(issue_name), name=issue_name)
