docker run -v /home/ai/jazzy_ws:/docker-ros/ws -it --runtime=nvidia --name jazzy_container rwthika/ros2-torch bash
docker run -it --runtime=nvidia  --network host rwthika/ros2-torch bash

docker run -it --runtime=nvidia --network host jetson_image bash


sudo docker start ros2_humble_slam
sudo docker exec -it ros2_humble_slam /bin/bash

--env="DISPLAY=$DISPLAY" --volume="/tmp/.X11-unix:/tmp/.X11-unix"


### 启用图形界面
xhost +local:docker
docker exec -it \
  --env="DISPLAY=$(echo $DISPLAY)" \
  --volume="/tmp/.X11-unix:/tmp/.X11-unix" \
  <CONTAINER_ID> /bin/bash

* 例子：
xhost +local:docker
docker exec -it \
  --env="DISPLAY=$(echo $DISPLAY)" \
  --volume="/tmp/.X11-unix:/tmp/.X11-unix" \
  jazzy_container /bin/bash


### jetson yolo docker 命令
#### 查看容器名字
sudo docker ps -a
CONTAINER ID   IMAGE           COMMAND                  CREATED       STATUS         PORTS     NAMES
0cdfc3446265   yolo_ros:v1.0   "/tini -- /entrypoin…"   8 weeks ago   Up 8 seconds             yolo
#### 启动容器
sudo docker start yolo
#### 进入容器
sudo docker exec -it yolo /bin/bash
#### 复制文件到容器
sudo docker cp bus.jpg 4729ab41f810:/docker-ros/ws/src/yolo_test

#### 使用 docker commit 命令打包容器为镜像
sudo docker commit [选项] <容器ID或容器名称> <镜像名称:标签>
-m "message"：添加提交说明信息。
-a "author"：指定作者信息。 
示例：
sudo docker commit -m "ptz support" -a "ShaoXiang" yolo yolo_ros:v2

#### 创建云台容器
sudo docker run -it --runtime=nvidia --network host --privileged --device=/dev/ttyCH341USB0 --name ptz_ros yolo_ros:v2 /bin/bash
#### 进入云台容器
sudo docker exec -it ptz_ros /bin/bash
#### 开启云台容器
sudo docker start ptz_ros

#### 导出单个镜像
sudo docker save -o <文件路径> <镜像名称>:<标签>
sudo docker save -o yolo_ros_v2.tar yolo_ros:v2

#### 导入镜像到docker中
sudo docker load -i <镜像文件路径>
sudo docker load -i yolo_ros_v2.tar

#### 停止正在运行的容器（如果存在）
sudo docker stop ptz_ros
 
#### 强制删除容器（包括已停止的）
sudo docker rm -f ptz_ros