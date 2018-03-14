from time import sleep

import requests

import subprocess

from ansible.module_utils.basic import AnsibleModule

SERVER_EXECUTABLE_LOCATION_PARAMETER_NAME = "executable"
SERVER_CONFIGURATION_LOCATION_PARAMETER_NAME = "config"
SERVER_HOST_PARAMETER_NAME = "host"
SERVER_PORT_PARAMETER_NAME = "port"

_SUPERGIANT_CONFIG_FILE_LONG_PARAMETER_NAME = "--config-file"
_SUPERGIANT_STARTED_INDICATOR = "Writing log to "
_SUPERGIANT_FAILED_INDICATOR = "panic"
_SUPERGIANT_TEXT_ENCODING = "utf-8"


def main():
    module = AnsibleModule({
        SERVER_EXECUTABLE_LOCATION_PARAMETER_NAME: dict(required=True, type="str"),
        SERVER_CONFIGURATION_LOCATION_PARAMETER_NAME: dict(required=True, type="str"),
        SERVER_HOST_PARAMETER_NAME: dict(required=True, type="str"),
        SERVER_PORT_PARAMETER_NAME: dict(required=True, type="int")
    }, supports_check_mode=False)

    start_supergiant(module.params.get(SERVER_EXECUTABLE_LOCATION_PARAMETER_NAME),
                     module.params.get(SERVER_CONFIGURATION_LOCATION_PARAMETER_NAME))


    test_ui("http://%s:%s/ui" % (module.params.get(SERVER_HOST_PARAMETER_NAME),
                                 module.params.get(SERVER_PORT_PARAMETER_NAME)), module)
    # TODO: Add more tests

    module.exit_json(changed=False, msg="All tests passed")


def test_ui(url, module):
    response = requests.get(url)
    if response.status_code != 200:
        module.fail_json(msg="UI test failed - incorrect status code: %s" % response.status_code)


def start_supergiant(executable_location, config_location):
    arguments = [executable_location, _SUPERGIANT_CONFIG_FILE_LONG_PARAMETER_NAME, config_location]
    process = subprocess.Popen(arguments, stderr=subprocess.PIPE, stdout=subprocess.PIPE)

    # FIXME
    # Thread(target=detect_panic, args=process.stderr).start()

    started = False
    while not started:
        line = process.stdout.readline().decode(_SUPERGIANT_TEXT_ENCODING).strip()
        if _SUPERGIANT_STARTED_INDICATOR in line:
            started = True
            # Grace time
            sleep(1)

    return process


def detect_panic(stderr, module):
    while True:
        line = stderr.readline().decode(_SUPERGIANT_TEXT_ENCODING).strip()
        if _SUPERGIANT_FAILED_INDICATOR in line:
            module.fail_json(msg=line)


if __name__ == "__main__":
    main()
