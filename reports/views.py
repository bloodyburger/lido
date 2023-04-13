from django.http import HttpResponse
from django.shortcuts import render
from .models import Reports, ReportsConfig
import snowflake.connector
import json, pandas as pd


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
    string = 'a,b'
    result = ",".join(["'"+x+"'" for x in string.split(",")])
    print(result)
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
    if rc.show_token == "YES":
        field_list.append('TOKEN_SYMBOL')    

    if len(rc.primary_filters) > 5 :
        sf_filter = sf_filter
    #print(json.dumps(field_list, cls=UnquotedEncoder))
    #field_list = ['col1','col2']
    #print(make_query())
    return render(request, 'reports/report.html', context={'field_list': field_list, 'final_data': make_query(rc),'rc':rc})


def make_query(rc):
    token_symbol = {'0xc02aaa39b223fe8d0a0e5c4f27ead9083c756cc2':'ETH',
                    '0x6b175474e89094c44da98b954eedeac495271d0f':'DAI',
                    '0x7d1afa7b718fb893db30a3abc0cfc608aacfebb0':'MATIC',
                    '0xa0b86991c6218b36c1d19d4a2e9eb0ce3606eb48':'USDC',
                    '0xdac17f958d2ee523a2206206994597c13d831ec7':'USDT',
                    '7dHbWXmci3dT8UFYWYZweBLXgycu7Y3iL6trKn1Y7ARj':'SOL',
                    '0x5a98fcbea516cf06857215779fd812ca3bef1b32':'LDO'}
    
    conn = snowflake.connector.connect(
        user='READ_ONLY_LIDO',
        password='9dC8v5y9rQ6XqX',
        account='rha26240.us-east-1',
        warehouse='XS',
        database='user_tb',
        schema='PUBLIC'
    )
    cur = conn.cursor()
    query_filters = "WHERE "
    if len(rc.primary_filters) > 1:
        query_filters = query_filters + "PRIMARY_LABEL in ({}) AND ".format(",".join(["'"+x+"'" for x in rc.primary_filters.split(",")]))
    if len(rc.secondary_filters) > 1:
        query_filters = query_filters + "SECONDARY_LABEL in ({}) AND ".format(",".join(["'"+x+"'" for x in rc.secondary_filters.split(",")]))
    if len(rc.account_filters) > 1:
        query_filters = query_filters + "ACCOUNT in ({}) AND ".format(",".join(["'"+x+"'" for x in rc.account_filters.split(",")]))        
    
    query_filters = query_filters + " 1=1 "
    query_string = "select * from {} {} ".format(rc.source_table,query_filters)
    print("Query string is {}".format(query_string))
    cur.execute(query_string)
    df = cur.fetch_pandas_all()

    df['TOKEN_SYMBOL'] = df['BASE_TOKEN_ADDRESS'].map(token_symbol)
    if rc.filter_known_tokens:
        df = df[df['TOKEN_SYMBOL'].isin(['ETH','DAI','MATIC','USDC','USDT','SOL','LDO'])]
    
    if len(rc.fold_primary) > 3:
        print('Folding data for {}'.format(rc.fold_primary))
        print(rc.fold_primary.split(","))
        df_fold = df
        # exclude data to be folded
        #df = df[~df['PRIMARY_LABEL'].isin(rc.fold_primary.split(","))]
        # include only data to be folded
        df_fold = df_fold[df_fold['PRIMARY_LABEL'].isin(rc.fold_primary.split(","))]
        df_fold2 = df_fold.groupby(['PERIOD','PRIMARY_LABEL']).agg({'VALUE_ETH':'sum'}).reset_index()
        #df = pd.concat([df,df_fold2])
        #df_fold2.to_csv('fold.csv', header=True)
    df.to_csv('lido.csv',header=True)
    return df.to_json(orient='records')
