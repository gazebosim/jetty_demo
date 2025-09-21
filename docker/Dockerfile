FROM docker.io/library/ros:rolling-ros-core-noble

RUN apt update \
    && apt install -y ros2-testing-apt-source ros-dev-tools \
    && apt dist-upgrade -y

RUN apt update \
    && apt install -y ros-rolling-gz-sim-vendor lld

RUN mkdir -p /ws_rmf/src
COPY rmf.repos rmf.repos
RUN vcs import /ws_rmf/src < rmf.repos
RUN rosdep init \
    && rosdep update \
    && rosdep install --from-paths /ws_rmf/src -yi
RUN . /opt/ros/rolling/setup.sh \
    && cd /ws_rmf \
    && colcon mixin add default https://raw.githubusercontent.com/colcon/colcon-mixin-repository/master/index.yaml \
    && colcon mixin update default \
    && colcon build --mixin release lld

RUN apt-get clean \
    && rm -rf /var/lib/apt/lists/*
