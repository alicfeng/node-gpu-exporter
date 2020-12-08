# node-gpu-exporter

## 概览

基于 `Python` 编写开发的一款专注于采集显卡资源数据的  `prometheus`  自定义采集器，基于节点颗粒度收集并汇报，即 `node-gpu-exporter`。



## prom结构

```
graphics{index="0",arg="utilization.gpu",model="GeForce GTX 1660 Ti"} 0
graphics{index="0",arg="utilization.memory",model="GeForce GTX 1660 Ti"} 0
graphics{index="0",arg="memory.total",model="GeForce GTX 1660 Ti"} 5944.25
graphics{index="0",arg="memory.free",model="GeForce GTX 1660 Ti"} 5944.1875
graphics{index="0",arg="memory.used",model="GeForce GTX 1660 Ti"} 0.0625
```



## 镜像

```shell
docker pull alicfeng/node-gpu-exporter:1.0.0
```



## 配置

#### 轮训采集周期

通过环境变量 `PLUGIN_PROM_INTERVAL` 控制，默认周期为 `5s`

#### 采集写入文件

写入容器 ` /etc/nvidia.prom` 文件位置





