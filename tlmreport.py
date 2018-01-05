import os
import sys
import requests

all_ifs = '/nos/api/cfg/interface'

def form_url(conn, url):
   url = conn.transport+'://' + conn.ip + ':' + conn.port + url
   return url

def form_hdr(conn):
   hdr = dict()
   tmp_ckie = 'auth_cookie='+conn.cookie + ';user='+ conn.user +'; Max-Age=3600; Path=/'
   hdr['Cookie'] = tmp_ckie
   hdr['Content-type'] = 'application/json'
   return hdr

class Connection:
     def __init__(self,params):
         self.transport = params['transport']
         self.port = params['port']
         self.ip = params['ip']
         self.user = params['user']
         self.password = params['password']
         self.cookie = ''
         self.url = self.transport + '://' + self.ip + ':' + self.port + '/nos/api/login/'
#         print(self.url, self.user, self.password)

         # Step 1 - Login and get the auth cookie
         ret = requests.get(self.url,auth=(self.user, self.password),verify=False, timeout=20)
         self.cookie=ret.cookies['auth_cookie']

         # Step 2 - Login with valid cookie
         tmp_ckie = 'auth_cookie=' + self.cookie + ';user='+ self.user +'; Max-Age=3600; Path=/'
         self.hdr=dict()
         self.hdr['Cookie']=tmp_ckie

         ret = requests.get(self.url, headers=self.hdr, auth=(self.user, self.password),verify=False)
         self.cookie=ret.cookies['auth_cookie']
         self.hdr['Content-Type']='application/json'


class Interfaces:
    #This API will get properties names of all interfaces
    def get_interfaces(self, conn):
        '''
        API's description: This API will get names of all ethernet interfaces
        Mandatory arguments: None
        Output: List or dictionary of interface properties
        '''
        tmp_url=form_url(conn, all_ifs)
        hdr = form_hdr(conn)
        ret = requests.get(tmp_url, headers=hdr, auth=(conn.user, conn.password), verify=False, timeout=10)
        report = ret.json()
        interfaces = []
        for obj in report:
           interfaces.append(obj.get('if_name'))
        return interfaces

    #This API will get names of all link up ethernet interface
    def get_link_up_interfaces(self, conn):
        '''
        API's description: This API will get names of link up ethernet interfaces
        Mandatory arguments: None
        Output: List or dictionary of interface properties
        '''
        tmp_url=form_url(conn, all_ifs)
        hdr = form_hdr(conn)
        ret = requests.get(tmp_url, headers=hdr, auth=(conn.user, conn.password), verify=False, timeout=10)
        report = ret.json()
        interfaces = []
        for obj in report:
           if obj.get('oper_state') == 'up':
             interfaces.append(obj.get('if_name'))
        return interfaces


def writeoutput(buf, bufFile, append):
   if (append == 'Y'):
       file = open(bufFile, "a") 
   else:
       file = open(bufFile, "w") 
   file.write(buf)
   file.close()

def userinput_integer(string1, min, max):
   while True:
     res = raw_input(string1)
     if res.isdigit() and min<= int(res) <= max:
         break;
     print "Error Invalid Input"
   return res

def userinput_string_yn(string1):
   while True:
     res = raw_input(string1)
     if res == 'Y' or res == 'N':
         break;
     print "Invalid choice"
   return res
    

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

