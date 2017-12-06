# CNOS Restapi Module for support of Lenovo's CNOS-based networking device in Ansible

## Overview

* Module provide access CNOS Restapi for switch management functions.
* Python Script to generate telemetry roles based on user input

## Requirements

* Ansible 2.4 installed.  [Ansible Installation Instructions](http://docs.ansible.com/ansible/intro_installation.html)
* Lenovo CNOS network device version 10.5 or later
* Restapi Feature enabled on switch

## Documentation

### Cnos Restapi Module
Performs restapi operations from a remote server on devices running Lenovo CNOS.

#### Synopsis
This module performs restapi operations on a device running CNOS. The Restapi operations retrive, modify and creates resources on the CNOS device. 
It provides a way to manage CNOS devices remotely from server.

#### Options

parameter | required | default | choices | Description
:------:  | :------: | :------:| ------ | ------
outputfile|  yes     |  null   |   []   | This specifies the file path to which the output of each command execution is persisted.Response from the device saved here. Usually the location is the results folder. But your user can choose which ever path he has write permission. 
host      |  yes     |  null   |   []   | This is the variable which used to look into /etc/ansible/hosts file so that device IP addresses on which this template has to be applied is identified. Usually we specify the ansible keyword {{ inventory_hostname }} which we specify in the playbook which is an abstraction to the group of network elements that need to be configured.
username  |  yes     |  null   |   []   | Configures the username to use to authenticate the connection to the remote device. The value of  username is used to authenticate the REST session. The value has to come from inventory file ideally, you can even enter it as variable.
password  |  yes     |  null   |   []   | Configures the password to use to authenticate the connection to the remote device. The value of password is used to authenticate the REST session.The value has to come from inventory file ideally you can even enter it as variable.
use_ssl   |  no     |  True   |[True,False]  | Transport layer used by the RESTAPI. False choice  indicates http  plaintext communication over port 8090. True indicates https secured encrypted comminication
urlpath   |  yes     |  null   |   []         | URL Path of the RESTAPI
method    |  yes     |  null   |[GET,PUT,POST]| The HTTP method of the request.  GET is typically used for querying objects. POST is typically used for creating/querying objects. PUT is typically used for modifying objects
jsoninp   |  no     |  null   |   []         | Input json dictionary. Used by POST, PUT method to input request paramters

#### Examples
The following are examples of using the module cnos_restapi. These are written in the main.yml file of the tasks directory. 
```sh
- name: Configure BST feature using a JSON string
  cnos_restapi:
    host: '{{ inventory_hostname }}'
    username: '{{ username }}'
    password: '{{ password }}'
    outputfile: "./results/test_restapi_{{ inventory_hostname }}_output.txt"
    use_ssl: True
    urlpath: /nos/api/cfg/telemetry/bst/feature
    method: PUT
    jsoninp: '{"collection-interval": 20, "send-async-reports": 1,
             "send-snapshot-on-trigger": 1, "trigger-rate-limit": 1,
              "async-full-report": 0, "trigger-rate-limit-interval": 11,
              "bst-enable": 1}'

- name: Fetch BST feature using a JSON string
  cnos_restapi:
    host: '{{ inventory_hostname }}'
    username: '{{ username }}'
    password: '{{ password }}'
    outputfile: "./results/test_restapi_{{ inventory_hostname }}_output.txt"
    use_ssl: True
    urlpath: /nos/api/cfg/telemetry/bst/feature
    method: GET

- name: Fetch BST feature using a JSON string
  cnos_restapi:
    host: '{{ inventory_hostname }}'
    username: '{{ username }}'
    password: '{{ password }}'
    outputfile: "./results/test_restapi_{{ inventory_hostname }}_output.txt"
    use_ssl: True
    urlpath: /nos/api/info/telemetry/bst/congestion-drop-counters
    method: POST
    jsoninp: '{"req-id" : 1, "request-type" : "port-drops", "request-params": {"interface-list": ["Ethernet1/1", "Ethernet1/2", "Ethernet1/3"]}}'

```

#### Return Values
On successful execution, the method returns an string with the following message in JSON format: 
"RESTAPI [GET,PUT,POST]  urlpath is successful"

Upon any failure, the method returns an error display string. 

### Python Script to generate telemetry roles based on user input

The python script *tlmreport.py* creates telemetry roles based on user input. It creates commands, results, template, tasks and vars sub-directory, populating the tasks and the variable in the tasks and variable directory respectively. 

The script is executed using the python.
"python tlmreport.py"

#### User input Description

##### rolename
      The ansible rolename used by the playbook. A directory is created with the rolename with the commands, results, template, tasks 
      and vars sub-directory. 
      directory.
##### Controller IP
      The IP address of the controller which receives the telemetry data from the switch. 
##### Controller Port
      The controller TCP listening port that receives the telemetry data from the switch. 
##### Controller Vrf
      The vrf of the configured IP address. This is either management or default
##### Heart beat interval 
      The switch sends heartbeat to the configured controller every few seconds. The heartebeat interval is configured by this    
      parameter. The range is between 1 and 600.
##### Report type 
      The type of telemetry report.
      1 - Predictive Congestion Report 
      2 - Congestion_Detection
      3 - Capacity_Planning
  
  Report Type | Description
  --- | ---
  Predictive Congestion Report | This selection sets thresholds on certain realms. On reaching the configured threshold, the switch sends reports to the controller. *Trigger Rate Interval* is the interval when these threshold reports are sent to the controller from the switch. *realm* is the realm that use choose to configure the threshold. The script request user to enter the indexes and the threshold values for the configured realm.
 Congestion_Detection | This selection configures congestion detection reports periodically. There are four types of congestion reports supported. *top-drops* reports the ports experiencing maximum congestion. The number of ports and the periodicity of the report is further required as input for *top-drop* report. *port-drops* reports the port specific congestion.The list of interfaces and the periodicity of the report is further required as input for *port-drop* report. *top-port-queue-drops* reports the port queues experiencing maximum congestion. The number of port queues, the periodicity of the report and queue-type are further requested as input for *top-port-queue-drops* report. *port-queue-drops* reports port queues specific congestion. The list of interfaces, type of queue, periodicity and queue list is further required as input for *port-queue-drops* report.
 Capacity Planning | This selection configures a periodic report of the current realms buffer count. The periodicity of the report is further given as input.
         
### Role Deployment
 Copy the role directory contents to the ansible role directory path. 
 
## License

* GPLv3
* Copyright (C) 2017 Lenovo, Inc.

