FROM ghcr.io/gazebosim/gz-jetty:main
ENV LANG=C
ENV LC_ALL=C
ARG DEBIAN_FRONTEND=noninteractive

RUN apt-get update \
    && apt-get install -y curl
ENV ROS_APT_SOURCE_VERSION=1.1.0
RUN curl -L -o /tmp/ros2-apt-source.deb "https://github.com/ros-infrastructure/ros-apt-source/releases/download/${ROS_APT_SOURCE_VERSION}/ros2-apt-source_${ROS_APT_SOURCE_VERSION}.$(. /etc/os-release && echo ${UBUNTU_CODENAME:-${VERSION_CODENAME}})_all.deb"
RUN dpkg -i /tmp/ros2-apt-source.deb
RUN apt-get update \
    && apt-get install -y ros-dev-tools ros-rolling-ros-core \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*
