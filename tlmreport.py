import os
import sys

cnos_tlm_template_str = "feature telemetry\n"
cnos_tlm_template_str = cnos_tlm_template_str + "telemetry controller ip {{item.controllerip}} port {{item.controllerport}} vrf {{item.vrf}}\n"
cnos_tlm_template_str = cnos_tlm_template_str + "telemetry heartbeat enabled interval {{item.hbinterval}}"

tasks = "---\n"
tasks = tasks + "- name: Replace Config CLI command template with values\n"
tasks = tasks + "  template: src=./template/cnos_tlm_common_template.j2 dest=./commands/cnos_tlm_{{ inventory_hostname }}_commands.txt\n"
tasks = tasks + "  with_items: \"{{cnos_tlm_common_template_data}}\"\n\n"
tasks = tasks + "- name: Applying CLI commands on Switches\n"
tasks = tasks + "  cnos_template: host={{ inventory_hostname }} username={{ hostvars[inventory_hostname]['username']}}  password={{ hostvars[inventory_hostname]['password']}} deviceType={{ hostvars[inventory_hostname]['deviceType']}} commandfile=./commands/cnos_tlm_{{ inventory_hostname }}_commands.txt outputfile=./results/cnos_tlm_{{ inventory_hostname }}_output.txt\n"
tasks = tasks + "  with_items: \"{{cnos_tlm_common_template_data}}\"\n"
tasks = tasks + "- name: PUT BST feature\n"
tasks = tasks + "  cnos_restapi:  host={{ inventory_hostname }} username={{ hostvars[inventory_hostname]['username']}}  password={{ hostvars[inventory_hostname]['password']}} outputfile=./results/cnos_tlm_{{ inventory_hostname }}_output.txt  transport='{{item.transport}}' urlpath='{{item.urlpath}}' method='{{item.method}}' jsoninp='{{item.jsoninp}}'\n"
tasks = tasks + "  with_items: \"{{cnos_tlm_bst_feature_data}}\"\n"

def createdirifpresent(DirPath):
   try:
      os.stat(DirPath)
   except:
      os.mkdir(DirPath)       

def inp_to_intflist(str1): 
   list1 = str1.split(",")
   str3 = str(list1)
   str3 = str3.replace('\'','"')
   return str3

def qliststr(str1):
   list1 = str1.split(",")
   str3 = str(list1)
   str3 = str3.replace('\'','')
   return str3


