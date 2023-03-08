FROM ubuntu:22.04

# Set up user as it's on the host
ARG USER_UID
ARG USER_NAME

RUN groupadd -g ${USER_UID} ${USER_NAME}
RUN useradd -r -u ${USER_UID} -g ${USER_UID} ${USER_NAME}

LABEL Description="Image to facilitate development of DB Backups app."

ENV DEBIAN_FRONTEND=noninteractive

# Install required packages to run apps
RUN apt-get update && apt-get install -y build-essential git bash-completion python3-pip wget autoconf libtool unzip curl vim

# Install required packages to manage mysql
RUN apt-get update && apt-get install -y mysql-client

# Install pip and virtualenv
RUN apt-get update && apt-get install -y python3-pip python3-gdbm
RUN yes | pip3 install setuptools --upgrade
RUN yes | pip3 install virtualenv pyyaml

# Install misc
RUN apt-get update && apt-get install -y sudo

RUN echo "${USER_NAME} ALL=(ALL) NOPASSWD:ALL" > /etc/sudoers.d/docker

# Set up locales
RUN apt-get update && apt-get install -y locales
RUN sed -i -e 's/# en_US.UTF-8 UTF-8/en_US.UTF-8 UTF-8/' /etc/locale.gen && \
    locale-gen

# Set up terminal colors
ENV TERM=xterm-256color
COPY ./scripts/00-aliases.sh /etc/profile.d/
COPY ./scripts/02-colors.sh /etc/profile.d/

# Set up executables for creating the environment
COPY ./scripts/attach_env /usr/local/bin
COPY ./scripts/setup_env /usr/local/bin

# Set up user
USER ${USER_NAME}
ENV HOME=/home/${USER_NAME}
