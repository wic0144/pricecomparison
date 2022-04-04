from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from airflow.models.baseoperator import chain
from airflow.contrib.operators.spark_submit_operator import SparkSubmitOperator
from airflow.models import Variable
from datetime import datetime, timedelta

# from scraper.JDCentralV203 import JdCentralData

seven_days_ago = datetime.combine(datetime.today() - timedelta(7),
                                datetime.min.time())
data = Variable.get("Date")
default_args = {
'owner': 'airflow',
'depends_on_past': False,
'start_date':seven_days_ago,
'scheduler_interval':f'{data}',
'email': ['Ruttanard.ru@mail.wu.ac.th'],
'email_on_failure': True,
'email_on_retry': True,
'retries': 1,
'retry_delay': timedelta(minutes=1),
}

dag = DAG('PriceComparerisonBlackBoneX', default_args=default_args)

JdCentralScraping= BashOperator(
task_id='CollectDataFromJDCentral',
bash_command='python3 /c/Users/OMEN/airflow/scraper/JDCentralV203.py',
dag=dag)

LazadaScraping = BashOperator(
task_id='CollectDataFromLAZADA',
bash_command='python3 /c/Users/OMEN/airflow/scraper/ScrapeLazada.py',
dag=dag)

ShopeeScraping = BashOperator(
task_id='CollectDataFromShopee',
bash_command='python3 /c/Users/OMEN/airflow/scraper/Shopee.py',
dag=dag)

PushAllDataIntoHadoop = BashOperator(
task_id='PushAllDataIntoHadoop',
bash_command='hdfs dfs -put -f /c/Users/OMEN/airflow/scraper/RawData/* /data_upload/master',
dag=dag)

FristPrep = SparkSubmitOperator(task_id='PrepFrist',
                                              conn_id='spark_standalone_cm',
                                              application='/c/Users/OMEN/airflow/DataPrep/PreprocessAll.py',
                                              conf={
            "spark.dynamicAllocation.enabled": "False"
        },
                                              dag=dag
                                              )

SecPrep = SparkSubmitOperator(task_id='PrepSec',
                                              conn_id='spark_standalone_cm',
                                              application='/c/Users/OMEN/airflow/DataPrep/Prefix.py',
                                              conf={
            "spark.dynamicAllocation.enabled": "False"
        },
                                              dag=dag
                                              )
PushFristPrep = BashOperator(
task_id='PushFristPrep',
bash_command='hdfs dfs -put -f /c/Users/OMEN/airflow/DataPrep/FinalData/JD+Shopee+Lazada.csv /data_upload/master',
dag=dag)

PushPrepDataSec = BashOperator(
task_id='PushSecPrep',
bash_command='hdfs dfs -put -f /c/Users/OMEN/airflow/DataPrep/FinalData/FinalResult.csv /data_upload/master',
dag=dag)



LoaddataToElas= BashOperator(
task_id='LoaddataToElas',
bash_command='python3 /c/Users/OMEN/airflow/Elasticsearch/LoadDataintoElastic.py',
dag=dag)

[JdCentralScraping,LazadaScraping,ShopeeScraping] >> PushAllDataIntoHadoop>>FristPrep >> PushFristPrep >> SecPrep >> PushPrepDataSec>>LoaddataToElas



# PushDataShopee = BashOperator(
# task_id='PushDataintoHadoopShopee',
# bash_command='hdfs dfs -put -f /c/Users/OMEN/airflow/scraper/RawData/Shopee.csv /data_upload/',
# dag=dag)

# PushDataLazada = BashOperator(
# task_id='PushDataintoHadoopLazada',
# bash_command='hdfs dfs -put -f /c/Users/OMEN/airflow/scraper/RawData/Lazada.csv /data_upload/',
# dag=dag)


# [JdCentralScraping,LazadaScraping,ShopeeScraping]>>[PushDataJDcentral,PushDataShopee,PushDataLazada]

# chain([JdCentralScraping,LazadaScraping,ShopeeScraping],[PushDataJDcentral,PushDataShopee,PushDataLazada])
