from datetime import timedelta

from airflow import DAG

from airflow.utils.dates import days_ago
from airflow.operators.bash import BashOperator

from airflow.providers.cncf.kubernetes.operators.kubernetes_pod import KubernetesPodOperator
import os

print("STARTING DAG POD DEPOD CREATION")

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
	t1 = BashOperator(
		task_id = "first-pod-test",
		bash_command = "kubectl apply -f pod_test.yaml"
	)
	
	print("FINISHED CREATING TASK 1 KUBECTL APPLY")

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

	print("FINISHED CREATING TASK 2")
	t1 >> t2
print("FINISHED CREATING DAG")
