---
title: Docker based setup
---

## Install and setup Docker on host machine

Follow the instructions available [here](https://docs.docker.com/get-docker/) to install docker on your machine.

You could also go through the [:material-docker: Docker quick start quide](https://docs.docker.com/get-started/) to know more about Docker .

!!! warning
    The following has **not** been tested on _Windows_.
    
    If you encounter any issues/ has suggestions raise an issue [here](https://github.com/eXpOSNitc/expos-docs/issues/new)

## Setting up

We'll assume the following directory structure

``` plaintext
.
├── Dockerfile
└── workdir/ # <- user files will be stored here and mapped to container
```

We'll store the user written code in `workdir` and map the same into the container.

The contents of `Dockerfile` are given below

``` dockerfile
FROM ubuntu:20.04

RUN apt-get update \
    && apt-get install -y bison flex libreadline-dev libc6-dev libfl-dev wget vim make gcc curl unzip build-essential

RUN useradd -m expos
USER expos

RUN cd /home/expos \
    && curl -sSf https://raw.githubusercontent.com/eXpOSNitc/expos-bootstrap/main/download.sh | sh \
    && cd /home/expos/myexpos \
    && make

WORKDIR /home/expos/myexpos
```

The given `Dockerfile` will setup expos environment as specified in [Setting Up Page](./setting-up.md)

### Building the container image

We'll now build the container image using the `Dockerfile`

```sh
docker build -t expos:ubuntu20.04 .
```

### Start the container instance

We'll start an instance of Container and map the local folder `workdir` into `/home/expos/workdir` directory of container.

```sh
# on unix
docker run -v $PWD:/home/expos/myexpos/workdir -d --name expos -i expos:ubuntu20.04 
# on windows
docker run -v %cd%:/home/expos/myexpos/workdir -d --name expos -i expos:ubuntu20.04
```

We now have a container instance running in background with the name `expos` and required volume mounts

### Connecting to the container

We can connect to the container instance using the following commands

```sh
docker start expos # if the container instance is not already running

docker exec -it expos /bin/bash # to get a bash shell inside the container
```

After connecting to the container you can use `spl`, `expl`, `xfs-interface`, and `xsm` binaries as mentioned in [Setting Up Page](./setting-up.md)