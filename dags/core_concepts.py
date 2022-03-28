from datetime import timedelta
import numbers
from airflow import DAG
from airflow.utils.dates import days_ago
from airflow.operators.bash_operator import BashOperator
from airflow.operators.python_operator import PythonOperator
from random import seed,random
default_arguments = {'owner':'Alexandra Abbas','start_date':days_ago(1)}
with DAG(
    'core_concepts',
    default_args=default_arguments,
    description='A simple tutorial DAG',
    schedule_interval=timedelta(days=1),
    start_date=days_ago(2),
    tags=['example'],
) as dag:

    bash_task = BashOperator(
     task_id="bash_task",
     bash_command='echo "Hi from bash operator"',
     env={"TODAY":"2020-05-21"})
     # output_encoding: str = 'utf-8',
     # skip_exit_code: int = 99,
    
    def print_random_number(numbers):
        seed(numbers)
        print(random())




    python_task = PythonOperator(
        task_id="python_task",
        python_callable=print_random_number,
        op_args=[1]

        
    )
 
bash_task >> python_task
 
