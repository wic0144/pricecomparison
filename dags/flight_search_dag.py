from datetime import datetime, timedelta
import pendulum
from airflow import DAG
from airflow.contrib.operators.spark_submit_operator import SparkSubmitOperator
from airflow.models import Variable

local_tz = pendulum.timezone("Asia/Tehran")

default_args = {
    'owner': 'mahdyne',
    'depends_on_past': False,
    'start_date': datetime(2020, 10, 10, tzinfo=local_tz)
}
dag = DAG(dag_id='Pyspark',
          default_args=default_args,
          catchup=False,
          schedule_interval="0 * * * *")
pyspark_app_home = Variable.get("PYSPARK_APP_HOME")

flight_search_ingestion = SparkSubmitOperator(task_id='spark_test2',
                                              conn_id='spark_standalone_cm',
                                              application='/c/Users/OMEN/airflow/DataPrep/PreprocessAll.py',
                                            #   total_executor_cores=1,                                         
                                            #   executor_cores=2,
                                            #   executor_memory='2g',
                                            #   driver_memory='2g',
                                            #   execution_timeout=timedelta(minutes=20),
                                              conf={
            "spark.dynamicAllocation.enabled": "False"
        },
                                              dag=dag
                                              )

flight_search_ingestion 


# f'{pyspark_app_home}/spark/search_event_ingestor.py',