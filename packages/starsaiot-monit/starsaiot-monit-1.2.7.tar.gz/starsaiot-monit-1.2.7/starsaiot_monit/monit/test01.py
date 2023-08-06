import os
import uuid


def get_eth():
    eth_list = []
    os.system("ls -l /sys/class/net/ | grep -v virtual | sed '1d' | awk 'BEGIN {FS=\"/\"} {print $NF}' > eth.yaml")
    try:
        with open('./eth.yaml', "r") as f:
            for line in f.readlines():
                line = line.strip()
                eth_list.append(line.lower())
    except Exception as e:
        print(e)
        eth_list = []

    return eth_list

if __name__ == '__main__':
    print(uuid.uuid1())
    telemetry_report_datas = []
    telemetry_report_datas.append("1")
    telemetry_report_datas.append("2")
    telemetry_report_datas.append("3")
    telemetry_report_datas.append("4")
    telemetry_report_datas.append("5")
    telemetry_report_datas.append("6")
    print(telemetry_report_datas)

    telemetry_report_datas1 = []

    status = 0
    for trdata in telemetry_report_datas:
        if status == 0:
            # telemetry_report_datas.remove(trdata)
            status = 0
        else:
            telemetry_report_datas1.append(trdata)
            status = 0
    print(telemetry_report_datas)
    print(telemetry_report_datas1)
    telemetry_report_datas = telemetry_report_datas1
    print(len(telemetry_report_datas) == 0)