ROOT_DIR = "./"
if __name__ == '__main__':
   print "This script will create ansible role to configure CNOS switch for telemetry reporting \n"
   rolename = raw_input("Enter the rolename: ")
   ContIP = raw_input('Enter Controller IP Address: ')
   ContPort = raw_input('Enter Controller Port(1-65535): ')
   ContVrf = raw_input('Enter Controller Vrf(default/management): ')
   HbInt = raw_input('Enter Heartbeat Interval(1-600): ')

   ReportType=None
   while (ReportType == None):
      ReportType = raw_input('Report Type (Pred_Congestion(1)/Congestion_Detection(2)/Capacity_Planning(3): ') 
      if (ReportType not in ['1', '2', '3']):
          print "Unsupported Report Type"
          ReportType = None 

   RoleDir = ROOT_DIR + rolename

   createdirifpresent(RoleDir)
   CommandDir = RoleDir + "/commands"  
   createdirifpresent(CommandDir)
   ResultDir = RoleDir + "/results"  
   createdirifpresent(ResultDir)
   TasksDir = RoleDir + "/tasks"  
   createdirifpresent(TasksDir)
   TemplateDir = RoleDir + "/template"  
   createdirifpresent(TemplateDir)
   VarsDir = RoleDir + "/vars"  
   createdirifpresent(VarsDir)

   vars = "---\n"
   vars = vars + "cnos_tlm_common_template_data:\n"
   vars = vars + "  - {controllerip: " + ContIP + ", controllerport: " + ContPort + ", vrf: " + ContVrf
   vars = vars + ", hbinterval: " + HbInt + "}\n"
   if (ReportType == '3'):
       collectinterval = raw_input("Enter the periodic report interval in seconds(10-600): ")
       vars = vars + "cnos_tlm_bst_feature_data:\n"
       vars = vars + "  - { transport: https, urlpath: /nos/api/cfg/telemetry/bst/feature, method: PUT, "
       vars = vars + "jsoninp: '{\"bst-enable\" : 1, \"send-async-reports\": 1,"
       vars = vars + "\"trigger-rate-limit\": 1, \"trigger-rate-limit-interval\": 10" 
       vars = vars + ", \"send-snapshot-on-trigger\": 0"
       vars = vars + ", \"collection-interval\": " + collectinterval
       vars = vars + ", \"async-full-report\": 1}'}\n" 
       vars = vars + "cnos_tlm_bst_tk_data:\n"
       vars = vars + "  - { transport: https, urlpath: /nos/api/cfg/telemetry/bst/tracking,"
       vars = vars + " method: PUT, jsoninp: '{\"track-egress-port-service-pool\": 1," 
       vars = vars + "\"track-egress-uc-queue\": 1, \"track-egress-rqe-queue\": 1, \"track-egress-cpu-queue\": 1,"
       vars = vars + "\"track-ingress-port-service-pool\":1, \"track-ingress-service-pool\": 1, \"track-egress-mc-queue\": 1,"
       vars = vars + "\"track-peak-stats\": 0, \"track-ingress-port-priority-group\": 1,"
       vars = vars + "\"track-egress-service-pool\": 1, \"track-device\": 1}'}\n" 
       tasks = tasks + "- name: PUT BST tracking\n"
       tasks = tasks + "  cnos_restapi:  host={{ inventory_hostname }} username={{ hostvars[inventory_hostname]['username']}}  password={{ hostvars[inventory_hostname]['password']}} outputfile=./results/cnos_tlm_{{ inventory_hostname }}_output.txt  use_ssl='{{item.use_ssl}}' urlpath='{{item.urlpath}}' method='{{item.method}}' jsoninp='{{item.jsoninp}}'\n"
       tasks = tasks + "  with_items: \"{{cnos_tlm_bst_tk_data}}\"\n"
   elif (ReportType == '2'):
       print(" The following are the supported congestion report:")
       print(" 1 : Top-port Drops [The top ports that experience highest congestion]")
       print(" 2 : Port Drops [The specified  ports congestion drop  ]")
       print(" 3 : Top-port-queue Drops [The top port queue that are experienceing highest congestion ]")
       print(" 4 : Port Queue Drops [The specified  port queue drops]")
       rpt = raw_input("Select the Report(1/2/3/4): ")
       if (rpt == '1'):
          count = raw_input("Number of ports per report: ")
          interval = raw_input("Periodic interval  of the report in seconds(10-600): ")
          vars = vars + "cnos_tlm_bst_cgsn_data1:\n"
          vars = vars + "  - { transport: https, urlpath: /nos/api/info/telemetry/bst/congestion-drop-counters,"
          vars = vars + " method: POST, jsoninp: '{ \"req-id\" : 2000, \"request-type\" : \"top-drops\","
       vars = vars + " \"request-params\": { \"count\": " + count + " } , \"collection-interval\": "
       vars = vars + interval + "}'}\n"  
       tasks = tasks + "- name: POST BST top-drops cgsn report\n"
       tasks = tasks + "  cnos_restapi:  host={{ inventory_hostname }} username={{ hostvars[inventory_hostname]['username']}}  password={{ hostvars[inventory_hostname]['password']}} outputfile=./results/cnos_tlm_{{ inventory_hostname }}_output.txt  use_ssl='{{item.use_ssl}}' urlpath='{{item.urlpath}}' method='{{item.method}}' jsoninp='{{item.jsoninp}}'\n"
       tasks = tasks + "  with_items: \"{{cnos_tlm_bst_cgsn_data1}}\"\n"
   elif (rpt == '2'):
       vars = vars + "cnos_tlm_bst_cgsn_data2:\n"
       inp = raw_input("Interface List(/All/InterfaceName seperated by comma): ")
       interval = raw_input("Periodic interval  of the report in seconds(10-6000: ")
       intstr = inp_to_intflist(inp)
       vars = vars + "  - { transport: https, urlpath: /nos/api/info/telemetry/bst/congestion-drop-counters,"
       vars = vars + " method: POST, jsoninp: '{ \"req-id\" : 3000, \"request-type\" : \"port-drops\","
       vars = vars + " \"request-params\": { \"interface-list\": " + intstr + " }, \"collection-interval\": "
       vars = vars + interval + "}'}\n"  
       tasks = tasks + "- name: POST BST port-drops cgsn report\n"
       tasks = tasks + "  cnos_restapi:  host={{ inventory_hostname }} username={{ hostvars[inventory_hostname]['username']}}  password={{ hostvars[inventory_hostname]['password']}} outputfile=./results/cnos_tlm_{{ inventory_hostname }}_output.txt  use_ssl='{{item.use_ssl}}' urlpath='{{item.urlpath}}' method='{{item.method}}' jsoninp='{{item.jsoninp}}'\n"
       tasks = tasks + "  with_items: \"{{cnos_tlm_bst_cgsn_data2}}\"\n"
   elif (rpt == '3'):
       vars = vars + "cnos_tlm_bst_cgsn_data3:\n"
       count = raw_input("Number of ports queues per report: ")
       interval = raw_input("Periodic interval of the report in seconds(10-600): ")
       queueType = raw_input("Queue Type(mcast/ucast/all): ")
       vars = vars + "  - { transport: https, urlpath: /nos/api/info/telemetry/bst/congestion-drop-counters,"
       vars = vars + " method: POST, jsoninp: '{ \"req-id\" : 4000, \"request-type\" : \"top-port-queue-drops\","
       vars = vars + " \"request-params\": { \"queue-type\": \"" + queueType + "\" "
       vars = vars + ", \"count\": " + count + " }, \"collection-interval\": "
       vars = vars + interval + "}'}\n"  
       tasks = tasks + "- name: POST BST top-drops cgsn report\n"
       tasks = tasks + "  cnos_restapi:  host={{ inventory_hostname }} username={{ hostvars[inventory_hostname]['username']}}  password={{ hostvars[inventory_hostname]['password']}} outputfile=./results/cnos_tlm_{{ inventory_hostname }}_output.txt  use_ssl='{{item.use_ssl}}' urlpath='{{item.urlpath}}' method='{{item.method}}' jsoninp='{{item.jsoninp}}'\n"
       tasks = tasks + "  with_items: \"{{cnos_tlm_bst_cgsn_data3}}\"\n"
   elif (rpt == '4'):
       vars = vars + "cnos_tlm_bst_cgsn_data4:\n"
       intflist = raw_input("Interface List(/All/InterfaceName separated by comma): ")
       interval = raw_input("Periodic interval of the report in seconds(10-600): ")
       queueType = raw_input("Queue Type(mcast/ucast/all): ")
       queueListstr = raw_input("Queue List (number seperated by comma): ")
       intstr = inp_to_intflist(intflist)
       queueList = qliststr(queueListstr)
       vars = vars + "  - { transport: https, urlpath: /nos/api/info/telemetry/bst/congestion-drop-counters,"
       vars = vars + " method: POST, jsoninp: '{ \"req-id\" : 5000, \"request-type\" : \"port-queue-drops\","
       vars = vars + " \"request-params\": { \"interface-list\": " + intstr + " , \"queue-type\": \"" + queueType + "\" "
       vars = vars + ", \"queue-list\": " + queueList + " }, \"collection-interval\": "
       vars = vars + interval + "}'}\n"  
       tasks = tasks + "- name: POST BST top-drops cgsn report\n"
       tasks = tasks + "  cnos_restapi:  host={{ inventory_hostname }} username={{ hostvars[inventory_hostname]['username']}}  password={{ hostvars[inventory_hostname]['password']}} outputfile=./results/cnos_tlm_{{ inventory_hostname }}_output.txt  use_ssl='{{item.use_ssl}}' urlpath='{{item.urlpath}}' method='{{item.method}}' jsoninp='{{item.jsoninp}}'\n"
       tasks = tasks + "  with_items: \"{{cnos_tlm_bst_cgsn_data4}}\"\n"
       vars = vars + "cnos_tlm_bst_feature_data:\n"
       vars = vars + "  - { transport: https, urlpath: /nos/api/cfg/telemetry/bst/feature, method: PUT, "
       vars = vars + "jsoninp: '{\"bst-enable\" : 1,\"collection-interval\": 0, \"send-async-reports\": 0,"
       vars = vars + "\"trigger-rate-limit\": 1, \"trigger-rate-limit-interval\": 10" 
       vars = vars + ", \"send-snapshot-on-trigger\": 0"
       vars = vars + ", \"async-full-report\": 0}'}\n" 
   elif (ReportType == '1'):
       TrigRateInt = raw_input('Enter the Trigger Rate Limit Interval:') 
       Snapshot = raw_input('Send All Realms in Report(Y/N):')  
       print("The following Realms are supported in CNOS \n    Device: Device Realm \n       ISP: Ingress Service Pool")
       print("      ESP: Egress Service Pool\n     IPSP: Ingress Port Service Pool")
       print("     IPPG: Ingress Port Priority Group\n     EPSP: Egress Port Service Pool")
       print("     EUCQ: Egress Unicast Queue\n     EMCQ: Egress Multicast Queue")
       print("    ECPUQ: Egress CPU Queue\n    ERQEQ: Egress RQE Queue")
       Realm = None
       while (Realm is None):
          Realm = raw_input('Enter the Threshold Realm:')
          if (Realm not in ['Device', 'ISP', 'ESP', 'IPPG', 'IPSP', 'EPSP', 'EUCQ', 'EMCQ', 'ECPUQ', 'ERQEQ']):
               print "Invalid Realm\n"
               Realm = None
       if (Realm == 'Device'):
          Threshold = raw_input("Enter Threshold for Device Realm:")
       elif (Realm == 'ISP'):
          ServicePool = raw_input("Enter Service Pool:")
          Threshold = raw_input("Enter um-share Threshold for the above Service Pool:")
       elif (Realm == 'IPPG'):
          IntfName = raw_input("Enter Interface Name:")
          PGrp = raw_input("Enter Priority Group:")
          Threshold = raw_input("Enter um-share Threshold for the above Priority group and port :")
       elif (Realm == 'IPSP'):
          IntfName = raw_input("Enter Interface Name:")
          ServicePool = raw_input("Enter Service Pool:")
          Threshold = raw_input("Enter um-share Threshold for the above service pool and port :")
       elif (Realm == 'ESP'):
          ServicePool = raw_input("Enter Service Pool:")
          Threshold = raw_input("Enter um-share Threshold for the above Service Pool:")
          mcThreshold = raw_input("Enter mc-share Threshold for the above Service Pool:")
       elif (Realm == 'EPSP'):
          IntfName = raw_input("Enter Interface Name:")
          ServicePool = raw_input("Enter Service Pool:")
          ucThreshold = raw_input("Enter uc-share Threshold for the above service pool and port :")
          Threshold = raw_input("Enter um-share Threshold for the above service pool and port :")
       elif (Realm == 'EUCQ'):
          ucq = raw_input("Enter UC Queue:")
          ucThreshold = raw_input("Enter the Threshold for the above UC Queue:")
       elif (Realm == 'EMCQ'):
          mcq = raw_input("Enter UC Queue:")
          mcThreshold = raw_input("Enter the Threshold for the above MC Queue:")
       elif (Realm == 'ECPUQ'):
          cpuq = raw_input("Enter CPU Queue:")
          Threshold = raw_input("Enter the Threshold for the above CPU Queue:")
       elif (Realm == 'ERQEQ'):
          rqeq = raw_input("Enter RQE Queue:")
          Threshold = raw_input("Enter the Threshold for the above RQE Queue:")
   
       vars = vars + "cnos_tlm_bst_feature_data:\n"
       vars = vars + "  - { transport: https, urlpath: /nos/api/cfg/telemetry/bst/feature, method: PUT, "
       vars = vars + "jsoninp: '{\"bst-enable\" : 1,\"collection-interval\": 0, \"send-async-reports\": 0,"
       vars = vars + "\"trigger-rate-limit\": 1, \"trigger-rate-limit-interval\": " + TrigRateInt
       if (Snapshot == 'Y'):
           vars = vars + ", \"send-snapshot-on-trigger\": 1"
       elif (Snapshot == 'N'):
           vars = vars + ", \"send-snapshot-on-trigger\": 0"
       vars = vars + ", \"async-full-report\": 0}'}\n" 
       vars = vars + "cnos_tlm_bst_tk_data:\n"
       vars = vars + "  - { transport: https, urlpath: /nos/api/cfg/telemetry/bst/tracking,"
       vars = vars + " method: PUT, jsoninp: '{\"track-egress-port-service-pool\": 1," 
       vars = vars + "\"track-egress-uc-queue\": 1, \"track-egress-rqe-queue\": 1, \"track-egress-cpu-queue\": 1,"
       vars = vars + "\"track-ingress-port-service-pool\":1, \"track-ingress-service-pool\": 1, \"track-egress-mc-queue\": 1,"
       vars = vars + "\"track-peak-stats\": 0, \"track-ingress-port-priority-group\": 1,"
       vars = vars + "\"track-egress-service-pool\": 1, \"track-device\": 1}'}\n" 
       vars = vars + "cnos_tlm_bst_threshd_data:\n"
       vars = vars + "  - { transport: https, urlpath: /nos/api/cfg/telemetry/bst/threshold, method: PUT, jsoninp: '{"
       if (Realm == 'Device'):
            vars = vars + "\"realm\": \"device\", \"threshold\": " + Threshold
       elif (Realm == 'ISP'):
            vars = vars + "\"realm\": \"ingress-service-pool\", \"service-pool\": " + ServicePool + ", \"um-share-threshold\": " + Threshold
       elif (Realm == 'ESP'):
            vars = vars + "\"realm\": \"egress-service-pool\", \"service-pool\": " + ServicePool + ", \"um-share-threshold\": " + Threshold + ", \"mc-share-threshold\": " +mcThreshold 
       elif (Realm == 'IPPG'):
            vars = vars + "\"realm\": \"ingress-port-priority-group\", \"priority-group\": " + PGrp + ", \"interface\": \"" + IntfName + "\", \"um-share-threshold\": " + Threshold
       elif (Realm == 'IPSP'):
            vars = vars + "\"realm\": \"ingress-port-service-pool\", \"service-pool\": " + ServicePool + ", \"interface\": \"" + IntfName + "\", \"um-share-threshold\": " + Threshold
       elif (Realm == 'EPSP'):
            vars = vars + "\"realm\": \"egress-port-service-pool\", \"service-pool\": " + ServicePool + ", \"interface\": \"" + IntfName + "\", \"um-share-threshold\": " + Threshold + ", \"uc-share-threshold\": " + ucThreshold 
       elif (Realm == 'EUCQ'):
            vars = vars + "\"realm\": \"egress-uc-queue\", \"queue\": " + ucq + ", \"uc-threshold\": " + ucThreshold
       elif (Realm == 'EMCQ'):
            vars = vars + "\"realm\": \"egress-mc-queue\", \"queue\": " + mcq + ", \"mc-threshold\": " + mcThreshold
       elif (Realm == 'ECPUQ'):
            vars = vars + "\"realm\": \"egress-cpu-queue\", \"queue\": " + cpuq + ", \"cpu-threshold\": " + Threshold
       elif (Realm == 'ERQEQ'):
            vars = vars + "\"realm\": \"egress-rqe-queue\", \"queue\": " + rqeq + ", \"rqe-threshold\": " + Threshold
       vars = vars + "}'}\n"
       tasks = tasks + "- name: PUT BST tracking\n"
       tasks = tasks + "  cnos_restapi:  host={{ inventory_hostname }} username={{ hostvars[inventory_hostname]['username']}}  password={{ hostvars[inventory_hostname]['password']}} outputfile=./results/cnos_tlm_{{ inventory_hostname }}_output.txt  transport='{{item.transport}}' urlpath='{{item.urlpath}}' method='{{item.method}}' jsoninp='{{item.jsoninp}}'\n"
       tasks = tasks + "  with_items: \"{{cnos_tlm_bst_tk_data}}\"\n"
       tasks = tasks + "- name: PUT BST threshold\n"
       tasks = tasks + "  cnos_restapi:  host={{ inventory_hostname }} username={{ hostvars[inventory_hostname]['username']}}  password={{ hostvars[inventory_hostname]['password']}} outputfile=./results/cnos_tlm_{{ inventory_hostname }}_output.txt  transport='{{item.transport}}' urlpath='{{item.urlpath}}' method='{{item.method}}' jsoninp='{{item.jsoninp}}'\n"
       tasks = tasks + "  with_items: \"{{cnos_tlm_bst_threshd_data}}\"\n"
   print vars
   file = open(VarsDir + "/main.yml", "w")
   file.write(vars)
   file.close()
   file = open(TasksDir + "/main.yml", "w")
   file.write(tasks)
   file.close()
   file = open(TemplateDir + "/cnos_tlm_common_template.j2", "w") 
   file.write(cnos_tlm_template_str)
   file.close()
