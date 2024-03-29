import logging
import time
import datetime

from robusta.api import (
    ExecutionBaseEvent,
    RobustaDeployment,
    action,
    ActionParams,
    RateLimitParams,
    PrometheusKubernetesAlert,
    RateLimiter,
)


class DeploymentParams(RateLimitParams):
    """
    :var name: name of deployment that needs to restart.
    :var namespace: namespace of deployment that needs restart.
    """

    name: str
    namespace: str


@action
def restart_deployment_pods(alert: PrometheusKubernetesAlert, params: DeploymentParams):
    """
    Restart given deployment based on prometheus alert condition with defined rate limiting.
    """
    if not RateLimiter.mark_and_test("deployment_restart", params.name + params.namespace, params.rate_limit):
        logging.info(f"Skipping deployment restart for {params.name} {params.namespace}. Rate limited")
        return

    now = datetime.datetime.utcnow()
    now = str(now.isoformat("T") + "Z")
    my_deployment: RobustaDeployment = RobustaDeployment.readNamespacedDeployment(params.name, params.namespace).obj

    if not my_deployment:
        logging.error(f"Restart Deployment: Deployment not found: {alert}")
        return

    my_deployment.spec.template.metadata.annotations["kubectl.kubernetes.io/restartedAt"] = now
    my_deployment.update()

class ScaleDeploymentParams(ActionParams):
    name: str
    namespace: str
    replicas: int

@action
def scale_deployment(event: ExecutionBaseEvent, params: ScaleDeploymentParams):
    """
    Scale the specified deployment up and down to the specified number of replicas.
    Typically used with a scheduled trigger
    """
    deployment: RobustaDeployment = RobustaDeployment.readNamespacedDeployment(params.name, params.namespace).obj
    if deployment.spec.replicas == params.replicas:
        deployment.spec.replicas = 0
    else:
        deployment.spec.replicas = params.replicas
    deployment.update()
    logging.info(f"Scaled deployment {params.namespace}/{params.name} to {deployment.spec.replicas}")