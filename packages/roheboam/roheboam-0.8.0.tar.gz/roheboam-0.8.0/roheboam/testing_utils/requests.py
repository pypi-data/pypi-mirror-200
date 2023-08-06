import time

import requests

from ..engine.utils.convenience import run_shell_command


def post_request_on_url_with_retry_until_success(
    url, data, attempts=10, per_try_timeout=5, completion_handler=lambda: None
):
    completed_successfully = False
    try:
        for attempt in range(attempts):
            try:
                response = requests.post(
                    url,
                    data=data,
                    headers={"Content-Type": "application/json"},
                )
                if response.status_code != 200:
                    raise Exception(
                        f"Response status code: {response.status_code}\nResponse text: {response.text}"
                    )
                assert response.status_code == 200
                print(f"Success on attempt: {attempt + 1}")
                completed_successfully = True
                break
            except Exception as e:
                print(f"Failure on attempt: {attempt + 1}")
                print(e)
                time.sleep(per_try_timeout)
    finally:
        completion_handler()
        return completed_successfully


def stop_container_completion_handler(container, silent=True):
    try:
        if not silent:
            print(container.logs().decode())
        container.stop()
    except Exception as e:
        print(e)


def stop_k8s_pods_completion_handler(
    deployment_manifest_save_path, gateway_manifest_save_path
):
    try:
        run_shell_command(f"microk8s kubectl delete -f {deployment_manifest_save_path}")
        run_shell_command(f"microk8s kubectl delete -f {gateway_manifest_save_path}")
    except Exception as e:
        print(e)
