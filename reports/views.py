from django.http import HttpResponse
from django.shortcuts import render
from .models import Reports, ReportsConfig
import snowflake.connector
import json


def index(request):
    # return HttpResponse("Hello, world. You're at the polls index.")
    conn = snowflake.connector.connect(
        user='READ_ONLY_LIDO',
        password='9dC8v5y9rQ6XqX',
        account='rha26240.us-east-1',
        warehouse='XS',
        database='user_tb',
        schema='PUBLIC'
    )
    cur = conn.cursor()
    #cur.execute('select * from LIDO_DEV limit 500')
    #df = cur.fetch_pandas_all()
    #df.to_csv('lido_snowflake.csv', header=True)
    reports = Reports.objects.all()
    return render(request, 'reports/index.html', context={'report_list': reports})


def generate_report(request, report_id):
    print('Selected Report id is {}'.format(report_id))
    try:
        rc = ReportsConfig.objects.get(report_id=report_id)
    except ReportsConfig.DoesNotExist:
        raise Exception("Could not find the config")
    except ReportsConfig.MultipleObjectsReturned:
        raise Exception("Found too many entries for same report")

    value_col = rc.value_col
    field_list = []
    if rc.show_primary == "YES":
        field_list.append('PRIMARY_LABEL')
    if rc.show_secondary == "YES":
        field_list.append('SECONDARY_LABEL')
    if rc.show_account == "YES":
        field_list.append('ACCOUNT')
    if rc.show_category == "YES":
        field_list.append('CATEGORY')
    if rc.show_subcategory == "YES":
        field_list.append('SUBCATEGORY')

    if len(rc.primary_filters) > 5 :
        sf_filter = sf_filter
    #print(json.dumps(field_list, cls=UnquotedEncoder))
    #field_list = ['col1','col2']
    print(make_query())
    return render(request, 'reports/report.html', context={'field_list': field_list, 'final_data': make_query(),'value_col':value_col})


def make_query():
    conn = snowflake.connector.connect(
        user='READ_ONLY_LIDO',
        password='9dC8v5y9rQ6XqX',
        account='rha26240.us-east-1',
        warehouse='XS',
        database='user_tb',
        schema='PUBLIC'
    )
    cur = conn.cursor()
    cur.execute('select * from LIDO_DEV')
    df = cur.fetch_pandas_all()
    return df.to_json(orient='records')