def Controller_info_configuration(TemplateDir, TaskDir, VarsDir, append):
   tasks = "- name: Replace Config CLI command template with values\n"
   tasks = tasks + "  template: src=./template/cnos_tlm_common_template.j2 dest=./commands/cnos_tlm_{{ inventory_hostname }}_commands.txt\n"
   tasks = tasks + "  with_items: \"{{cnos_tlm_common_template_data}}\"\n\n"
   tasks = tasks + "- name: Applying CLI commands on Switches\n"
   tasks = tasks + "  cnos_template: host={{ inventory_hostname }} username={{ hostvars[inventory_hostname]['username']}}  password={{ hostvars[inventory_hostname]['password']}} deviceType={{ hostvars[inventory_hostname]['deviceType']}} commandfile=./commands/cnos_tlm_{{ inventory_hostname }}_commands.txt outputfile=./results/cnos_tlm_{{ inventory_hostname }}_output.txt\n"
   tasks = tasks + "  with_items: \"{{cnos_tlm_common_template_data}}\"\n"
   cnos_tlm_template_str = "feature telemetry\n"
   cnos_tlm_template_str = cnos_tlm_template_str + "telemetry controller ip {{item.controllerip}} port {{item.controllerport}} vrf {{item.vrf}}\n"
   ContIP = raw_input('Enter Controller IP Address(xx.xx.xx.xx): ')
   ContPort = userinput_integer('Enter Controller Port(1-65535): ', 1, 65535)
   while True:
       ContVrf = raw_input('Enter Controller Vrf(default/management): ')
       if (ContVrf in ['default', 'management']):
          break
       else:
          print "incorrect choice\n"
   vars = "cnos_tlm_common_template_data:\n"
   vars = vars + "  - {controllerip: " + ContIP + ", controllerport: " + ContPort + ", vrf: " + ContVrf + " }\n"
   writeoutput(cnos_tlm_template_str, (TemplateDir + "/cnos_tlm_common_template.j2"), "N") 
   writeoutput(vars, (VarsDir + "/main.yml"), append)
   writeoutput(tasks, (TasksDir + "/main.yml"), append)
    
def Heartbeat_configuration(TemplateDir, TaskDir, VarsDir, append):
   tasks = "- name: Replace Config CLI command template with values\n"
   tasks = tasks + "  template: src=./template/cnos_tlm_common_template1.j2 dest=./commands/cnos_tlm_{{ inventory_hostname }}_commands.txt\n"
   tasks = tasks + "  with_items: \"{{cnos_tlm_common_template_data1}}\"\n\n"
   tasks = tasks + "- name: Applying CLI commands on Switches\n"
   tasks = tasks + "  cnos_template: host={{ inventory_hostname }} username={{ hostvars[inventory_hostname]['username']}}  password={{ hostvars[inventory_hostname]['password']}} deviceType={{ hostvars[inventory_hostname]['deviceType']}} commandfile=./commands/cnos_tlm_{{ inventory_hostname }}_commands.txt outputfile=./results/cnos_tlm_{{ inventory_hostname }}_output.txt\n"
   tasks = tasks + "  with_items: \"{{cnos_tlm_common_template_data1}}\"\n"
   cnos_tlm_template_str = "telemetry heartbeat enabled interval {{item.hbinterval}}"
   HbInt = userinput_integer('Enter Heartbeat Interval(1-600): ', 1, 600)
   vars = "cnos_tlm_common_template_data1:\n"
   vars = vars + "  - {hbinterval: " + HbInt + "}\n"
   writeoutput(cnos_tlm_template_str, (TemplateDir + "/cnos_tlm_common_template1.j2"), "N") 
   writeoutput(vars, (VarsDir + "/main.yml"), append)
   writeoutput(tasks, (TasksDir + "/main.yml"), append)
   
