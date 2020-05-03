# 搜索救援机器人项目组 WIKI
## 本库收录项目关键部分和出现问题部分，非整库和安装教学
## 项目介绍
###### 基于Turtlebot3-Wiffle-pi，Opencv控制激光雷达，电机，以及供电，树莓派负责ros程序以及对opencv的程序控制。本项目是Jungle的毕业设计。标题是搜索救援机器人的研究。将利用Turtlebot3平台，加入多个搜索救援用到的传感器（红外摄像，双目视觉，有害气体检测），以及设计一个搜索救援控制台（websocket+python）。

## ROS环境安装
###### 树莓派集成ROS环境的Ubuntu mate16.04镜像下载：https://github.com/AtsushiSaito/Ubuntu16.04_for_RaspberryPi/releases
###### 安装好系统后，换国内源，下载turtlebot3或者其他机器人源码，进行编译。
##### 注意：1.使用最新ubuntu18.04或者raspberry系统的，使用的是melodic版本的ROS环境，需要将本文档所有Kinetic替换成melodic
#####       2.如果使用Ubuntu16.04，树莓派会出现彩虹屏问题，可以用官方的raspi镜像boot分区覆盖除cmdline.txt以外文件。
#####       3.Turtlebot3 使用需要加入环境变量 
    echo "export TURTLEBOT3_MODEL=型号" >> ~/.bashrc   //设置好这里后以后就不用再一次次声明参数
    env | grep TURTLEBOT3   检查，环境变量是否正确
    source ~/catkin_ws/devel/setup.sh  //设置好这里后安装软件包不用再一次次声明
    source ~/.bashrc
    
#####       4.部分新机器，需要升级内核，并且安装Gnome开源桌面环境，仿真建模会快很多

## HC-SR501红外传感器
#### 三个引脚和电位器未标注，下面方向都是引脚靠近自己：
###### 左侧为正极接5V，右侧接地，中间高低电平输出 程序中接12。
###### 1、调节距离电位器（右侧）顺时针旋转，感应距离增大（约 7 米），反之，感应距离减小（约 3 米）。
###### 2、调节延时电位器（左侧）顺时针旋转，感应延时加长（约300S），反之，感应延时减短（约 0.5S）。
###### 该设备极易损坏

## MQ-2烟雾传感器
#### 四个引脚：
###### 1. VCC：输入5V正极电流
###### 2. GND：接GND
###### 3. DO：TTL高低电平输出端   程序中接36
###### 4. AO：模拟电压输出端 （程序中没有使用，只用了高低电平判断）
###### 电位器初始化:逆时针转动到灯亮，高电平时，缓慢顺时针调整，直至熄灭

## ROS节点添加传感器程序
###### 传感器采用python程序，使用ROS的rospy依赖库，创建好程序包，移入scripts文件夹
###### Cmakelist添加以下声明：
       install(PROGRAMS 
       scripts/your_scripts.py 
       DESTINATION ${CATKIN_PACKAGE_BIN_DESTINATION}
       )
###### catkin_make写入节点，rosrun运行

## 视觉设备
###### 首先本地摄像头流获取
      sudo apt-get install ros-kinetic-uvc-camera
      roscd uvc_camera
      sudo mkdir launch
      cd launch
      sudo nano camera_node.launch
      编辑入以下内容：
      <launch>
      <node pkg="uvc_camera" type="uvc_camera_node" name="uvc_camera" output="screen">
        <param name="width" type="int" value="1280" />
        <param name="height" type="int" value="720" />
        <param name="fps" type="int" value="30" />
        <param name="frame" type="string" value="wide_stereo" />
        <param name="auto_focus" type="bool" value="False" />
        <param name="focus_absolute" type="int" value="0" />
        <!-- other supported params: auto_exposure, exposure_absolute, brightness, power_line_frequency -->

        <param name="device" type="string" value="/dev/video0" />
        <param name="camera_info_url" type="string" value="file://$(find uvc_camera)/example.yaml" />
      </node>
      </launch>
###### 摄像头web_video_server安装,这个教程很多，注意一定要先安装UVC获取本地流！
###### 因为采用双目摄像头，单目720p已经达到15Mbit带宽，双目需要达到30Mbit带宽，局域网可以跑，但是本项目采用的是云端控制，导致延迟升高，所以采用流压缩处理。
      
