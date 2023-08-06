from textwrap import dedent

import yaml


def create_seldon_deployment_manifest(
    image,
    deployment_name="app",
    predictor_name="default",
    spec_name="classifier",
    container_name="classifier",
    gateway_name=None,
    namespace="seldon",
    replicas=1,
):
    manifest = yaml.safe_load(
        dedent(
            f"""
        apiVersion: machinelearning.seldon.io/v1
        kind: SeldonDeployment
        metadata:
          name: {deployment_name}
          namespace: {namespace}
        spec:
          name: {spec_name}
          protocol: seldon
          predictors:
            - name: {predictor_name}
              graph:
                name: classifier
              componentSpecs:
                - spec:
                    containers:
                      - image: {image}
                        name: {container_name}
                        resources:
                          limits:
                            nvidia.com/gpu: 1
                        livenessProbe:
                          failureThreshold: 3
                          initialDelaySeconds: 60
                          periodSeconds: 5
                          successThreshold: 1
                          httpGet:
                            path: /health/status
                            port: http
                            scheme: HTTP
                          timeoutSeconds: 1
                        readinessProbe:
                          failureThreshold: 3
                          initialDelaySeconds: 20
                          periodSeconds: 5
                          successThreshold: 1
                          httpGet:
                              path: /health/status
                              port: http
                          timeoutSeconds: 1
              replicas: {replicas}
    """
        )
    )

    if gateway_name is not None:
        manifest["spec"].get("annotations", {})[
            "seldon.io/istio-gateway"
        ] = gateway_name

    return manifest
