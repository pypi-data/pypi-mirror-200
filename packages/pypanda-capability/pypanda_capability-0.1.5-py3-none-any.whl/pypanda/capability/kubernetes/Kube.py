import base64
import os
import tempfile

import urllib3
import yaml
from kubernetes import client, config
from kubernetes.client import ApiException
from urllib3.exceptions import InsecureRequestWarning

urllib3.util.ssl_.DEFAULT_CIPHERS = 'ALL:@SECLEVEL=1'
urllib3.disable_warnings(InsecureRequestWarning)

urllib3.util.ssl_.DEFAULT_CIPHERS = 'ALL:@SECLEVEL=1'


class KubeClient:
    def __init__(self, configuration):
        self.configuration = configuration

    @classmethod
    def init_from_cli_config(cls):
        config.load_kube_config()
        return KubeClient(configuration=client.Configuration.get_default_copy())

    @classmethod
    def init_from_config_stream(cls, config_stream):
        config.load_kube_config_from_dict(config_dict=yaml.safe_load(config_stream))
        return KubeClient(configuration=client.Configuration.get_default_copy())

    @classmethod
    def init_from_token(cls, account_token, server, ca_base64_str):
        configuration = client.Configuration()
        configuration.api_key["authorization"] = account_token
        configuration.api_key_prefix['authorization'] = 'Bearer'
        configuration.host = server
        ca_fd, ca_path = tempfile.mkstemp(text=True)
        os.write(ca_fd, base64.b64decode(ca_base64_str))
        os.close(ca_fd)
        configuration.ssl_ca_cert = ca_path
        return KubeClient(configuration)

    @staticmethod
    def client_wrapper(func):
        def wrapper(self, *args, **kwargs):
            with client.ApiClient(self.configuration) as api_client:
                try:
                    return func(self, api_client=api_client, *args, **kwargs)
                except ApiException as err:
                    import traceback
                    err = traceback.format_exc()
                    print(err)

        return wrapper

    @property
    def cluster_admin_role(self):
        return {
            "apiGroup": "rbac.authorization.k8s.io",
            "kind": "ClusterRole",
            "name": "cluster-admin"
        }

    @client_wrapper
    def list_namespaces(self, api_client=None):
        api_core = client.CoreV1Api(api_client=api_client)
        ns = api_core.list_namespace().items
        return ns

    @client_wrapper
    def get_namespace(self, name, api_client=None):
        api_core = client.CoreV1Api(api_client=api_client)
        ns = api_core.list_namespace(field_selector=f'metadata.name={name}').items
        if len(ns) == 1:
            return ns[0]
        else:
            return None

    @client_wrapper
    def create_namespace(self, name, annotations, api_client=None):
        api_core = client.CoreV1Api(api_client=api_client)
        namespace = client.V1Namespace(
            metadata={"name": name, "annotations": annotations}
        )
        api_response = api_core.create_namespace(namespace)
        return api_response

    @client_wrapper
    def create_service_account(self, name, namespace, annotations, api_client=None):
        api_core = client.CoreV1Api(api_client=api_client)
        sa_body = client.V1ServiceAccount(
            metadata={"name": name, "annotations": annotations})
        sa = api_core.create_namespaced_service_account(namespace, sa_body)
        return sa

    @client_wrapper
    def get_service_account(self, name, namespace, api_client=None):
        api_core = client.CoreV1Api(api_client=api_client)
        sa = api_core.list_namespaced_service_account(namespace=namespace, field_selector=f'metadata.name={name}').items
        if len(sa) == 1:
            return sa[0]
        else:
            return None

    @client_wrapper
    def ping(self, api_client=None):
        try:
            api_core = client.CoreV1Api(api_client=api_client)
            res = api_core.get_api_resources()
            return res is not None
        except Exception:
            import traceback
            traceback.print_exc()
            return False

    @client_wrapper
    def bind_sa_as_cluster_admin(self, name, sa_namespace, sa_name, annotations, api_client=None):
        rbac_client = client.RbacAuthorizationV1Api(api_client=api_client)
        cluster_role_binding = client.V1ClusterRoleBinding(
            metadata={"name": name, "annotations": annotations},
            role_ref=self.cluster_admin_role,
            subjects=[{"kind": "ServiceAccount", "namespace": sa_namespace, "name": sa_name}]
        )
        role_binding = rbac_client.create_cluster_role_binding(cluster_role_binding)
        return role_binding

    @client_wrapper
    def get_secret(self, namespace, name, api_client=None):
        api_core = client.CoreV1Api(api_client=api_client)
        secrets = api_core.list_namespaced_secret(namespace=namespace, field_selector=f'metadata.name={name}').items
        if len(secrets) == 1:
            return secrets[0]
        else:
            return None

    @client_wrapper
    def delete_secret(self, namespace, name, api_client=None):
        api_core = client.CoreV1Api(api_client=api_client)
        api_core.delete_namespaced_secret(name, namespace)

    @client_wrapper
    def create_secret(self, namespace, name, data: dict[str, str], secret_type, annotations=None, api_client=None):
        data_encrypted = {}
        for k, v in data.items():
            data_encrypted[k] = base64.b64encode(v.encode()).decode()
        api_core = client.CoreV1Api(api_client=api_client)
        metadata = client.V1ObjectMeta(
            name=name,
            namespace=namespace,
            annotations=annotations
        )
        body = client.V1Secret(
            metadata=metadata,
            data=data_encrypted,
            type=secret_type,
        )
        secrets = api_core.create_namespaced_secret(namespace, body)
        return secrets

    @client_wrapper
    def patch_service_account(self, namespace, sa_name, body, api_client=None):
        api_core = client.CoreV1Api(api_client=api_client)
        _ = api_core.patch_namespaced_service_account(
            sa_name, namespace, body
        )
        return _

    @client_wrapper
    def list_cluster_role_binding(self, api_client=None):
        api = client.RbacAuthorizationV1Api(api_client=api_client)
        binding_strs = api.list_cluster_role_binding()
        return binding_strs.items

    @client_wrapper
    def list_namespaced_role_binding(self, namespace, api_client=None):
        api = client.RbacAuthorizationV1Api(api_client=api_client)
        binding_strs = api.list_namespaced_role_binding(namespace)
        return binding_strs.items

    @client_wrapper
    def list_cluster_role(self, api_client=None):
        api = client.RbacAuthorizationV1Api(api_client=api_client)
        return api.list_cluster_role().items

    @client_wrapper
    def list_namespaced_role(self, namespace, api_client=None):
        api = client.RbacAuthorizationV1Api(api_client=api_client)
        return api.list_namespaced_role(namespace).items

    def append_image_pull_secrets_to_default_service_account(self, namespace, secrets):
        sa = self.get_service_account('default', namespace)
        if sa.image_pull_secrets is not None:
            current_image_pull_secrets = [x.name for x in sa.image_pull_secrets]
            patch_body = []
            for secret in secrets:
                if secret in current_image_pull_secrets:
                    continue
                else:
                    patch_body.append(
                        {"op": "add", "path": "/imagePullSecrets/-", "value": {"name": secret}}
                    )
        else:
            patch_body = [
                {"op": "add", "path": "/imagePullSecrets", "value": [{"name": x for x in secrets}]}
            ]
        __ = self.patch_service_account(namespace, 'default', patch_body)
        return __


def validation_config(cluster_info, encoded):
    return KubeClient(cluster_info, encoded).ping()
