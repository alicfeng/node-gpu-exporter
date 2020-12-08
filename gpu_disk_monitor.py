# -*- coding: utf-8 -*-
import pynvml
import psutil
import time
import os

while True:
    time.sleep(int(os.getenv("PLUGIN_PROM_INTERVAL", 5)))
    try:
        # nvml初始化
        pynvml.nvmlInit()
        # 通过驱动获取GPU个数
        DeviceCount = pynvml.nvmlDeviceGetCount()
        GpuData = ""
        for i in range(DeviceCount):
            #  获取GPU信息
            GpuDevice = pynvml.nvmlDeviceGetHandleByIndex(i)
            # 获取根据序号获取GPU的总使用率
            Utilization = pynvml.nvmlDeviceGetUtilizationRates(GpuDevice)
            # 获取根据序号获取GPU的内存情况
            GpuMemInfo = pynvml.nvmlDeviceGetMemoryInfo(GpuDevice)
            # 获取GPU名称
            GpuModel = pynvml.nvmlDeviceGetName(GpuDevice)
            GpuInfo = {"utilization.gpu": Utilization.gpu, "utilization.memory": Utilization.memory,
                       "memory.total": GpuMemInfo.total / 1024 ** 2, "memory.free": GpuMemInfo.free / 1024 ** 2,
                       "memory.used": GpuMemInfo.used / 1024 ** 2}
            # 定义prometheus的数据格式
            temp = '{name}{{index="{index}",arg="{lable}",model="{model}"}} {value}\n'
            for k, v in GpuInfo.items():
                values = {"name": "graphics", "index": i, "lable": k, "value": v, "model": GpuModel.decode("utf-8")}
                GpuData = GpuData + temp.format(**values)

        with open('/etc/nvidia.prom', 'w') as f:
            f.write(GpuData)
            f.close()
        pynvml.nvmlShutdown()
    except Exception as nvmllib:
        print("nvmllibError %s" % nvmllib)
    finally:
        DiskInfo = psutil.disk_usage("/")
        DiskName = psutil.disk_partitions("/")[1][0]
        DiskData = {"total": DiskInfo.total / 1024, "used": DiskInfo.used / 1024, "avail": DiskInfo.free / 1024}
        temp = '{name}{{device="{device}"}} {value}\n'
        with open('/etc/disk.prom', 'w') as f:
            for DiskDataKey, DiskDataValue in DiskData.items():
                values = {"name": "disk_" + DiskDataKey + "_bytes", "device": DiskName, "value": DiskDataValue}
                f.write(temp.format(**values))
            f.close()
