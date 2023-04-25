from django.http import HttpResponse
from django.shortcuts import render
from .models import Reports, ReportsConfig
import snowflake.connector
import json
import pandas as pd
import os
from dune_client.types import QueryParameter
from dune_client.client import DuneClient
from dune_client.query import Query
from requests import get, post
import pandas as pd

BASE_URL = "https://api.dune.com/api/v1/"
API_KEY = "15CXPjYmpLvqTHrBkrkorrAFzRU0Vd6o"
HEADER = {"x-dune-api-key" : API_KEY}


def make_api_url(module, action, ID):
    """
    We shall use this function to generate a URL to call the API.
    """

    url = BASE_URL + module + "/" + ID + "/" + action

    return url

def index(request):
    """ main function that the home page

    Args:
        request (HttpRequest): incoming HTTP request

    Returns:
        HttpRequest: returns view that renders home page
    """    
    reports = Reports.objects.all()
    return render(request, "reports/index.html", context={"report_list": reports})


def generate_report(request, report_id):
    """ this function is responsible for reading the reports config
        and render the final template with parameters

    Args:
        request (HttpRequest): incoming HttpRequest
        report_id (int): ID of report to be generated

    Raises:
        DoesNotExist: if config for report is not found
        MultipleObjectsReturned: if duplicated config

    Returns:
        HttpRequest: render report view with parameters
    """    
    print("Selected Report id is {}".format(report_id))
    try:
        rc = ReportsConfig.objects.get(report_id=report_id)
    except ReportsConfig.DoesNotExist:
        raise Exception("Could not find the config")
    except ReportsConfig.MultipleObjectsReturned:
        raise Exception("Found too many entries for same report")

    value_col = rc.value_col
    field_list = []
    # Split the string and pass as list to template
    if rc.show_primary == "YES":
        field_list.append("PRIMARY_LABEL")
    if rc.show_secondary == "YES":
        field_list.append("SECONDARY_LABEL")
    if rc.show_account == "YES":
        field_list.append("ACCOUNT")
    if rc.show_category == "YES":
        field_list.append("CATEGORY")
    if rc.show_subcategory == "YES":
        field_list.append("SUBCATEGORY")
    if rc.show_token == "YES":
        field_list.append("TOKEN_SYMBOL")

    return render(
        request,
        "reports/report.html",
        context={"field_list": field_list, "final_data": make_query(rc), "rc": rc},
    )


