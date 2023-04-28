from django.http import HttpResponse
from django.shortcuts import render
from .models import Reports, ReportsConfig
import snowflake.connector
import json
import pandas as pd
import os

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

    drilldown_cols = ",".join(["'" + x.strip() + "'" for x in rc.drilldown_cols.split(",")])  
    print("Drilldown cols are {}".format(drilldown_cols))  

    return render(
        request,
        "reports/report.html",
        context={"field_list": field_list, "final_data": make_query(rc), "rc": rc, "drilldown_cols":drilldown_cols},
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

    df.to_csv("lido.csv", header=True)
    return df.to_json(orient="records")

