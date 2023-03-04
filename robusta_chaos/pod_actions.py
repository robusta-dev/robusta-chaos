import logging

from kubernetes import client
from kubernetes.client import V1Pod, V1PodList

from robusta.api import (
    ExecutionBaseEvent,
    RateLimiter,
    RateLimitParams,
    RobustaPod,
    action,
)


class RunInPodParams(RateLimitParams):
    pod_label_selector: str
    command: str


@action
def run_command_in_pod(event: ExecutionBaseEvent, params: RunInPodParams):
    """
    Run a command on a target pod
    """
    if not RateLimiter.mark_and_test(
        "run_command_in_pod", f"{params.pod_label_selector}{params.command}", params.rate_limit
    ):
        logging.info(f"Skipping run_command_in_pod for {params.pod_label_selector} {params.command}. Rate limited")
        return

    pods: V1PodList = client.CoreV1Api().list_pod_for_all_namespaces(label_selector=params.pod_label_selector)
    if not pods.items:
        logging.info(f"run_in_pod: No pods matching label selector {params.pod_label_selector}")
        return

    target_pod: V1Pod = pods.items[0]
    pod = RobustaPod.readNamespacedPod(target_pod.metadata.name, target_pod.metadata.namespace).obj
    if not pod:
        logging.info(
            f"run_in_pod: Could not find target pod: {target_pod.metadata.name}/{target_pod.metadata.namespace}"
        )
        return

    exec_result = pod.exec(params.command)
    logging.info(f"run_in_pod: exec result: {exec_result}")
