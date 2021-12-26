from robusta.api import *
import time


class OOMKillParams(BaseModel):
    sleep_time_before_oom: float = 120
    megabytes: int = 129
    sleep_time_before_deletion: float = 300


@action
def generate_oom_kill(event: ExecutionBaseEvent, params: OOMKillParams):
    logging.info("starting oom kill")
    dep = RobustaDeployment.from_image(
        "stress-test2",
        "jfusterm/stress",
        ["sh", "-c", f"sleep {params.sleep_time_before_oom}"],
    )
    dep.spec.template.spec.containers[0].resources = ResourceRequirements(
        limits={"memory": f"{params.megabytes-1}"}
    )
    dep: RobustaDeployment = dep.createNamespacedDeployment(dep.metadata.namespace).obj
    time.sleep(params.sleep_time_before_deletion)
    logging.info("stopping oom kill")
    RobustaDeployment.deleteNamespacedDeployment(
        dep.metadata.name, dep.metadata.namespace
    )
    logging.info("done")

