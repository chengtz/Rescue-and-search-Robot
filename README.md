# 搜索救援机器人项目组 WIKI
## 本库收录部分关键程序代码，未包含所有程序
## 项目介绍
###### Turtlebot3-Wiffle-pi，是金科实验室的大号机器车，Opencv控制雷达，电机，以及供电，树莓派负责ros程序以及对opencv的程序控制。本项目是Jungle的毕业设计。标题是搜索救援机器人的研究。将利用Turtlebot3平台，加入多个搜索救援用到的传感器（红外摄像，双目视觉，有害气体检测），以及设计一个搜索救援控制台（websocket+python）。

## ROS环境安装
###### Turtlebot3树莓派的ROS环境安装教程：https://www.ncnynl.com/archives/201807/2531.html
###### 注意：使用ubuntu18.04或者raspberry系统，使用的是melodic版本的ROS环境，需要将所有Kinetic替换成melodic

## MQ-2烟雾传感器
#### 有四个引脚：
1. VCC：输入5V正极电流
2. GND：接电源负极
3. DO：TTL高低电平输出端   接GPIO 36
4. AO：模拟电压输出端 （程序中没有使用，只用了高低电平判断）

## 机器人FRP内网穿透
###### 机器人必须实时进行监测和控制，而很多情况下获取机器人IP必须进入路由器管理界面，或者插上显示器，所以采用FRP内网穿透，保证通信畅通。
###### 采用了阿里云学生机平台搭建的FRPS客户端，通过tcp内网穿透，达到外网随时随地可以访问树莓派。这样在多种环境下，只要保证树莓派有网络连接，都可以直接进行控制台控制或者进行代码编程。教程地址可见本人博客 https://jungleshi.cn/index.php/archives/15/
###### 注意： 树莓派若使用wifi或者pppoe进行联网，设置systemctl自启动会出现开机无法连接frp的情况，请使用上方github库中的frpc.service


## ROS Bridge
###### Rosbridge为非ROS程序提供了一个使用ROS功能的JSON API。 有许多前端与rosbridge接口，包括一个WebSocket服务器，用于Web浏览器进行交互。Rosbridge_suite是一个包含rosbridge的元包，rosbridge的各种前端包，像一个WebSocket包和帮助包。
###### 作用：  采用Rosbridge采集ros环境下各种参数，和机器人控制台进行实时交流，并且通过rosbridge中的websocket实现对机器人的远程便携式控制。


## HTML页面设计
