from ...utils.convenience import run_shell_command


def get_istio_ingress_ip():
    return run_shell_command(
        "microk8s kubectl get po -l istio=ingressgateway -n istio-system -o jsonpath='{.items[0].status.hostIP}'",
        silent=True,
    )[0]


def get_istio_ingress_port():
    return run_shell_command(
        "microk8s kubectl -n istio-system get service istio-ingressgateway -o jsonpath='{.spec.ports[?(@.name==\"http2\")].nodePort'}",
        silent=True,
    )[0]