def configure_capacity_planning(TaskDir, VarsDir, append): 
   collectinterval = userinput_integer("Enter the periodic report interval in seconds(10-600): ", 10, 600)
   vars = "cnos_tlm_bst_feature_data:\n"
   vars = vars + "  - { use_ssl: True, urlpath: /nos/api/cfg/telemetry/bst/feature, method: PUT, "
   vars = vars + "jsoninp: '{\"bst-enable\" : 1, \"send-async-reports\": 1,"
   vars = vars + "\"trigger-rate-limit\": 1, \"trigger-rate-limit-interval\": 10" 
   vars = vars + ", \"send-snapshot-on-trigger\": 0"
   vars = vars + ", \"collection-interval\": " + collectinterval
   vars = vars + ", \"async-full-report\": 1}'}\n" 
   vars = vars + "cnos_tlm_bst_tk_data:\n"
   vars = vars + "  - { use_ssl: True, urlpath: /nos/api/cfg/telemetry/bst/tracking,"
   vars = vars + " method: PUT, jsoninp: '{\"track-egress-port-service-pool\": 1," 
   vars = vars + "\"track-egress-uc-queue\": 1, \"track-egress-rqe-queue\": 1, \"track-egress-cpu-queue\": 1,"
   vars = vars + "\"track-ingress-port-service-pool\":1, \"track-ingress-service-pool\": 1, \"track-egress-mc-queue\": 1,"
   vars = vars + "\"track-peak-stats\": 0, \"track-ingress-port-priority-group\": 1,"
   vars = vars + "\"track-egress-service-pool\": 1, \"track-device\": 1}'}\n" 
   tasks = "- name: PUT BST feature\n"
   tasks = tasks + "  cnos_restapi:  host={{ inventory_hostname }} username={{ hostvars[inventory_hostname]['username']}}  password={{ hostvars[inventory_hostname]['password']}} outputfile=./results/cnos_tlm_{{ inventory_hostname }}_output.txt  use_ssl='{{item.use_ssl}}' urlpath='{{item.urlpath}}' method='{{item.method}}' jsoninp='{{item.jsoninp}}'\n"
   tasks = tasks + "  with_items: \"{{cnos_tlm_bst_feature_data}}\"\n"
   tasks = tasks + "- name: PUT BST tracking\n"
   tasks = tasks + "  cnos_restapi:  host={{ inventory_hostname }} username={{ hostvars[inventory_hostname]['username']}}  password={{ hostvars[inventory_hostname]['password']}} outputfile=./results/cnos_tlm_{{ inventory_hostname }}_output.txt  use_ssl='{{item.use_ssl}}' urlpath='{{item.urlpath}}' method='{{item.method}}' jsoninp='{{item.jsoninp}}'\n"
   tasks = tasks + "  with_items: \"{{cnos_tlm_bst_tk_data}}\"\n"
   writeoutput(vars, (VarsDir + "/main.yml"), append)
   writeoutput(tasks, (TasksDir + "/main.yml"), append)

