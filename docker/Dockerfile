FROM docker.io/library/ros:rolling-ros-core-noble

RUN apt update \
    && apt install -y ros2-testing-apt-source ros-dev-tools \
    && apt dist-upgrade -y

RUN apt update \
    && apt install -y curl lld

RUN mkdir -p /ws_jetty/src \
    && cd /ws_jetty/src
# TODO(ac): update branch once it is merged
RUN mkdir -p /ws_jetty/src/jetty_demo \
    && curl -L https://github.com/gazebosim/jetty_demo/archive/ac/rmf-demo.tar.gz -o jetty_demo.tar.gz \
    && tar zxf jetty_demo.tar.gz -C /ws_jetty/src/jetty_demo --strip-components=1 \
    && rm jetty_demo.tar.gz
RUN vcs import /ws_jetty/src < /ws_jetty/src/jetty_demo/docker/rmf.repos
RUN rosdep init \
    && rosdep update \
    && rosdep install --from-paths /ws_jetty/src -yi
RUN . /opt/ros/rolling/setup.sh \
    && cd /ws_jetty \
    && colcon mixin add default https://raw.githubusercontent.com/colcon/colcon-mixin-repository/master/index.yaml \
    && colcon mixin update default \
    && colcon build --mixin release lld

RUN apt-get clean \
    && rm -rf /var/lib/apt/lists/*

RUN sed --in-place \
        --expression '$isource "/ws_jetty/install/setup.bash"' \
        /ros_entrypoint.sh

ENV RMW_IMPLEMENTATION=rmw_zenoh_cpp
