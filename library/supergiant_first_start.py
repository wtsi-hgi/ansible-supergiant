import subprocess

from ansible.module_utils.basic import AnsibleModule

SERVER_EXECUTABLE_LOCATION_PARAMETER_NAME = "executable"
SERVER_CONFIGURATION_LOCATION_PARAMETER_NAME = "config"

_SUPERGIANT_CONFIG_FILE_LONG_PARAMETER_NAME = "--config-file"
_SUPERGIANT_CREDENTIALS_LINE_PREFIX = "( \xCD\xA1\xC2\xB0\x20\xCD\x9C\xCA\x96\x20\xCD\xA1\xC2\xB0)"
_SUPERGIANT_TEXT_ENCODING = "utf-8"


def main():
    module = AnsibleModule({
        SERVER_EXECUTABLE_LOCATION_PARAMETER_NAME: dict(required=True, type="str"),
        SERVER_CONFIGURATION_LOCATION_PARAMETER_NAME: dict(required=True, type="str")
    }, supports_check_mode=False)


    # TODO: Check locations?

    arguments = [module.params.get(SERVER_EXECUTABLE_LOCATION_PARAMETER_NAME),
                 _SUPERGIANT_CONFIG_FILE_LONG_PARAMETER_NAME,
                 module.params.get(SERVER_CONFIGURATION_LOCATION_PARAMETER_NAME)]
    process = subprocess.Popen(arguments, stderr=subprocess.PIPE)
    while True:
        # TODO: Detect first start

        line = process.stderr.readline().decode(_SUPERGIANT_TEXT_ENCODING).strip()
        if _SUPERGIANT_CREDENTIALS_LINE_PREFIX in line:
            raise Exception(line)


if __name__ == "__main__":
    main()