def configure_congestion_detection(TaskDir, VarsDir, append):
   print(" The following are the supported congestion report:")
   print(" 1 : Top-port Drops [The top ports that experience highest congestion]")
   print(" 2 : Port Drops [The specified  ports congestion drop  ]")
   print(" 3 : Top-port-queue Drops [The top port queue that are experienceing highest congestion ]")
   print(" 4 : Port Queue Drops [The specified  port queue drops]")
   rpt = raw_input("Select the Report(1/2/3/4): ")
   if (rpt == '1'):
      count = userinput_integer("Number of ports per report: ", 1, 20)
      interval = userinput_integer("Periodic interval  of the report in seconds(10-600): ", 10, 600)
      vars = "cnos_tlm_bst_cgsn_data1:\n"
      vars = vars + "  - { use_ssl: True, urlpath: /nos/api/info/telemetry/bst/congestion-drop-counters,"
      vars = vars + " method: POST, jsoninp: '{ \"req-id\" : 2000, \"request-type\" : \"top-drops\","
      vars = vars + " \"request-params\": { \"count\": " + count + " } , \"collection-interval\": "
      vars = vars + interval + "}'}\n"  
      tasks = "- name: POST BST top-drops cgsn report\n"
      tasks = tasks + "  cnos_restapi:  host={{ inventory_hostname }} username={{ hostvars[inventory_hostname]['username']}}  password={{ hostvars[inventory_hostname]['password']}} outputfile=./results/cnos_tlm_{{ inventory_hostname }}_output.txt  use_ssl='{{item.use_ssl}}' urlpath='{{item.urlpath}}' method='{{item.method}}' jsoninp='{{item.jsoninp}}'\n"
      tasks = tasks + "  with_items: \"{{cnos_tlm_bst_cgsn_data1}}\"\n"
   elif (rpt == '2'):
      vars = "cnos_tlm_bst_cgsn_data2:\n"
      inp = raw_input("Interface List(AllUP/InterfaceName seperated by comma): ")
      if inp == "AllUP":
          switch_ip = raw_input("Enter the switch IP(xx.xx.xx.xx):")
          ssl = userinput_string_yn("https connection(Y/N): ") 
          params = dict()
          params['ip'] = switch_ip
          if (ssl is 'Y'):
             params['transport'] = 'https'
             params['port'] = '443'
          elif (ssl is 'N'):
             params['transport'] = 'http'
             params['port'] = '8090'
          params['user'] = 'admin'
          params['password'] = 'admin'
          conn = Connection(params)
          ifinfo = Interfaces()
          ifacelist = ifinfo.get_link_up_interfaces(conn)
          intstr = str(ifacelist)
          intstr = intstr.replace('u','')
          intstr = intstr.replace('\'','\"')
      else:
          intstr = inp_to_intflist(inp)
      interval = userinput_integer("Periodic interval  of the report in seconds(10-600): ", 10, 600)
      vars = vars + "  - { use_ssl: True, urlpath: /nos/api/info/telemetry/bst/congestion-drop-counters,"
      vars = vars + " method: POST, jsoninp: '{ \"req-id\" : 3000, \"request-type\" : \"port-drops\","
      vars = vars + " \"request-params\": { \"interface-list\": " + intstr + " }, \"collection-interval\": "
      vars = vars + interval + "}'}\n" 
      tasks = "- name: POST BST port-drops cgsn report\n"
      tasks = tasks + "  cnos_restapi:  host={{ inventory_hostname }} username={{ hostvars[inventory_hostname]['username']}}  password={{ hostvars[inventory_hostname]['password']}} outputfile=./results/cnos_tlm_{{ inventory_hostname }}_output.txt  use_ssl='{{item.use_ssl}}' urlpath='{{item.urlpath}}' method='{{item.method}}' jsoninp='{{item.jsoninp}}'\n"
      tasks = tasks + "  with_items: \"{{cnos_tlm_bst_cgsn_data2}}\"\n"
   elif (rpt == '3'):
      vars = "cnos_tlm_bst_cgsn_data3:\n"
      count = userinput_integer("Number of ports queues per report: ", 1, 20)
      interval = userinput_integer("Periodic interval of the report in seconds(10-600): ", 10, 600)
      queueType = raw_input("Queue Type(mcast/ucast/all): ")
      vars = vars + "  - { use_ssl: True, urlpath: /nos/api/info/telemetry/bst/congestion-drop-counters,"
      vars = vars + " method: POST, jsoninp: '{ \"req-id\" : 4000, \"request-type\" : \"top-port-queue-drops\","
      vars = vars + " \"request-params\": { \"queue-type\": \"" + queueType + "\" "
      vars = vars + ", \"count\": " + count + " }, \"collection-interval\": "
      vars = vars + interval + "}'}\n"  
      tasks = tasks + "- name: POST BST top-drops cgsn report\n"
      tasks = tasks + "  cnos_restapi:  host={{ inventory_hostname }} username={{ hostvars[inventory_hostname]['username']}}  password={{ hostvars[inventory_hostname]['password']}} outputfile=./results/cnos_tlm_{{ inventory_hostname }}_output.txt  use_ssl='{{item.use_ssl}}' urlpath='{{item.urlpath}}' method='{{item.method}}' jsoninp='{{item.jsoninp}}'\n"
      tasks = tasks + "  with_items: \"{{cnos_tlm_bst_cgsn_data3}}\"\n"
   elif (rpt == '4'):
      vars = "cnos_tlm_bst_cgsn_data4:\n"
      inp = raw_input("Interface List(AllUP/InterfaceName separated by comma): ")
      if inp == "AllUP":
          switch_ip = raw_input("Enter the switch IP(xx.xx.xx.xx):")
          ssl = userinput_string_yn("https connection(Y/N): ") 
          params = dict()
          params['ip'] = switch_ip
          if (ssl is 'Y'):
             params['transport'] = 'https'
             params['port'] = '443'
          elif (ssl is 'N'):
             params['transport'] = 'http'
             params['port'] = '8090'
          params['user'] = 'admin'
          params['password'] = 'admin'
          conn = Connection(params)
          ifinfo = Interfaces()
          ifacelist = ifinfo.get_link_up_interfaces(conn)
          intstr = str(ifacelist)
          intstr = intstr.replace('u','')
          intstr = intstr.replace('\'','\"')
      else:
          intstr = inp_to_intflist(inp)
      interval = userinput_integer("Periodic interval of the report in seconds(10-600): ", 10, 600)
      queueType = raw_input("Queue Type(mcast/ucast/all): ")
      queueListstr = raw_input("Queue List (number seperated by comma): ")
      queueList = qliststr(queueListstr)
      vars = vars + "  - { use_ssl: True, urlpath: /nos/api/info/telemetry/bst/congestion-drop-counters,"
      vars = vars + " method: POST, jsoninp: '{ \"req-id\" : 5000, \"request-type\" : \"port-queue-drops\","
      vars = vars + " \"request-params\": { \"interface-list\": " + intstr + " , \"queue-type\": \"" + queueType + "\" "
      vars = vars + ", \"queue-list\": " + queueList + " }, \"collection-interval\": "
      vars = vars + interval + "}'}\n"  
      tasks = tasks + "- name: POST BST top-drops cgsn report\n"
      tasks = tasks + "  cnos_restapi:  host={{ inventory_hostname }} username={{ hostvars[inventory_hostname]['username']}}  password={{ hostvars[inventory_hostname]['password']}} outputfile=./results/cnos_tlm_{{ inventory_hostname }}_output.txt  use_ssl='{{item.use_ssl}}' urlpath='{{item.urlpath}}' method='{{item.method}}' jsoninp='{{item.jsoninp}}'\n"
      tasks = tasks + "  with_items: \"{{cnos_tlm_bst_cgsn_data4}}\"\n"
      vars = vars + "cnos_tlm_bst_feature_data:\n"
      vars = vars + "  - { use_ssl: True, urlpath: /nos/api/cfg/telemetry/bst/feature, method: PUT, "
      vars = vars + "jsoninp: '{\"bst-enable\" : 1,\"collection-interval\": 0, \"send-async-reports\": 0,"
      vars = vars + "\"trigger-rate-limit\": 1, \"trigger-rate-limit-interval\": 10" 
      vars = vars + ", \"send-snapshot-on-trigger\": 0"
      vars = vars + ", \"async-full-report\": 0}'}\n" 
   writeoutput(vars, (VarsDir + "/main.yml"), append)
   writeoutput(tasks, (TasksDir + "/main.yml"), append)

