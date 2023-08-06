from textwrap import dedent

import yaml


def create_default_istio_gateway_manifest():
    manifest = yaml.safe_load(
        dedent(
            f"""
        apiVersion: networking.istio.io/v1alpha3
        kind: Gateway
        metadata:
          name: seldon-gateway
          namespace: istio-system
        spec:
          selector:
            istio: ingressgateway # use istio default controller
          servers:
          - port:
              number: 80
              name: http
              protocol: HTTP
            hosts:
            - "*"
    """
        )
    )

    return manifest
