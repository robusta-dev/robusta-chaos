from robusta.api import *


@action
def kill_node(event: NodeEvent):
    node = event.get_node()
    if node is None:
        logging.error(f"cannot kill node without node details. event={event}")
        return

    result = RobustaPod.exec_on_node(
        "node-killer", node.metadata.name, "systemctl stop kubelet"
    )
    logging.warning(f"result from killing node is {result}")
