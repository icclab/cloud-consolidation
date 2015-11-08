import tools as tools_mod
import migration as mig_mod


def consolidate(env):
    vms = env["vms"]
    hosts = env["hosts"]
    sorted_hosts = tools_mod.sort_dictionaries("util", hosts)
    actions = []
    # going through the sorted host
    asc = 0
    for host in sorted_hosts:
        number_of_hosts = len(sorted_hosts)
        vms_on_host = tools_mod.search_dictionaries("host", host["id"], vms)
        sorted_vms_on_host_dsc = reversed(
            tools_mod.sort_dictionaries(
                "util_abs", vms_on_host))
        turn_off = True
        # going through the vms on host
        for vm in sorted_vms_on_host_dsc:
            new_host_found = False
            dsc = number_of_hosts - 1
            # searching for a new host for a VM
            for dest_host in reversed(sorted_hosts):
                if asc < dsc:
                    # found suitable host
                    if dest_host["util"] + vm["util_abs"] <= dest_host["capacity"] and \
                       dest_host["ram_used"] + vm["ram"] <= dest_host["ram_capacity"]:
                        mig_mod.migrate_sim(vm, host, dest_host)
                        actions.append({"action": "live-migrate",
                                        "vm_id": vm["id"],
                                        "src": host["id"],
                                        "dst": dest_host["id"]})
                        break
                    dsc = dsc - 1
                else:
                    break
        asc = asc + 1
    return actions


def split(env):
    vms = env["vms"]
    hosts = env["hosts"]
    sorted_hosts = tools_mod.sort_dictionaries("util", hosts)
    # sorted_hosts_dsc = reversed(sort_dictionaries("util", hosts))

    actions = []
    for host in reversed(sorted_hosts):
        # print "host" + host["id"]
        if host["util"] > host["capacity"]:
            vms_on_host = tools_mod.search_dictionaries(
                "host", host["id"], vms)
            sorted_vms_on_host = tools_mod.sort_dictionaries(
                "util_abs", vms_on_host)
            for vm in sorted_vms_on_host:
                # print len(sorted_vms_on_host)
                # print host["util"]
                if host["util"] <= host["capacity"]:
                    # print  "util: " + str(host["util"])
                    # print  "capacity " + str(host["capacity"])
                    break
                # print "sorted host len: " + str(len(sorted_hosts))
                for dest_host in reversed(sorted_hosts):
                    # print "dest host: " + dest_host["id"]
                    if dest_host["util"] + vm["util_abs"] <= dest_host["capacity"] and \
                       dest_host["ram_used"] + vm["ram"] <= dest_host["ram_capacity"]:
                        # print "dest host fits: " + dest_host["id"]
                        mig_mod.migrate_sim(vm, host, dest_host)
                        actions.append({"action": "live-migrate",
                                        "vm_id": vm["id"],
                                        "src": host["id"],
                                        "dst": dest_host["id"]})
                        break
    return actions
