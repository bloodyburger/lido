from django.http import HttpResponse
from .models import Reports, ReportsConfig
import snowflake.connector
import json, time
import pandas as pd
import os
import psycopg2
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from .models import Uploads
from .forms import UploadForm
from django.http import HttpResponseRedirect
from .utils import process_postgresql, send_email
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect


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
    start = time.process_time()
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
    print("Time to render the view is {}".format(time.process_time() - start))
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
        "0x7d1afa7b718fb893db30a3abc0cfc608aacfebb0": "MATIC1",
        "0xa0b86991c6218b36c1d19d4a2e9eb0ce3606eb48": "USDC",
        "0xdac17f958d2ee523a2206206994597c13d831ec7": "USDT",
        "7dHbWXmci3dT8UFYWYZweBLXgycu7Y3iL6trKn1Y7ARj": "SOL1",
        "0x5a98fcbea516cf06857215779fd812ca3bef1b32": "LDO",
    }
    # connect to Snowflake
    #conn = snowflake.connector.connect(
    ##    user=os.environ.get("SNOWFLAKE_USER"),
    #    password=os.environ.get("SNOWFLAKE_PASSWORD"),
    #    account=os.environ.get("SNOWFLAKE_ACCOUNT"),
    #    warehouse=os.environ.get("SNOWFLAKE_WAREHOUSE"),
    #    database=os.environ.get("SNOWFLAKE_DATABASE"),
    #    schema=os.environ.get("SNOWFLAKE_SCHEMA"),
    #)
    conn = psycopg2.connect(database = os.environ.get("PG_DATABASE"), 
                        user = os.environ.get("PG_USER"), 
                        host= os.environ.get("PG_HOST"),
                        password = os.environ.get("PG_PASSWORD"),
                        port = os.environ.get("PG_PORT"))
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
    start = time.process_time()
    cur.execute(query_string)
    # fetch all rows and convert to a DataFrame
    df = pd.DataFrame(cur.fetchall(), columns=[desc[0] for desc in cur.description])
    df.columns = map(lambda x: str(x).upper(), df.columns)
    print("Runtime for data extraction from DB is {}".format(time.process_time() - start))
    # close the cursor and connection
    cur.close()
    conn.close()
    #df = cur.fetch_pandas_all()
    # filter toekns if configured
    df["TOKEN_SYMBOL"] = df["BASE_TOKEN_ADDRESS"].map(token_symbol)
    if rc.filter_known_tokens:
        df = df[
            df["TOKEN_SYMBOL"].isin(
                ["ETH", "DAI", "MATIC", "USDC", "USDT", "SOL", "LDO"]
            )
        ]

    #df.to_csv("lido.csv", header=True)
    #df.to_json('data.json',orient="records")
    return df.to_json(orient="records")

@login_required
def upload_file(request):
    if request.method == 'POST':
        form = UploadForm(request.POST, request.FILES)
        upload_file = request.FILES['document']
        if form.is_valid():
            df = pd.read_csv(upload_file)
            process_postgresql(df)
            print(df.columns)
            form.save()
            send_email("File upload to pgsql","Data loaded from File to Postgresql successful")
            return HttpResponseRedirect("/") 
    else:
        form = UploadForm
    return render(request, 'reports/upload.html', {'form':form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('upload')
    else:
        form = AuthenticationForm(request)
    
    return render(request, 'reports/login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('login')