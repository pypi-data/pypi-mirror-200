import yaml


def build_client_config(server, ca_cert_b64encoded, token):
    config_dict = {
        "apiVersion": "v1",
        "clusters": [
            {
                "cluster": {
                    "certificate-authority-data": ca_cert_b64encoded,
                    "server": server
                },
                "name": "default"
            }
        ],
        "contexts": [
            {
                "context": {
                    "cluster": "default",
                    "user": "sa-user"
                },
                "name": "default"
            }
        ],
        "current-context": "default",
        "kind": "Config",
        "preferences": {},
        "users": [
            {
                "name": "sa-user",
                "user": {
                    "token": token
                }
            }
        ]
    }
    return yaml.dump(config_dict, default_flow_style=False)
