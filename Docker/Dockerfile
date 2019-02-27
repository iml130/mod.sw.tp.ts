FROM ubuntu:latest

### Pre Settings:
# Set Proxy Settings 
ENV http_proxy http://www-cache:80/
ENV https_proxy http://www-cache:80/
ENV all_proxy socks://www-cache:80/
ENV ftp_proxy ftp://www-cache:80/

# apt-key add via Keyserver is not working (maybe firewall?), instead we just copy the key manually. (Needed for ROS-Installation)
#COPY key.txt ./
# package tzdata is interactive, we supress it. (Needed for ROS-Installation)
#ENV DEBIAN_FRONTEND=noninteractive



### Checking for Updates (?)
RUN apt-get update && apt-get upgrade -y && apt-get dist-upgrade -y



### Installation Pytthon2.7
RUN apt-get update
RUN apt-get install -y python2.7
RUN apt-get install -y python-pip



### Installation ROS Melodic
#lsb-cre needed for lsb_release
#RUN apt-get install -y lsb-core 
#RUN sh -c 'echo "deb http://packages.ros.org/ros/ubuntu $(lsb_release -sc) main" > /etc/apt/sources.list.d/ros-latest.list'
#RUN apt-key add key.txt
#RUN apt-get update

# Which one is needed?
#RUN apt-get install -y ros-melodic-desktop-full
#RUN apt-get install -y ros-melodic-desktop
#RUN apt-get install -y ros-melodic-ros-base

#RUN rosdep init 
#RUN rosdep update
#RUN echo "source /opt/ros/melodic/setup.bash" >> ~/.bashrc
#RUN ["/bin/bash",  "-c", "source ~/.bashrc"]
# Are Dependencies to build packages needed?
#RUN apt-get install -y python-rosinstall python-rosinstall-generator python-wstool build-essential