from pydantic import BaseModel, parse_obj_as
import logging
from typing import Any
from deepmerge import always_merger


logger = logging.getLogger(__name__)

# operations:
#   deploy:
#     configurations:
#       hcloud-flannel:
#         title: "hcloud k8s; flannel cni"
#         name: hcloud-flannel
#         modules: [pki, dns-zone, nodes, inventory, kubernetes, cluster-secret, hcloud-ccm]

class Configuration(BaseModel):
    title: str
    name: str
    modules: list[str]

class Operation(BaseModel):
    configurations: dict[str, Configuration] = {}