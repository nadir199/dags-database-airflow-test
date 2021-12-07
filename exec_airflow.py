from datetime import timedelta

from airflow import DAG

from airflow.utils.dates import days_ago
from airflow.operators.bash import BashOperator

from airflow.providers.cncf.kubernetes.operators.kubernetes_pod import KubernetesPodOperator
import os

print("STARTING DG CREATION")

default_args = {
	"owner" : "airflow",
	"depends_on_past" : False,
	"email" : ["airflow@example.com"],
	"email_on_failure" : False,
	"email_on_retry" : False,
	"retries" : 1,
	"retry_delay" : timedelta(minutes = 5),
}

with DAG(
	"exec_airflow",
	default_args = default_args,
	description="exec_airflow",
	schedule_interval=timedelta(minutes=60),
	start_date=days_ago(0),
	tags=["test_pod"]
) as dag:
	tt = BashOperator(
		task_id = "dummy",
		bash_command = "echo TESTDUMMY"
	)

	print("FINISHED BASH COMMAND")

	t1 = KubernetesPodOperator(
		namespace = "default",
		pod_template_file = "./pod_test.yaml",
		labels = {"foo":"bar"},
		name = "task-1-hdep",
		is_delete_operator_pod = True,
		in_cluster = True,
		task_id = "task-1-hdep",
		config_file = os.path.expanduser("~") + "/.kube.config",
		get_logs = True

	)

	print("FINISHED CREATING TASK 1 POD TEST")

	tt >> t1
print("FINISHED CREATING DAG")
