from time import sleep

import requests
from airflow.exceptions import AirflowException
from airflow.models import BaseOperator, Variable
from airflow.plugins_manager import AirflowPlugin
from airflow.utils.decorators import apply_defaults

env = Variable.get("env")
s3_bucket_name = Variable.get("papermill_s3_bucket_name", "sktai-notebooks")
notebook_path = "{{dag.dag_id}}/{{task.task_id}}/{{run_id}}/{{ti.try_number}}.ipynb"
output_nb = f"s3://{s3_bucket_name}/papermill/{env}/{notebook_path}"
commuter_url = Variable.get(
    "commuter_url", "https://commuter-d4anno4aha-an.a.run.app/view"
)
output_nb_url = f"{commuter_url}/papermill/{env}/{notebook_path}"


class NesOperator(BaseOperator):
    template_fields = ("input_nb", "output_nb", "parameters")

    @apply_defaults
    def __init__(
        self,
        input_nb: str,
        output_nb: str = output_nb,
        output_nb_url: str = output_nb_url,
        parameters: dict = None,
        runtime: str = None,
        profile: str = None,
        host_network: bool = None,
        poll_interval: int = 60,
        *args,
        **kwargs,
    ) -> None:
        super().__init__(*args, **kwargs)
        self.input_nb = input_nb
        self.output_nb = output_nb
        self.parameters = parameters or {}
        self.output_nb_url = output_nb_url
        self.run_id = None
        self.runtime = runtime
        self.profile = profile
        self.host_network = host_network

        self.nes = "http://nes.sktai.io/v1/runs"
        self.poll_interval = poll_interval
        self.proxy = Variable.get("proxy") if env == "prd" else None

    def get_status(self, id):
        res = requests.get(f"{self.nes}/{id}")
        res.raise_for_status()
        status = res.json()["status"]
        return status

    def execute(self, context):
        data = {"input_url": self.input_nb, "parameters": self.parameters}
        if self.runtime:
            data["runtime"] = self.runtime

        if self.profile:
            data["profile"] = self.profile

        if self.host_network is not None:
            data["host_network"] = self.host_network

        res = requests.post(self.nes, json=data)
        print(f"Job submitted with: {data}")
        res.raise_for_status()

        r = res.json()
        id, output = r["id"], r["output_url"]
        self.run_id = id
        print(
            f"""--------------------------------------------------------------------------------\n\n{output}\n\n--------------------------------------------------------------------------------"""
        )

        while (status := self.get_status(id)) != "Succeeded":
            if status in ["Failed", "Error"]:
                raise AirflowException(f'Job {id} exited with "{status}"')
            else:
                print(f'Polling job status... current status: "{status}"')
                sleep(self.poll_interval)

        print(f'Job {id} successfully finished with "{status}"')
        return True

    def on_kill(self):
        while True:
            res = requests.delete(f"{self.nes}/{self.run_id}")
            if res.status_code == 404:
                break
            status = res.json()["status"]
            print(f'Deleting job... current status: "{status}"')
            sleep(self.poll_interval)


class NesPlugin(AirflowPlugin):
    name = "nes_plugin"
    operators = [NesOperator]
    sensors = []
    hooks = []
    executors = []
    macros = []
    admin_views = []
    flask_blueprints = []
    menu_links = []
    appbuilder_views = []
    appbuilder_menu_items = []
    global_operator_extra_links = []
    operator_extra_links = []
