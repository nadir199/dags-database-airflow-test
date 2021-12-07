from datetime import timedelta

from airflow import DAG

from airflow.utils.dates import days_ago
from airflow.operators.bash import BashOperator

from airflow.providers.cncf.kubernetes.operators.kubernetes_pod import KubernetesPodOperator
import os

default_args = {
	"owner" : "airflow",
	"depends_on_past" : True,
	"email" : ["airflow@example.com"],
	"email_on_failure" : False,
	"email_on_retry" : False,
	"retries" : 1,
	"retry_delay" : timedelta(minutes = 5),
}

with DAG(
	"merge_job_spark",
	default_args = default_args,
	description="merge_job_spark",
	schedule_interval=timedelta(minutes=60),
	start_date=days_ago(0),
	tags=["test_pod"]
) as dag:
	tt = BashOperator(
		task_id = "dummy",
		bash_command = "echo TESTPREMERGE"
	)

	print("FINISHED BASH COMMAND")

	t1 = KubernetesPodOperator(
		namespace = "default",
		pod_template_file = "/opt/airflow/dags/repo/pod_job_merge.yaml",
		labels = {"foo":"bar"},
		name = "merging_task",
		is_delete_operator_pod = True,
		in_cluster = True,
		task_id = "merging_task",
		config_file = os.path.expanduser("~") + "/.kube.config",
		get_logs = True

	)

	print("FINISHED MERGE POD TEST")

	tt >> t1
print("FINISHED CREATING DAG")