## 机器人FRP内网穿透
###### 机器人必须实时进行监测和控制，而很多情况下获取机器人IP必须进入路由器管理界面，或者插上显示器，所以采用FRP内网穿透，保证通信畅通。
###### 采用了阿里云学生机平台搭建的FRPS客户端，通过tcp内网穿透，达到外网随时随地可以访问树莓派。这样在多种环境下，只要保证树莓派有网络连接，都可以直接进行控制台控制或者进行代码编程。教程地址可见本人博客 https://jungleshi.cn/index.php/archives/15/
###### 注意： 树莓派若使用wifi或者pppoe进行联网，设置systemctl自启动会出现开机无法连接frp的情况，请使用上方github库中的frpc.service

## ROS Bridge
###### Rosbridge为非ROS程序提供了一个使用ROS功能的JSON API。 有许多前端与rosbridge接口，包括一个WebSocket服务器，用于Web浏览器进行交互。Rosbridge_suite是一个包含rosbridge的元包，rosbridge的各种前端包，像一个WebSocket包和帮助包。
###### 作用：  采用Rosbridge采集ros环境下各种参数，和机器人控制台进行实时交流，并且通过rosbridge中的websocket实现对机器人的远程便携式控制。

## Roslibpy
###### roslibpy是ros支持python的环境库，可以让自己的python程序快速便捷的加入ROS的消息订阅节点中，方便在ROS系统下运行我们自己的Python程序
###### 安装方法：
    python -m pip install --upgrade pip  //升级Pip
    pip install roslibpy  //安装库
    
    import roslibpy  //基础例子
    client = roslibpy.Ros(host='localhost', port=9090)
    client.run()
    print('Is ROS connected?', client.is_connected)
    client.terminate()
    
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
    
## 控制台
##### ROS端：
    roslaunch rosbridge_server rosbridge_websocket.launch
    rosrun uvc_camera uvc_camera_node 
    roslaunch web_video_server web_video.launch
    rosrun sense yanwu.py
    rosrun sense redsense.py
##### WEB端：
          var listener2 = new ROSLIB.Topic({
          ros : rbServer,
          name : '/X',
          messageType : 'std_msgs/String'
          });
          listener2.subscribe(function(message) {
          document.getElementById("ID").innerHTML = message.data;
          console.log('X：' + message.data);
          });
    
## 视觉处理
##### 采用Openpose项目，可识别人体结构、脸部特征
安装步骤：
1.准备：Openpose release   openpose_caffe_models   CUAD9.2 cudnn-9.2  
2.安装完毕，cmd启动 bin\OpenPoseDemo --

--face: 开启 Face 关键点检测.

--hand: 开启 Hand 关键点检测

--video input.mp4: 读取 Video.

--camera 3: 读取 webcam number 3.

--image_dir path_to_images/: 运行图像路径内的图片.

--ip_camera http://iris.not.iac.es/axis-cgi/mjpg/video.cgi?resolution=320x240?x.mjpeg: 在 streamed IP camera 上运行. 参考public IP cameras 例子.

--write_video path.avi: 将处理后的图片保存为 Video.

--write_images folder_path: 将处理后的图片保存到指定路径.

--write_keypoint path/: 在指定路径输出包含人体姿态数据的 JSON, XML 或 YML 文件.

--process_real_time: 对于视频，可能在实时运行时，跳过某些视频帧.

--disable_blending: 如果 --disable_blending=True，则在很色背景上渲染估计结果(如 keypoints skeletons 和 heatmaps)，而不显示原始图像. Related: part_to_show, alpha_pose, and alpha_pose.

--part_to_show: 可视化的预测通道(Prediction channel).

--display 0: 不打开可视化显示窗口. 对于服务器部署和 OpenPose 加速很帮助.

--num_gpu 2 --num_gpu_start 1: 多 GPUs 时，设置开始的 GPU id. 默认使用所有可用的 GPUs.

--model_pose MPI: 采用的模型Model，影响 Keypoints 的数量、运行速度和精度.

--logging_level 3: Logging messages threshold, range [0,255]: 0 - 输出所有信息e & 255 - 不输出任何信息. Current messages in the range [1-4], 1 for low priority messages and 4 for important ones.

保存：bin\OpenPoseDemo.exe --image_dir examples/media/ --write_images examples/media_out/
