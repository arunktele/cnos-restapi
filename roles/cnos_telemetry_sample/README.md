# Ansible Role: cnos_telemetry_sample - Configuring Telemetry report on Lenovo CNOS device
---
<add role description below>

This role is an example of using the *cnos_restapi.py* and *cnos_template.py* Lenovo module in the context of CNOS telemetry configuration. This role configures telemetry reports on the Lenovo CNOS devices.

The results of the operation can be viewed in *results* directory.

## Requirements
---
<add role requirements information below>

- Ansible version 2.4 or later ([Ansible installation documentation](http://docs.ansible.com/ansible/intro_installation.html))
- Lenovo switches running CNOS version 10.5.1.0 or later
- restapi must be enabled on the Lenovo switch
- an SSH connection to the Lenovo switch (SSH must be enabled on the network device)

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

###Variables for cnos_restapi in context of cnos telemetry configuration

Variable | Description
--- | ---
`urlpath` | Specifies the url path of the restapi
`use_ssl` | Specifies the transport layer used by the RESTAPI. False choice indicates http plaintext communication over port 8090. True indicates https secured encrypted comminication
`method` | The HTTP method of the restapi request. 
`jsoninp` | Input json dictionary. Used by POST, PUT method to input request paramters.

The restapis  and thier corresponding paramaters used by the cnos_telemetry role is given below.
urlpath | method |  Description
---  |  --- | --- 
/nos/api/cfg/telemetry/bst/feature | PUT | configures  the bst feature for the telemetry report
/nos/api/cfg/telemetry/bst/tracking | PUT | configures the tracking on or off  on the bst realms
/nos/api/cfg/telemetry/bst/threshold | PUT | configures the bst threshold for a bst realm 
/nos/api/info/telemetry/bst/congestion-drop-counters | POST | configure BST congestion drop counters report


####jsoninp parameter for the /nos/api/cfg/telemetry/bst/feature  restapi
Variable | values | Description
--- | --- | ---
bst-enable | 1: Enable BST feature, 0: Disable BST feature | Determines if the BST feature should be active or not  
collection-interval | 1- 600 | Periodic interval with which buffer stats should be send to the collector.
send-async-reports | 1: Asynchronously collect buffer statistics, 0:Disable Asynchronous collection | Asynchronously collect buffer statistics. 
trigger-rate-limit | 1-5 | Maximum number of Trigger reports for configured interval.
trigger-rate-limit-interval | 0, 10-600 | interval during which the number of trigger-reports are rate limited 
send-snapshot-on-trigger | 1: trigger-report contains buffer statistics for all configured realms 0: trigger-report contains buffer statistics  only for the statistic/ counter for which the trigger was raised.|  Determines whether the Agent should send a complete buffer statistics report for all configured realms to the collector
async-full-report | 1: enable full report, 0: disable full report | BST feature asynchronously sends full BST reports to the collector

####jsoninp parameters for the /nos/api/cfg/telemetry/bst/tracking restapi
Variable | values | Description 
--- | --- | ---
track-egress-port-service-pool | 0: Disable Tracking, 1: Enable Tracking | Tracks egress per-port and per-service pool buffers
track-egress-uc-queue | 0: Disable Tracking, 1: Enable Tracking | Tracks per egress Unicast queue buffers
track-egress-rqe-queue | 0: Disable Tracking, 1: Enable Tracking | Tracks per egress RQE buffers
track-egress-cpu-queue | 0: Disable Tracking, 1: Enable Tracking | Tracks per egress CPU buffers
track-ingress-port-service-pool | 0: Disable Tracking, 1: Enable Tracking | Tracks ingress per-port service pool buffers
track-ingress-service-pool | 0: Disable Tracking, 1: Enable Tracking | Tracks ingress per-service pool buffers
track-egress-mc-queue | 0: Disable Tracking, 1: Enable Tracking | Tracks per egress Multicast queue buffers
track-peak-stats | 0: Tracks current buffer count, 1: Tracks peak buffer count | Determines whether ASIC tracks the current buffer usage count or the peak buffer usage
track-ingress-port-priority-group | 0: Disable Tracking, 1: Enable Tracking | Tracks ingress per-port priority group buffers
track-egress-service-pool | 0: Disable Tracking, 1: Enable Tracking | Tracks per egress service pool buffers
track-device | 0: Disable Tracking, 1: Enable Tracking | Tracks per device buffers

####jsoninp parameter for the /nos/api/cfg/telemetry/bst/threshold restapi

The jsoninp comprises od realm, index1/index1 and index2, threshold parameter.

The possible values for these are given below

Realm | Index 1 | Index 2 | Values in the realm report
--- | --- | --- | ---
ingress-port-priority-group | interface	| priority-group | um-share-threshold
ingress-port-service-pool | interface | service-pool | um-share-threshold
ingress-service-pool | service-pool | | um-share-threshold
egress-port-service-pool | interface | service-pool | uc-share-threshold,  um-share-threshold
egress-service-pool | service-pool | | um-share-threshold,  mc-share-threshold
egress-rqe-queue | queue | | rqe-threshold
egress-cpu-queue | queue | | cpu-threshold
egress-mc-queue	 | queue | | mc-threshold
egress-uc-queue	 | queue | | uc-threshold
device| | |	Threshold

The permitted values for the indexs are given below
Index | Values | Description
--- | --- | ---
rqe-threshold, cpu-threshold, um-threshold, uc-threshold, mc-threshold | 1-100 | Threshold values in percentages
queue | integer | the queue  number with respect to the realm
service-pool | integer(0-1) | Service pool
priority-group | integer (0-7 ) Priority group
interface | string | Physical port interface of the device
 
####jsoninp parameters for the /nos/api/info/telemetry/bst/congestion-drop-counters restapi

The elements of the jsoninp consist of request-type, collection-interval and request-param
Variable | values | Description 
--- | --- | ---
request-type | "top-drops" : Ports suffering maximum congestion in the switch and the associated drop counters, “top-port-queue-drops” : Top port-queue level drop-counters in the switch, “port-drops” : Per-port total drop counters,  “port-queue-drops” : Port-queue level drop-counters | Indicates the specific set of drop counters being requested
collection-interval | 0, 10 - 3600 | Determines the period with which the congestion drop counters are collected from the ASIC and reported to the client
request-param | count : Number of records required in the report, ifname-list : List of interface names, queue-type : Type of queue requested,  Queue-list : List of the queue ids | Request Parameters for the congestion drop counters

The request-param is a dictionary of  the following
Variable | values | Description 
--- | --- | ---
count |  integer | Number of records requested
ifname-list | list | List of interfaces
queue-type | 'ucast': unicast queue, 'mcast': multicast queue, 'all' : Both unicast and multicast queue
queue-list | list of queues | list of queue ids

###The cnos_template used by the cnos_telemetry role is given below

The following is the contents of the common telemetry template
feature telemetry
telemetry controller ip {{item.controllerip}} port {{item.controllerport}} vrf {{item.vrf}}
telemetry heartbeat enabled interval {{item.hbinterval}}

If the user like to disable hearbeat the template to disable hearbeat is given below
feature telemetry
telemetry controller ip {{item.controllerip}} port {{item.controllerport}} vrf {{item.vrf}}
telemetry heartbeat disable

Variable | Description
---   | ---
`controllerip` | controller ip address
`controllerport` | controller's listening tcp port. The parameter type is Integer. 
`vrf` | vrf of the configured controller. Vrf can either be  default or management. The parameter type is string.
`hbinterval` | heartbeat interval in seconds. Values range from 1 to 600.  


## Dependencies
---
<add dependencies information below>

- username.iptables - Configures the firewall and blocks all ports except those needed for http(port=8090) or https(port=443) server and ssh server.
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
ansible-playbook cnos_telemetry_sample.yml -vvv
```

`-vvv` is an optional verbos command that helps identify what is happening during playbook execution. The playbook for each role is located in the main directory of the solution.

```
- name: Module to configure telemetry reports
   hosts: cnos_telemetry_sample
   gather_facts: no
   connection: local
   roles:
    - cnos_telemetry_sample
```


## License
---
<add license information below>
Copyright (C) 2017 Lenovo, Inc.

This Ansible Role is distributed WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  

See the [GNU General Public License](http://www.gnu.org/licenses/) for more details.
