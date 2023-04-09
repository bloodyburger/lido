from django.http import HttpResponse
from django.shortcuts import render
from .models import Reports, ReportsConfig
import snowflake.connector
import json


def index(request):
    #return HttpResponse("Hello, world. You're at the polls index.")
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
    return render(request, 'reports/index.html',context={'report_list':reports})

def generate_report(request, report_id):
    print('Selected Report id is {}'.format(report_id))
    try:
        rc = ReportsConfig.objects.get(report_id = report_id)
    except ReportsConfig.DoesNotExist:
        raise Exception("Could not find the config")
    except ReportsConfig.MultipleObjectsReturned:
        raise Exception("Found too many entries for same report")    
    print(rc.show_secondary, rc.show_primary)
    field_list = []
    if rc.show_primary == "YES":
        field_list.append('primary_label')
    if rc.show_secondary == "YES":
        field_list.append('secondary_label')    
    #print(json.dumps(field_list, cls=UnquotedEncoder))    
    return render(request, 'reports/report.html', context={'field_list': field_list})
