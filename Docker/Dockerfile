FROM ros:melodic-ros-core-bionic

# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

ENV GITLAB_TOKEN_MARS=6ThiiJd_xcSFFASN3Fye
ENV GITLAB_TOKEN_TS=XKw-VpSxMj52YcN4rQmp 

RUN apt-get update && apt-get install -y \
    ros-melodic-industrial-msgs \
    ros-melodic-behaviortree-cpp-v3 \
    git\   	
    software-properties-common \
    python2.7 \
    python-pip


# Setup catkin_ws
RUN mkdir catkin_ws \
    && mkdir catkin_ws/src \
    && mkdir catkin_ws/src/MARS 
WORKDIR /catkin_ws/src
RUN /bin/bash -c '. /opt/ros/melodic/setup.bash; catkin_init_workspace'

# Init catkin_ws
WORKDIR /catkin_ws
RUN /bin/bash -c '. /opt/ros/melodic/setup.bash; catkin_make'

# Setup TS
WORKDIR /catkin_ws/src/
RUN git clone https://oauth2:$GITLAB_TOKEN_MARS@gitlab.cc-asp.fraunhofer.de/iml/oe130/ROS/ROS-MARS/mars_common.git
RUN git clone https://oauth2:$GITLAB_TOKEN_MARS@gitlab.cc-asp.fraunhofer.de/iml/oe130/ROS/ROS-MARS/mars_common_msgs.git
RUN git clone https://oauth2:$GITLAB_TOKEN_MARS@gitlab.cc-asp.fraunhofer.de/iml/oe130/ROS/ROS-MARS/Virtual-Agents/mars_agent_logical_msgs.git
RUN git clone https://oauth2:$GITLAB_TOKEN_MARS@gitlab.cc-asp.fraunhofer.de/iml/oe130/ROS/ROS-MARS/Virtual-Agents/mars_agent_virtual_srvs.git
RUN git clone https://oauth2:$GITLAB_TOKEN_MARS@gitlab.cc-asp.fraunhofer.de/iml/oe130/ROS/ROS-MARS/Topology/mars_topology_msgs.git
RUN git clone https://oauth2:$GITLAB_TOKEN_MARS@gitlab.cc-asp.fraunhofer.de/iml/oe130/ROS/ROS-MARS/Physical-Agents/mars_agent_physical_robot_msgs.git
RUN git clone https://oauth2:$GITLAB_TOKEN_MARS@gitlab.cc-asp.fraunhofer.de/iml/oe130/infa-cts/taskplanner.git
RUN pip install -r ./taskplanner/requirements.txt


# Build TS
WORKDIR /catkin_ws
RUN /bin/bash -c '. /opt/ros/melodic/setup.bash; . /catkin_ws/devel/setup.bash; catkin_make'

# Add ROS setup bash to .bashrc
RUN echo 'source /opt/ros/melodic/setup.bash \n source /catkin_ws/devel/setup.bash' >> /root/.bashrc

EXPOSE 2906



# Clean up
RUN rm -rf /var/lib/apt/lists/*

# Clean up MARS
RUN rm -rf /catkin_ws/src/mars_common/include
RUN rm -rf /catkin_ws/src/mars_common/test
RUN rm -rf /catkin_ws/src/mars_common/.git
RUN rm -rf /catkin_ws/src/mars_common/src/EntityVisualization.cpp
RUN rm -rf /catkin_ws/src/mars_common/src/Id.cpp
RUN rm -rf /catkin_ws/src/mars_common/src/Result.cpp
RUN rm -rf /catkin_ws/src/mars_common/src/TimeInterval.cpp
RUN rm -rf /catkin_ws/src/mars_common/src/Tuple.cpp
RUN rm -rf /catkin_ws/src/mars_common/src/Value.cpp
RUN rm -rf /catkin_ws/src/taskplanner/Docker/Dockerfile

#RUN cd ./taskplanner
# run the application
WORKDIR /catkin_ws/src/taskplanner
COPY start.sh /catkin_ws/src/taskplanner/start.sh
RUN chmod +x start.sh
CMD "./start.sh"
