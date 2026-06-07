# Configuration
## Basic Structure
The config file, config.yml, has all of the configuration settings for widgets, proxmox, docker, and more. This file goes over the structure of config.yml file. It is recommended to put your authentication information, like for proxmox and docker, at the top of the document, then widgets.

## Authentication

### Proxmox
This defines credentials for connecting to the proxmox API.

```yaml
proxmox:
    host: 192.168.1.100
    user: root@pam
    pass: yourpassword
    node: nodename
```

`host`: This is the ip address of your proxmox server<br>
`user`: This is the username for the user you want to use. It will usually be root@pam if you haven’t specifically added any other users that you want to use<br>
`pass`: This is the password in plain-text for the username you defined above<br>
`node`: This is the name/hostname for the node (part of the tree under ‘Datacenter’)

### Docker
<b>Setup</b><br>
In order to use docker, you must setup a ssh key.
1. On the system you plan to use for the dashboard, run `ssh-keygen -t ed25519 -c “Dashboard”`
2. Hit enter on the prompts to use defaults and not add password.
3. On the same machine, run `ssh-copy-id youruser@ipfordocker` Enter the password for the docker system when asked
4. Test by running `ssh youruser@ipfordocker`. If it lets you login without your password, your good to go.

<b>Config</b><br>
Connects to docker running on an external machine
```yaml
docker: 
    host: 192.168.1.100
    user: myusername
```
`host`: The IP address for the server running docker<br>
`user`: The username to login as (<b>Must be the same as you used for the ssh key</b>)<br>

### Custom
If you aren’t using docker or proxmox, you can use this to run any command on any server<br>

```yaml
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
        command: sh /home/myusername/script.sh
```
`[custom name]`: You can define multiple custom commands, this is just the name for each one<br>
`host`: The ip address of the host you want to run the command on<br>
`user`: The user to run the command as<br>
`password`: The password for the user you set above<br>
`command`: The command to run on the host<br>

## Widgets
### Monitor
This widget monitors a web ui and lets you restart a proxmox VM/LXC, docker container, or run a custom command if the service is down
```yaml
widgets:
    monitor:
        myproxmoxservice:
            type: lxc
            id: 102
            url: http://192.168.1.100:8080
        mydockerservice:
            service: docker
            name: mycontainername
            url: http://192.168.1.100:8080
        mycustomservice:
            service: custom
            name: custom1
            url: http://192.168.1.100:8080
```
`[service name]`: The name to display in the dashboard<br>
`service`: The service used for the software monitored  (accepted: proxmox, docker, name of custom service)<br>
`url`: The exact url for the web ui, including protocol (http/https) and port (:8080) (Required for all services)<br>
`type`: The thing the service runs on (accepted: vm, lxc) (required only for proxmox)<br>
`id`: The id for the lxc/vm (required only for proxmox)<br>
`name`: Name of the docker container/custom service (required only for docker and custom)
