# 搜索救援机器人项目组 WIKI
## 本库收录部分关键程序代码，未包含所有程序
## 项目介绍
###### Turtlebot3-Wiffle-pi，是金科实验室的大号机器车，Opencv控制雷达，电机，以及供电，树莓派负责ros程序以及对opencv的程序控制。本项目是Jungle的毕业设计。标题是搜索救援机器人的研究。将利用Turtlebot3平台，加入多个搜索救援用到的传感器（红外摄像，双目视觉，有害气体检测），以及设计一个搜索救援控制台（websocket+python）。

## ROS环境安装
###### 树莓派集成ROS环境的Ubuntu mate16.04镜像下载：https://github.com/AtsushiSaito/Ubuntu16.04_for_RaspberryPi/releases
###### 安装好系统后，换国内源，下载github上turtlebot3源码，进行编译。
##### 注意：1.使用ubuntu18.04或者raspberry系统，使用的是melodic版本的ROS环境，需要将所有Kinetic替换成melodic
#####       2.如果使用Ubuntu16.04，树莓派会出现彩虹屏问题，可以用官方的raspi镜像boot分区覆盖除cmdline.txt以外文件。
#####       3.Turtlebot3 使用需要加入环境变量 
    echo "export TURTLEBOT3_MODEL=型号" >> ~/.bashrc  
    source ~/.bashrc
    env | grep TURTLEBOT3   检查，环境变量是否正确，否则每次都需要声明模型


## HC-SR501红外传感器
#### 三个引脚和电位器未标注，下面方向都是引脚靠近自己：
###### 左侧为正极接5V，右侧接地，中间高低电平输出 程序中接12。
###### 1、调节距离电位器（右侧）顺时针旋转，感应距离增大（约 7 米），反之，感应距离减小（约 3 米）。
###### 2、调节延时电位器（左侧）顺时针旋转，感应延时加长（约300S），反之，感应延时减短（约 0.5S）。

## MQ-2烟雾传感器
#### 四个引脚：
###### 1. VCC：输入5V正极电流
###### 2. GND：接电源负极
###### 3. DO：TTL高低电平输出端   程序中接36
###### 4. AO：模拟电压输出端 （程序中没有使用，只用了高低电平判断）
###### 电位器顺时针灵敏度调节，可以使用打火机吹灭后测试传感器是否正常。

## 机器人FRP内网穿透
###### 机器人必须实时进行监测和控制，而很多情况下获取机器人IP必须进入路由器管理界面，或者插上显示器，所以采用FRP内网穿透，保证通信畅通。
###### 采用了阿里云学生机平台搭建的FRPS客户端，通过tcp内网穿透，达到外网随时随地可以访问树莓派。这样在多种环境下，只要保证树莓派有网络连接，都可以直接进行控制台控制或者进行代码编程。教程地址可见本人博客 https://jungleshi.cn/index.php/archives/15/
###### 注意： 树莓派若使用wifi或者pppoe进行联网，设置systemctl自启动会出现开机无法连接frp的情况，请使用上方github库中的frpc.service


## ROS Bridge
###### Rosbridge为非ROS程序提供了一个使用ROS功能的JSON API。 有许多前端与rosbridge接口，包括一个WebSocket服务器，用于Web浏览器进行交互。Rosbridge_suite是一个包含rosbridge的元包，rosbridge的各种前端包，像一个WebSocket包和帮助包。
###### 作用：  采用Rosbridge采集ros环境下各种参数，和机器人控制台进行实时交流，并且通过rosbridge中的websocket实现对机器人的远程便携式控制。


## 仿真
##### 编译仿真库：
    $ mkdir -p ~/catkin_ws/src
    $ cd ~/catkin_ws/src
    $ git clone https://github.com/ROBOTIS-GIT/turtlebot3_msgs.git
    $ git clone https://github.com/ROBOTIS-GIT/turtlebot3.git
    $ git clone https://github.com/ROBOTIS-GIT/turtlebot3_simulations.git
    $ cd ~/catkin_ws
    $ rosdep install --from-paths src -i -y
    $ catkin_make
##### Gazebo仿真：（拥有物理效果并且有复杂的空间）第一次启动挂好代理
    roslaunch turtlebot3_gazebo turtlebot3_empty_world.launch
    roslaunch turtlebot3_gazebo turtlebot3_world.launch
    roslaunch turtlebot3_gazebo turtlebot3_house.launch
    新tty窗口：
    roslaunch turtlebot3_gazebo turtlebot3_simulation.launch  //启动gazebo
    roslaunch turtlebot3_teleop turtlebot3_teleop_key.launch //键盘控制
    roslaunch turtlebot3_slam turtlebot3_slam.launch slam_methods:=gmapping  //启动slam
    rosrun map_server map_saver -f ~/map                 //保存地图

###### Gazebo仿真手动下载模型：
    $ cd ~/.gazebo/
    $ mkdir -p models
    $ cd ~/.gazebo/models/
    $ wget http://file.ncnynl.com/ros/gazebo_models.txt
    $ wget -i gazebo_models.txt
    $ ls model.tar.g* | xargs -n1 tar xzvf