def configure_threshold(TasksDir, VarsDir, append, num):
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
      Threshold = userinput_integer("Enter Threshold for Device Realm(1-100):", 1, 100)
   elif (Realm == 'ISP'):
      ServicePool = userinput_integer("Enter Service Pool (0-1):", 0, 1)
      Threshold = userinput_integer("Enter um-share Threshold for the above Service Pool(1-100):", 1, 100)
   elif (Realm == 'IPPG'):
      IntfName = raw_input("Enter Interface Name:")
      PGrp = userinput_integer("Enter Priority Group(0-7):", 0, 7)
      Threshold = userinput_integer("Enter um-share Threshold for the above Priority group and port(1-100) :", 1, 100)
   elif (Realm == 'IPSP'):
      IntfName = raw_input("Enter Interface Name:")
      ServicePool = userinput_integer("Enter Service Pool(0-1):", 0, 1)
      Threshold = userinput_integer("Enter um-share Threshold for the above service pool and port (1-100):", 1, 100)
   elif (Realm == 'ESP'):
      ServicePool = userinput_integer("Enter Service Pool(0-1):", 0, 1)
      Threshold = userinput_integer("Enter um-share Threshold for the above Service Pool(1-100):", 1, 100)
      mcThreshold = userinput_integer("Enter mc-share Threshold for the above Service Pool(1-100):", 1, 100)
   elif (Realm == 'EPSP'):
      IntfName = raw_input("Enter Interface Name:")
      ServicePool = userinput_integer("Enter Service Pool(0-1):", 0, 1)
      ucThreshold = userinput_integer("Enter uc-share Threshold for the above service pool and port (1-100):", 1, 100)
      Threshold = userinput_integer("Enter um-share Threshold for the above service pool and port (1-100):", 1, 100)
   elif (Realm == 'EUCQ'):
      ucq = raw_input("Enter UC Queue:")
      ucThreshold = userinput_integer("Enter the Threshold for the above UC Queue(1-100):", 1, 100)
   elif (Realm == 'EMCQ'):
      mcq = raw_input("Enter MC Queue:")
      mcThreshold = userinput_integer("Enter the Threshold for the above MC Queue(1-100):", 1, 100)
   elif (Realm == 'ECPUQ'):
      cpuq = raw_input("Enter CPU Queue:")
      Threshold = userinput_integer("Enter the Threshold for the above CPU Queue(1-100):", 1, 100)
   elif (Realm == 'ERQEQ'):
      rqeq = raw_input("Enter RQE Queue:")
      Threshold = userinput_integer("Enter the Threshold for the above RQE Queue(1-100):", 1, 100)
   vars = "cnos_tlm_bst_threshd_data" + str(num) + ":\n"
   vars = vars + "  - { use_ssl: True, urlpath: /nos/api/cfg/telemetry/bst/threshold, method: PUT, jsoninp: '{"
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
   tasks = "- name: PUT BST threshold\n"
   tasks = tasks + "  cnos_restapi:  host={{ inventory_hostname }} username={{ hostvars[inventory_hostname]['username']}}  password={{ hostvars[inventory_hostname]['password']}} outputfile=./results/cnos_tlm_{{ inventory_hostname }}_output.txt  use_ssl='{{item.use_ssl}}' urlpath='{{item.urlpath}}' method='{{item.method}}' jsoninp='{{item.jsoninp}}'\n"
   tasks = tasks + "  with_items: \"{{cnos_tlm_bst_threshd_data" + str(num) + "}}\"\n"
   writeoutput(vars, (VarsDir + "/main.yml"), append)
   writeoutput(tasks, (TasksDir + "/main.yml"), append)

