import tools as tools_mod
import login

def get_unused_hypervisors(env):
    #Returns list of unused hypervisors (no_vms = 0)
    return tools_mod.search_dictionaries("no_vms", 0, env["hosts"])

def get_used_hypervisors(env):
    #Return list of used hypervisors (no_vms > 0)
    return [element for element in env["hosts"] if element["no_vms"] > 0]

def compute_pm_consumption(hosts):
    #vms = env["vms"]
    #hosts = env["hosts"]
    for host in hosts:
        if host["no_vms"] > 0:
            host["power_consumption"] = host["consumption_idle"] + ((host["consumption_max"] - host["consumption_idle"]) * host["util"] / host["capacity"])
        else:
            host["power_consumption"] = 0.0

def clear_hypervisors_util(hosts):
    for host in hosts:
        host["util"] = 0.0
        host["no_vms"] = 0
        host["ram_used"] = 0.0

def compute_pm_util(vms, hosts):
    clear_hypervisors_util(hosts)
    for vm in vms:
         host = tools_mod.search_dictionaries("id", vm["host"], hosts)[0]
         host["util"] = host["util"] + vm["util_abs"]
         host["no_vms"] = host["no_vms"] + 1
         host["ram_used"] = host["ram_used"] + vm["ram"]

def compute_pm_util_avg_abs(env):
    compute_pm_util(env["vms"], env["hosts"])
    cpu_util_sum = 0.0
    no_used_hosts = 0.0
    for host in env["hosts"]:
        if host["no_vms"] > 0:
            cpu_util_sum = cpu_util_sum + host["util"]
            no_used_hosts = no_used_hosts + 1.0
    cpu_util_avg = cpu_util_sum / no_used_hosts
    print "System avg cpu util abs: " + str(cpu_util_avg)
    return cpu_util_avg

def compute_pm_capacity_avg(env):
    capacity_sum = 0.0
    no_used_hosts = 0.0
    for host in env["hosts"]:
        if host["no_vms"] > 0:
            capacity_sum = capacity_sum + host["capacity"]
            no_used_hosts = no_used_hosts + 1.0
    capacity_avg = capacity_sum / no_used_hosts
    return capacity_avg

def compute_pm_util_avg_rel(env):
    return compute_pm_util_avg_abs(env) / compute_pm_capacity_avg(env)

def get_hypervisors():
    nova = login.get_nova_client()
    nova_hypervisors = nova.hypervisors.list()
    hypervisors = []
    for hypervisor in nova_hypervisors:
        print hypervisor._info
        hypervisor_id = hypervisor._info["hypervisor_hostname"]
        hypervisor_running_vms = hypervisor._info["running_vms"]
        hypervisor_util = 0.0
        hypervisor_ram_used = 0.0
        hypervisor_vcpus = hypervisor._info["vcpus"]
        hypervisor_ram = hypervisor._info["memory_mb"]
        #hypervisor_state = hypervisor._info["state"]
        hypervisor_host_ip = hypervisor._info["host_ip"]
        hypervisor_pc = 0.0
	consumption_idle = 150.0
	consumption_max = 300.0
        hypervisors.append({    "id":hypervisor_id,
                                "util":hypervisor_util,
                                "cpu":hypervisor_vcpus,
                                "capacity":hypervisor_vcpus * 100,
                                "ram_capacity":hypervisor_ram,
                                "ram_used":hypervisor_ram_used,
                                #"state":hypervisor_state,
                                "host_ip":hypervisor_host_ip,
                                "power_consumption":hypervisor_pc,
                                "no_vms":hypervisor_running_vms,
				"consumption_idle":consumption_idle,
				"consumption_max":consumption_max})
    return hypervisors
