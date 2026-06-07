**Configuration**

Basic Structure
===============

The config file, config.yml, has all of the configuration settings for widgets, proxmox, docker, and more. This file goes over the structure of config.yml file. It is recommended to put your authentication information, like for proxmox and docker, at the top of the document, then widgets.

Authentication
==============

Proxmox
-------

|

proxmox:

host: 192.168.1.100

user: <root@pam>

pass: yourpassword

node: nodename

 |

This defines credentials for connecting to the proxmox api.

|

**host**: This is the ip address of your proxmox server

 |
|

**user**: This is the username for the user you want to use. It will usually be <root@pam> if you haven't specifically added any other users that you want to use

 |
|

**pass**: This is the password in plain-text for the username you defined above

 |
|

**node**: This is the name/hostname for the node (part of the tree under 'Datacenter'

 |

Docker
------

**Setup**

In order to use docker, you must setup a ssh key.

1\. On the system you plan to use for the dashboard, run *ssh-keygen -t ed25519 -c "Dashboard"*

2. Hit enter on the prompts to use defaults and not add password.

3. On the same machine, run *ssh-copy-id <youruser@ipfordocker>* Enter the password for the docker system when asked

4. Test by running *ssh <youruser@ipfordocker>*. If it lets you login without your password, your good to go.

**Config**

|

docker:

host: 192.168.1.100

user: myusername

 |

Connects to docker running on an external machine

|

**host**: The ip address for the server running docker

 |
|

**user**: The username to login as (MUST BE THE SAME AS YOU USED FOR THE SSH KEY)

 |

Custom
------

|

custom:

custom1:

host: 192.168.1.100

user: root

password: 1234

command: systemctl restart myservice.service

custom2:

host: 192.168.1.101

user: myusername

password: 12345

command: systemctl restart myservice.service

 |

If you aren't using docker or proxmox, you can use this to run any command on any server

|

**[custom name]**: You can define multiple custom commands, this is just the name for each one

 |
|

**host**: The ip address of the host you want to run the command on

 |
|

**user**: The user to run the command as

 |
|

**password**: The password for the user you set above

 |
|

**command**: The command to run on the host

 |

Widgets
=======

Monitor
-------

|

Monitor:

myproxmoxservice:

service: proxmox

type: lxc

id: 102

url: [http://192.168.1.100:8080](http://192.168.1.100:8080/)

mydockerservice:

service: docker

name: mycontainername

url: [http://192.168.1.100:8080](http://192.168.1.100:8080/)

mycustomservice:

service: custom

name: custom1

url: [http://192.168.1.100:8080](http://192.168.1.100:8080/)

 |

This widget monitors a web ui and lets you restart a proxmox VM/LXC, docker container, or run a custom command if the service is down

|

**[service name]**: The name to display

 |
|

**service**: the service used for the software monitord (accepted: proxmox, docker, name of custom service)

 |
|

**url:** The exact url for the web ui, including protocol (http/https) and port (:8080) (Required for all services)

 |
|

**type**:The thing the service runs on (accepted: vm, lxc) (required only for proxmox)

 |
|

**id**:The id for the lxc/vm (required only for proxmox)

 |
|

**name**: Name of the docker container/custom service (required only for docker and custom)

 |