def configure_pred_congestion(TasksDir, VarsDir, append):

   TrigRateInt = userinput_integer('Enter the Trigger Rate Limit Interval:', 1, 600) 
   Snapshot = userinput_string_yn('Send All Realms in Report(Y/N):')  

   if (Snapshot == 'Y'):
       vars =  ", \"send-snapshot-on-trigger\": 1"
   elif (Snapshot == 'N'):
       vars = ", \"send-snapshot-on-trigger\": 0"
   vars = vars + "cnos_tlm_bst_feature_data:\n"
   vars = vars + "  - { use_ssl: True, urlpath: /nos/api/cfg/telemetry/bst/feature, method: PUT, "
   vars = vars + "jsoninp: '{\"bst-enable\" : 1,\"collection-interval\": 0, \"send-async-reports\": 0,"
   vars = vars + "\"trigger-rate-limit\": 1, \"trigger-rate-limit-interval\": " + TrigRateInt
   vars = vars + ", \"async-full-report\": 0}'}\n" 
   vars = vars + "cnos_tlm_bst_tk_data:\n"
   vars = vars + "  - { use_ssl: True, urlpath: /nos/api/cfg/telemetry/bst/tracking,"
   vars = vars + " method: PUT, jsoninp: '{\"track-egress-port-service-pool\": 1," 
   vars = vars + "\"track-egress-uc-queue\": 1, \"track-egress-rqe-queue\": 1, \"track-egress-cpu-queue\": 1,"
   vars = vars + "\"track-ingress-port-service-pool\":1, \"track-ingress-service-pool\": 1, \"track-egress-mc-queue\": 1,"
   vars = vars + "\"track-peak-stats\": 0, \"track-ingress-port-priority-group\": 1,"
   vars = vars + "\"track-egress-service-pool\": 1, \"track-device\": 1}'}\n" 
   tasks = "- name: PUT BST tracking\n"
   tasks = tasks + "  cnos_restapi:  host={{ inventory_hostname }} username={{ hostvars[inventory_hostname]['username']}}  password={{ hostvars[inventory_hostname]['password']}} outputfile=./results/cnos_tlm_{{ inventory_hostname }}_output.txt  use_ssl='{{item.use_ssl}}' urlpath='{{item.urlpath}}' method='{{item.method}}' jsoninp='{{item.jsoninp}}'\n"
   tasks = tasks + "  with_items: \"{{cnos_tlm_bst_tk_data}}\"\n"
   writeoutput(vars, (VarsDir + "/main.yml"), append)
   writeoutput(tasks, (TasksDir + "/main.yml"), append)
   num = 0
   while True:
       configure_threshold(TasksDir, VarsDir, append, num)
       option = userinput_string_yn(" Want to configure more thresholds (Y/N)")
       num = num + 1
       if (option == 'N'): 
            break

