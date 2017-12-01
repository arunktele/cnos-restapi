# CNOS Restapi Module for support of Lenovo's CNOS-based networking device in Ansible

## Overview

* Module provide access CNOS Restapi for switch management functions.
* Python Script to generate telemetry roles based on user input

### Requirements

* Ansible 2.4 installed.  [Ansible Installation Instructions](http://docs.ansible.com/ansible/intro_installation.html)
* Lenovo CNOS network device version 10.5 or later
* Restapi Feature enabled on switch

## Documentation

###Lenovo CNOS Restapi Module:

Performs restapi operations from a remote server on devices running Lenovo CNOS.

####Synopsis
This module performs restapi operations on a device running CNOS. The Restapi operations retrive, modify and creates resources on the CNOS device. 
It provides a way to manage CNOS devices remotely from server.

####Options

parameter | required | default | choices      | Description
:------:  | :------: | :------:| :------:     | :------:
outputfile|  yes     |  null   |   []         | This specifies the file path to which the output of each command execution is persisted.Response from the device saved here. Usually the location is the results folder. But your user can choose which ever path he has write permission. 
host      |  yes     |  null   |   []         | This is the variable which used to look into /etc/ansible/hosts file so that device IP addresses on which this template has to be applied is identified. Usually we specify the ansible keyword {{ inventory_hostname }} which we specify in the playbook which is an abstraction to the group of network elements that need to be configured.
username  |  yes     |  null   |   []         | Configures the username to use to authenticate the connection to the remote device. The value of  username is used to authenticate the REST session. The value has to come from inventory file ideally, you can even enter it as variable.
password  |  yes     |  null   |   []         | Configures the password to use to authenticate the connection to the remote device. The value of password is used to authenticate the REST session.The value has to come from inventory file ideally you can even enter it as variable.
use_ssl   |  yes     |  True   |[True,False]  | Transport layer used by the RESTAPI. False choice  indicates http  plaintext communication over port 8090. True indicates https secured encrypted comminication
urlpath   |  yes     |  null   |   []         | URL Path of the RESTAPI
method    |  yes     |  null   |[GET,PUT,POST]| The HTTP method of the request.  GET is typically used for querying objects. POST is typically used for creating/querying objects. PUT is typically used for modifying objects
jsoninp   |  yes     |  null   |   []         | Input json dictionary. Used by POST, PUT method to input request paramters

####Examples
The following are examples of using the module cnos_restapi. These are written in the main.yml file of the tasks directory. 
```sh
- name: Configure BST feature using a JSON string
  cnos_restapi:
    host: '{{ inventory_hostname }}'
    username: '{{ username }}'
    password: '{{ password }}'
    outputfile: "./results/test_restapi_{{ inventory_hostname }}_output.txt"
    transport: https
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
    transport: https
    urlpath: /nos/api/cfg/telemetry/bst/feature
    method: GET

- name: Fetch BST feature using a JSON string
  cnos_restapi:
    host: '{{ inventory_hostname }}'
    username: '{{ username }}'
    password: '{{ password }}'
    outputfile: "./results/test_restapi_{{ inventory_hostname }}_output.txt"
    transport: https
    urlpath: /nos/api/info/telemetry/bst/congestion-drop-counters
    method: POST
    jsoninp: '{"req-id" : 1, "request-type" : "port-drops", "request-params": {"interface-list": ["Ethernet1/1", "Ethernet1/2", "Ethernet1/3"]}}'

```

####Return Values
On successful execution, the method returns an string with the following message in JSON format: 
"RESTAPI [GET,PUT,POST]  urlpath is successful"
Upon any failure, the method returns an error display string. 

## License

* GPLv3
* Copyright (C) 2017 Lenovo, Inc.

