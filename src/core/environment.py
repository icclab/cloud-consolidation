import math
from random import randint
import host as host_mod
import tools as tools_mod
import virtual_machine as vm_mod


def get_unused_hypervisors(env):
    # Returns list of unused hypervisors (no_vms = 0)
    return tools_mod.search_dictionaries("no_vms", 0, env["hosts"])


def get_used_hypervisors(env):
    # Return list of used hypervisors (no_vms > 0)
    return [element for element in env["hosts"] if element["no_vms"] > 0]


def print_env(env):
    print "Printing VM placement:"
    vms = env["vms"]
    hosts = env["hosts"]
    for host in hosts:
        vms_on_host = tools_mod.search_dictionaries("host", host["id"], vms)
        string = host["id"] + ": " + str(len(vms_on_host)) + "VMs ("
        for vm in vms_on_host:
            string = string + vm["id"] + ", "
        string = string + ")"
        print string


def compute_env_consumption(env):
    host_mod.compute_pm_consumption(env["hosts"])
    total = 0.0
    for host in env["hosts"]:
        print host["id"] + ": " + str(host["power_consumption"])
        if host["no_vms"] > 0:
            total = total + host["power_consumption"]
    return total


def print_env_available_res(env):
    for host in env["hosts"]:
        avail = host_mod.compute_pm_available_res(host)
        print host["id"] + " available absolute value: " + str(avail)


def print_env_available_res_rel(env):
    for host in env["hosts"]:
        avail = host_mod.compute_pm_available_res(
            host) / host["capacity"] * 100
        print host["id"] + " available relative value: " + str(avail) + "percent"


def get_environment():
    environment = {}
    vms = vm_mod.get_vms()
    hypervisors = host_mod.get_hypervisors()
    host_mod.compute_pm_util(vms, hypervisors)
    environment["vms"] = vms
    environment["hosts"] = hypervisors
    return environment


def parse_environment(input_file_path):
    environment = {}
    with open(input_file_path, "r") as f:
        lines = f.readlines()
        lines_array = []
        # print lines
        for line in lines:
            if not line.startswith("#"):
                if line.split():
                    lines_array.append(line.split())
    # print lines_array

    no_hypervisors = len(lines_array[0])
    hypervisors = []
    # setup hypervisors id, idle power consumption, max power consumption
    for i in range(no_hypervisors):
        hypervisors.append(
            {
                "id": "pm" +
                str(i),
                "consumption_max": float(
                    lines_array[0][i]),
                "consumption_idle": float(
                    lines_array[1][i]) *
                float(
                    lines_array[0][i]),
                "capacity": float(
                    lines_array[4][i]),
                "ram_capacity": float(
                    lines_array[5][i]),
                "util": 0.0,
                "ram_used": 0.0,
                "power_consumption": 0.0,
                "no_vms": 0,
                "cpu": -
                1,
                "host_ip": ""})
    # print hypervisors

    no_vms = len(lines_array[2])
    vms = []
    for i in range(no_vms):
        vms.append({"id": "vm" + str(i),
                    "util_abs": float(lines_array[2][i]),
                    "ram": float(lines_array[3][i]),
                    "host": ""})

    pli = 8
    for i in range(no_hypervisors):
        for j in range(no_vms):
            if int(lines_array[pli + i][j]) == 1:
                tools_mod.search_dictionaries(
                    "id", "vm" + str(j), vms)[0]["host"] = "pm" + str(i)

    # print vms
    host_mod.compute_pm_util(vms, hypervisors)
    environment["vms"] = vms
    environment["hosts"] = hypervisors
    return environment


def create_random_environment(no_hosts, no_vms):
    print "Generating random environment " + str(no_hosts) + " hosts, " + str(no_vms) + "vms."
    environment = {}
    vms = []
    hypervisors = []
    for i in range(no_hosts):
        hypervisors.append({"id": "pm" + str(i),
                            "util": 0.0,
                            "cpu": 24,
                            "capacity": 2400,
                            "ram_capacity": 192000,
                            "ram_used": 0.0,
                            "active": True,
                            "consumption_idle": 150.0,
                            "consumption_max": 300.0,
                            "host_ip": ""})
    for i in range(no_vms):
        server_vcpus = math.pow(2, randint(0, 3))
        server_util = randint(0, 100)
        server_util_abs = server_util * server_vcpus
        server_host = "pm" + str(randint(0, no_hosts - 1))
        vms.append({"id": "vm" + str(i),
                    "util": server_util,
                    #"util":100,
                    "host": server_host,
                    #"host":"0",
                    "vcpus": server_vcpus,
                    #"vcpus":8,
                    "ram": server_vcpus * 1024,
                    "util_abs": server_util_abs})
    # print vms, hypervisors
    host_mod.compute_pm_util(vms, hypervisors)
    environment["vms"] = vms
    environment["hosts"] = hypervisors
    return environment