ROOT_DIR = "./"
if __name__ == '__main__':
   print "This script will create ansible role to configure CNOS switch for telemetry reporting \n"
   rolename = raw_input("Enter the rolename: ")
   RoleDir = ROOT_DIR + rolename
   CommandDir = RoleDir + "/commands"  
   ResultDir = RoleDir + "/results"  
   TasksDir = RoleDir + "/tasks"  
   TemplateDir = RoleDir + "/template"  
   VarsDir = RoleDir + "/vars"  
   createdirifpresent(RoleDir)
   createdirifpresent(CommandDir)
   createdirifpresent(ResultDir)
   createdirifpresent(TasksDir)
   createdirifpresent(TemplateDir)
   createdirifpresent(VarsDir)

   append = userinput_string_yn("Do you want to append to the existing configuration  (Y/N): ")
  
   if (append == 'N'):
      tasks = "---\n"
      writeoutput(tasks, (VarsDir + "/main.yml"), append)
      writeoutput(tasks, (TasksDir + "/main.yml"), append)
      append = 'Y'

   option = userinput_string_yn("Do you want to configure controller info (Y/N): ")
   if (option == 'Y'):
      Controller_info_configuration(TemplateDir, TasksDir, VarsDir, append)
   option = userinput_string_yn("Do you want to configure heartbeat interval (Y/N): ")
   if (option == 'Y'):
      Heartbeat_configuration(TemplateDir, TasksDir, VarsDir, append)

   ReportType=None
   while True:
      ReportType = raw_input('Report Type (Pred_Congestion(1)/Congestion_Detection(2)/Capacity_Planning(3): ') 
      if (ReportType not in ['1', '2', '3']):
          print "Unsupported Report Type"
          ReportType = None 
      else:
          break

   if (ReportType == '3'):
       configure_capacity_planning(TasksDir, VarsDir, append)
   elif (ReportType == '2'):
       configure_congestion_detection(TasksDir, VarsDir, append)
   elif (ReportType == '1'):
       configure_pred_congestion(TasksDir, VarsDir, append)
