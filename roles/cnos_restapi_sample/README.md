# Ansible Role: cnos_restapi_sample - Configuring Telemetry report on Lenovo CNOS device
---
<add role description below>

This role is an example of using the *cnos_restapi.py* Lenovo module in the context of CNOS switch configuration. This module allows you to access Restapis on the Lenovo CNOS devices.

The results of the operation can be viewed in *results* directory.


## Requirements
---
<add role requirements information below>

- Ansible version 2.4 or later ([Ansible installation documentation](http://docs.ansible.com/ansible/intro_installation.html))
- Lenovo switches running CNOS version 10.5.1.0 or later
- restapi must be enabled on the Lenovo switch


## Role Variables
---
<add role variables information below>

Available variables are listed below, along with description.

The following are mandatory inventory variables:

Variable | Description
--- | ---
`username` | Specifies the username used to log into the switch
`password` | Specifies the password used to log into the switch
`hostname` | Searches the hosts file at */etc/ansible/hosts* and identifies the IP address of the switch on which the role is going to be applied
`deviceType` | Specifies the type of device from where the configuration will be backed up (**g8272_cnos** - G8272, **g8296_cnos** - G8296)

The values of the variables used need to be modified to fit the specific scenario in which you are deploying the solution. To change the values of the variables, you need to visits the *vars* directory of each role and edit the *main.yml* file located there. The values stored in this file will be used by Ansible when the template is executed.

The syntax of *main.yml* file for variables is the following:

```
<template variable>:<value>
```

You will need to replace the `<value>` field with the value that suits your topology. The `<template variable>` fields are taken from the template and it is recommended that you leave them unchanged.

Variable | Description
--- | ---
`urlpath` | Specifies the url path of the restapi
`use_ssl` | Specifies the transport layer used by the RESTAPI. False choice indicates http plaintext communication over port 8090. True indicates https secured encrypted comminication
`method` | The HTTP method of the restapi request. 
`jsoninp` | Input json dictionary. Used by POST, PUT method to input request paramters.


## Dependencies
---
<add dependencies information below>

- username.iptables - Configures the firewall and blocks all ports except those needed for http(port=8090) or https(port=443) server.
- /etc/ansible/hosts - You must edit the */etc/ansible/hosts* file with the device information of the switches.

Ansible keeps track of all network elements that it manages through a hosts file. Before the execution of a playbook, the hosts file must be set up.

Open the */etc/ansible/hosts* file with root privileges. Most of the file is commented out by using **#**. You can also comment out the entries you will be adding by using **#**. You need to copy the content of the hosts file for the role into the */etc/ansible/hosts* file.
  
```
[cnos_restapi_sample]
10.241.107.39   username=<username> password=<password> deviceType=g8272_cnos
10.241.107.40   username=<username> password=<password> deviceType=g8272_cnos
```
  
**Note:** You need to change the IP addresses to fit your specific topology. You also need to change the `<username>` and `<password>` to the appropriate values used to log into the specific Lenovo network devices.


## Example Playbook
---
<add playbook samples below>

To execute an Ansible playbook, use the following command:

```
ansible-playbook cnos_restapi_sample.yml -vvv
```

`-vvv` is an optional verbos command that helps identify what is happening during playbook execution. The playbook for each role is located in the main directory of the solution.

```
- name: Module to configure the telemetry report using CNOS restapi's
   hosts: cnos_restapi_sample
   gather_facts: no
   connection: local
   roles:
    - cnos_restapi_sample
```


## License
---
<add license information below>
Copyright (C) 2017 Lenovo, Inc.

This Ansible Role is distributed WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  

See the [GNU General Public License](http://www.gnu.org/licenses/) for more details.
