import virtual_machine as vm_mod


def print_actions(actions):
    print "Printing actions taken:"
    for action in actions:
        print action["vm_id"] + ": " + action["src"] + " -> " + action["dst"]


def migrate_sim(vm, src_host, dest_host):
    src_host["util"] = src_host["util"] - vm["util_abs"]
    src_host["no_vms"] = src_host["no_vms"] - 1
    src_host["ram_used"] = src_host["ram_used"] - vm["ram"]
    dest_host["util"] = dest_host["util"] + vm["util_abs"]
    dest_host["no_vms"] = dest_host["no_vms"] + 1
    dest_host["ram_used"] = dest_host["ram_used"] + vm["ram"]
    vm["host"] = dest_host["id"]
    # vm["dest_host"] = dest_host["id"]
    # print vm["id"] + ": " + src_host["id"] + " -> " + dest_host["id"]


def exec_migration(action):
    vm = vm_mod.get_vm(action["vm_id"])
    if(action["action"] == "live-migrate"):
        vm.live_migrate(host=action["dst"])
