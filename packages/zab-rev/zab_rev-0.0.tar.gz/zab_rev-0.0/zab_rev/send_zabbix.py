import os


class Zabbix:
    def __init__(self, kwargs: dict) -> None:
        self.zabbix_server = kwargs["zabbix_server"]
        self.node = kwargs["node"]
        self.key = kwargs["key"]
        self.value = kwargs["value"]
        if kwargs.get("zabbix_port"):
            self.zabbix_port = kwargs["zabbix_port"]
        else:
            self.zabbix_port = 10051

    def send_report(self) -> bool:
        try:
            zabbix_send_command = f"""zabbix_sender -z {self.zabbix_server} -p 10051 -s {self.node} \
                -k {self.key}  -o {self.value}"""
            os.system(zabbix_send_command)
            return True
        except Exception:
            return False


if __name__ == "__main__":
    pass
