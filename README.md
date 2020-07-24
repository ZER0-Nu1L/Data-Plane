# Data-Plane
Wedjat Eye's Date plane

## Topo Design
refer to:http://www.topology-zoo.org/dataset.html

| Network        | Type                        |
| -------------- | --------------------------- |
| Type           | COM                         |
| Geo Extent     | Region                      |
| Classification | Backbone, Customer, Transit |
| City           | Chengdu                     |

`data.geojson` - `data.gml` could preview by 'Geo Data Viewer' Extension in VSCode.

Web Test Demo: https://www.processon.com/view/link/5efffa7fe401fd3908b04d7e

## Usage
### Python
```shell
cd ./Data-Plane/
pip install -r requirements.txt
```
### Clone
```shell
git clone https://github.com/ZER0-Nu1L/Data-Plane.git
```

### Creat Topo
```shell
cd ./Data-Plane/Topo
sudo mn -c
sudo mn --custom topo_zoo.py --topo topo_zoo --mac --controller=remote,ip=127.0.0.1,port=6653
```
> p.s. 由于 `topo_zoo.py` 涉及到文件读写，所以 `sudo mn --custom ./Data-Plane/Topo/topo_zoo.py --topo topo_zoo  --arp --mac --controller=remote,ip=127.0.0.1,port=6653` 是不可以的，请完整地执行上面的三条命令。

### Server Folder
```shell
cd ./Data-Plane/Server
./create.sh num
```
其中 num 指定创建的文件夹数目；

### Web Server
./Data-Plane/CenterServer