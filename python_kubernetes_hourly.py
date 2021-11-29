from datetime import timedelta

from airflow import DAG

from airflow.utils.dates import days_ago

from airflow.providers.cncf.kubernetes.operators.kubernetes_pod import KubernetesPodOperator
import os

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
	"python_kubernetes_workflow_hourly",
	default_args = default_args,
	description="python_kubernetes_workflow_hourly",
	schedule_interval=timedelta(minutes=60),
	start_date=days_ago(0),
	tags=["python_kubernetes_workflow_hourly"]
) as dag:
	t1 = KubernetesPodOperator(
		namespace = "default",
		image = "python:3.7",
		image_pull_policy = "Never",
		cmds = ["python", "-c", "print('Hello task 1 ..................')"],
		labels =  {"foo":"bar"},
		name = "task-1-h",
		is_delete_operator_pod = True,
		in_cluster = True,
		task_id = "task-1-h",
		config_file=os.path.expanduser("~") + "/.kube.config",
		get_logs = True
	)

	t2 = KubernetesPodOperator(
		namespace = "default",
		image = "python:3.7",
		image_pull_policy = "Never",
		cmds = ["python", "-c", "print('Hello task 2 ..................')"],
		labels =  {"foo":"bar"},
		name = "task-2-h",
		is_delete_operator_pod = True,
		in_cluster = True,
		task_id = "task-2-h",
		config_file=os.path.expanduser("~") + "/.kube.config",
		get_logs = True
	)

	t1 >> t2
