import login


def get_vm_cpu_util(ceilometer, vm_id):
    # print "getting samples for " + vm_id
    NO_SAMPLES = 1
    query = [dict(field='resource', op='eq', value=vm_id)]
    samples = ceilometer.samples.list(
        meter_name='cpu_util', limit=NO_SAMPLES, q=query)
    cpu_util_sum = 0.0
    avg_cpu_util = 0.0
    try:
        for sample in samples:
            cpu_util_sum += float(sample._info['counter_volume'])
        avg_cpu_util = cpu_util_sum / float(len(samples))
    except:
        print "failed to get samples for " + vm_id
    # print vm_id + " " + str(avg_cpu_util)
    return avg_cpu_util


def get_vm(vm_id):
    nova = login.get_nova_client()
    print vm_id
    return nova.servers.find(id=vm_id)


def get_vms():
    nova = login.get_nova_client()
    ceilometer = login.get_ceilometer_client()
    nova_servers = nova.servers.list(search_opts={'all_tenants': True})
    vms = []
    for nova_server in nova_servers:
        # print nova_server._info
        server_id = nova_server._info["id"]
        server_flavor = nova.flavors.get(nova_server._info["flavor"]["id"])
        server_vcpus = server_flavor._info["vcpus"]
        server_ram = server_flavor._info["ram"]
        server_hypervisor = nova_server._info[
            "OS-EXT-SRV-ATTR:hypervisor_hostname"]
        server_state = nova_server._info["OS-EXT-STS:vm_state"]
        server_cpu_util_rel = get_vm_cpu_util(ceilometer, server_id)
        vms.append({"id": server_id,
                    "util": server_cpu_util_rel,
                    "host": server_hypervisor,
                    "vcpus": server_vcpus,
                    "ram": server_ram,
                    "vm_state": server_state,
                    "util_abs": server_cpu_util_rel * server_vcpus})
    return vms
