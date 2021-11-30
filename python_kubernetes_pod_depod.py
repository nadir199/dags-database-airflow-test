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
	"python_kubernetes_pod_depod",
	default_args = default_args,
	description="python_kubernetes_pod_depod",
	schedule_interval=timedelta(minutes=60),
	start_date=days_ago(0),
	tags=["test_pod"]
) as dag:
	t1 = KubernetesPodOperator(
		namespace = "default",
		pod_template_file="pod_test.yaml",
		labels =  {"foo":"bar"},
		name = "task-depod",
		is_delete_operator_pod = True,
		in_cluster = True,
		task_id = "task-depod",
		config_file=os.path.expanduser("~") + "/.kube.config",
		get_logs = True
	)

	t2 = KubernetesPodOperator(
		namespace = "default",
		image = "python:3.7",
		image_pull_policy = "Always",
		cmds = ["python", "-c", "print('DEUXIEME TASK ..................')"],
		labels =  {"foo":"bar"},
		name = "task-2-hdep",
		is_delete_operator_pod = True,
		in_cluster = True,
		task_id = "task-2-hdep",
		config_file=os.path.expanduser("~") + "/.kube.config",
		get_logs = True
	)

	t1 >> t2