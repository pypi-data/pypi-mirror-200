
from urllib.parse import urlparse
from pydantic import BaseModel
from deepmerge import always_merger
from copy import deepcopy
import logging, os
from typing import Any

logger = logging.getLogger(__name__)



class Module(BaseModel):
    name: str | None = None
    source: str | None = None
    src: str | None = None
    vars: dict[str, Any] = {}
    built_vars: dict[str, Any] = {}
    providers: list[str] = []    
    tf_state_key: str | None = None
    tf_state_bucket: str | None = None
    tf_state_bucket_region: str | None = None
    tf_backend: str | None = None
    

    def __str__(self) -> str:
        return f"<{self.__class__.__name__}:{self.name}>"

    def __init__(self, **data: Any) -> None:
        super().__init__(**data)
        if self.source:
            self.src = self.source
            logger.warn(f"{self} source is deprecated, use src instead")

    @property
    def abssrc(self) -> str:
        from stackdiac.stackd import sd
        return os.path.join(sd.root, self.src)


    @property
    def charts_root(self) -> str:
        from stackdiac.stackd import sd
        return os.path.join(sd.root, "charts")

    def get_template(self, template_name):
        from stackdiac.stackd import sd
        return sd.conf.repos["core"].get_jinja_env().get_template(template_name)

    def write(self, template_name, dest, **kwargs):
        tpl = self.get_template(template_name)
        
        with open(dest, "w") as f:
            f.write(tpl.render(**kwargs))

        logger.debug(f"{self} writed {dest} from {tpl}")

    @property
    def remote_state_template(self) -> str:
        return f"remote_state.s3.hcl.j2"

    
    def get_namespace(self, stack) -> str:
        return f"{stack.name}-{self.name}"

    

    def get_prefix(self, stack) -> str:
        return f"{stack.name}"

    
    def get_ingress_host(self, cluster, stack) -> str:
        from stackdiac.stackd import sd
        return f"{stack.name}.{cluster.name}.{sd.dns_zone}"

    def build_vars(self, cluster, cluster_stack, stack, **kwargs):
        return dict(
            prefix=self.get_prefix(stack),
            cluster_name=cluster.name,
            cluster=cluster.name,
            env=cluster.name,
            service=self.name,
            tg_abspath=self.abssrc,
            group="all", # legacy
            environment=cluster.name,
            ingress_host=self.get_ingress_host(cluster, stack),
            namespace=self.get_namespace(stack),
            tf_state_key=self.tf_state_key or f"{cluster.name}/{self.get_namespace(stack)}",
            charts_root=self.charts_root,
        )

    @property
    def tg_module_src(self):
        """
            adding // before last path component to avoid terragrunt to download the module 
        """
        return f"{os.path.dirname(self.abssrc)}//{os.path.basename(self.abssrc)}"

    def build(self, cluster, cluster_stack, stack, **kwargs):
        from stackdiac.stackd import sd
        path = sd.resolve_module_path(self.src)
        dest = os.path.join(sd.root, "build", cluster.name,
            stack.name, self.name)
        os.makedirs(dest, exist_ok=True)
        _vars = {}
        varSources = [
            self.build_vars(cluster, cluster_stack, stack, **kwargs),
            sd.conf.vars,
            cluster.vars,
            cluster_stack.vars,
            self.vars
        ]
        for v in varSources:
            always_merger.merge(_vars, deepcopy(v))       
        self.built_vars = deepcopy(_vars)
        ctx = dict(module=self, cluster=cluster, stackd=sd, vars=_vars, **kwargs)
        self.write("terragrunt.root.j2", os.path.join(dest, "terragrunt.hcl"), **ctx)        
        self.write("variables.tf.j2", os.path.join(dest, "_variables.tf"), **ctx)
        
        versions = [ v for v in sd.providers.values() if v.name in self.providers ] # if sd.provider name matches module providers
        self.write("versions.tf.j2", os.path.join(dest, "_versions.tf"), **dict(versions=versions, **ctx))

        self.write("vars.tfvars.json.j2", os.path.join(dest, "vars.tfvars.json"), **dict(versions=versions, **ctx))

        logger.debug(f"{self} building module {self.name} in {stack.name} from {path}")

         


class Stack(BaseModel):
    name: str | None = None
    src: str | None = None
    example_vars: dict[str, Any] = {}  
    modules: dict[str, Module]
    vars: dict[str, Any] = {}

    class Config:
        orm_mode = True
        exclude = {'cluster'}
   

    def __init__(self, **data: Any) -> None:
        super().__init__(**data)
       
        
        for module_name, module in self.modules.items():
            module.name = module_name
        

    def __str__(self) -> str:
        return f"<{self.__class__.__name__}:{self.name}>"


    def build(self, **kwargs):
        for module in self.modules.values():
            module.build(stack=self, **kwargs)