def make_query(rc):
    """ method that build the query dynamically based on config

    Args:
        rc (QuerySet): Query result of config for selected report

    Returns:
        dataframe: dataframe of all values to be displayed on the report
    """    
    # translate token hash code to token string
    token_symbol = {
        "0xc02aaa39b223fe8d0a0e5c4f27ead9083c756cc2": "ETH",
        "0x6b175474e89094c44da98b954eedeac495271d0f": "DAI",
        "0x7d1afa7b718fb893db30a3abc0cfc608aacfebb0": "MATIC",
        "0xa0b86991c6218b36c1d19d4a2e9eb0ce3606eb48": "USDC",
        "0xdac17f958d2ee523a2206206994597c13d831ec7": "USDT",
        "7dHbWXmci3dT8UFYWYZweBLXgycu7Y3iL6trKn1Y7ARj": "SOL",
        "0x5a98fcbea516cf06857215779fd812ca3bef1b32": "LDO",
    }
    # connect to Snowflake
    conn = snowflake.connector.connect(
        user=os.environ.get("SNOWFLAKE_USER"),
        password=os.environ.get("SNOWFLAKE_PASSWORD"),
        account=os.environ.get("SNOWFLAKE_ACCOUNT"),
        warehouse=os.environ.get("SNOWFLAKE_WAREHOUSE"),
        database=os.environ.get("SNOWFLAKE_DATABASE"),
        schema=os.environ.get("SNOWFLAKE_SCHEMA"),
    )
    cur = conn.cursor()
    # Build the query dynamically
    query_filters = "WHERE "
    if len(rc.primary_filters) > 1:
        query_filters = query_filters + "PRIMARY_LABEL in ({}) AND ".format(
            ",".join(["'" + x + "'" for x in rc.primary_filters.split(",")])
        )
    if len(rc.secondary_filters) > 1:
        query_filters = query_filters + "SECONDARY_LABEL in ({}) AND ".format(
            ",".join(["'" + x + "'" for x in rc.secondary_filters.split(",")])
        )
    if len(rc.account_filters) > 1:
        query_filters = query_filters + "ACCOUNT in ({}) AND ".format(
            ",".join(["'" + x + "'" for x in rc.account_filters.split(",")])
        )

    query_filters = query_filters + " 1=1 "
    query_string = "select * from {} {} ".format(rc.source_table, query_filters)
    print("Query string is {}".format(query_string))
    # fire the query on Snowflake
    cur.execute(query_string)
    df = cur.fetch_pandas_all()
    # filter toekns if configured
    df["TOKEN_SYMBOL"] = df["BASE_TOKEN_ADDRESS"].map(token_symbol)
    if rc.filter_known_tokens:
        df = df[
            df["TOKEN_SYMBOL"].isin(
                ["ETH", "DAI", "MATIC", "USDC", "USDT", "SOL", "LDO"]
            )
        ]
    # unused
    if len(rc.fold_primary) > 3:
        print("Folding data for {}".format(rc.fold_primary))
        print(rc.fold_primary.split(","))
        df_fold = df
        # exclude data to be folded
        # df = df[~df['PRIMARY_LABEL'].isin(rc.fold_primary.split(","))]
        # include only data to be folded
        df_fold = df_fold[df_fold["PRIMARY_LABEL"].isin(rc.fold_primary.split(","))]
        df_fold2 = (
            df_fold.groupby(["PERIOD", "PRIMARY_LABEL"])
            .agg({"VALUE_ETH": "sum"})
            .reset_index()
        )
        # df = pd.concat([df,df_fold2])
        # df_fold2.to_csv('fold.csv', header=True)
    df.to_csv("lido.csv", header=True)
    return df.to_json(orient="records")

def pull_data_from_dune(request):
    query = Query(
    name="@pipistrella / Lido Protocol Economics (Daily) with eth value/trp",
    query_id=2248762,
    params=[
        QueryParameter.date_type(name="date_from", value="2023-04-22 00:00:00"),
    ],
)
    #print("Results available at", query.url())

    #dotenv.load_dotenv()
    dune = DuneClient("15CXPjYmpLvqTHrBkrkorrAFzRU0Vd6o")
    data = dune.refresh_into_dataframe(query)
    data.to_csv('dune_results.csv', header=True)
    #execution_id = execute_query("2248762","large")
    ##print('Execution id is {}'.format(execution_id))
    #response_status = get_query_status(execution_id)
    #print("Response status {}".format(response_status.json()['execution_id']))
    #while get_query_status(execution_id).json()['state'] == 'QUERY_STATE_COMPLETED':
    #    response = get_query_results(execution_id)
    #    print('Query response is {}'.format(response.json()))
    #    data = pd.DataFrame(response.json()['result']['rows'])
    #    data.to_csv('dune_results.csv', header=True)



def execute_query(query_id, engine="medium"):
    """
    Takes in the query ID and engine size.
    Specifying the engine size will change how quickly your query runs. 
    The default is "medium" which spends 10 credits, while "large" spends 20 credits.
    Calls the API to execute the query.
    Returns the execution ID of the instance which is executing the query.
    """

    url = make_api_url("query", "execute", query_id)
    params = {
        "performance": engine,
    }
    response = post(url, headers=HEADER, params=params)
    execution_id = response.json()['execution_id']

    return execution_id


def get_query_status(execution_id):
    """
    Takes in an execution ID.
    Fetches the status of query execution using the API
    Returns the status response object
    """

    url = make_api_url("execution", "status", execution_id)
    response = get(url, headers=HEADER)

    return response


def get_query_results(execution_id):
    """
    Takes in an execution ID.
    Fetches the results returned from the query using the API
    Returns the results response object
    """

    url = make_api_url("execution", "results", execution_id)
    response = get(url, headers=HEADER)

    return response


def cancel_query_execution(execution_id):
    """
    Takes in an execution ID.
    Cancels the ongoing execution of the query.
    Returns the response object.
    """

    url = make_api_url("execution", "cancel", execution_id)
    response = get(url, headers=HEADER)

    return response
