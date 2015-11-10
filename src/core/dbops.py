import sqlite3
import login
import time
import calendar
from contextlib import closing
import os
import datetime
DATABASE = '/tmp/lmt.db'


def get_ts_ceilometer():
    ts = -1
    ceilometer = login.get_ceilometer_client()
    NO_SAMPLES = 1
    # query = [dict(field='resource', op='eq', value=instance_id)]
    samples = ceilometer.samples.list(meter_name='power', limit=NO_SAMPLES)
    try:
        ts = int((datetime.datetime.strptime(
                 str(samples[0]._info['timestamp']),
                 '%Y-%m-%dT%H:%M:%S.%f')).strftime('%s'))
        # cons_ts = cpu_util_sum += float(samples[0]._info['counter_volume'])
    except:
        print "failed to get timestamp!"
    return ts


def get_ts_local():
    return calendar.timegm(time.gmtime())


def save_cons_rec(ts, simulated=False, description=""):
    # init consolidation record
    ret = -1
    if(simulated):
        username = 'simulation'
        url = tn = ''
    else:
        username = os.environ['OS_USERNAME']
        url = os.environ['OS_AUTH_URL']
        tn = os.environ['OS_TENANT_NAME']

    with closing(sqlite3.connect(DATABASE)) as db:
        db.execute('insert into consolidations(timestamp,\
                    username, url, tenant_name, description)\
                    values(?, ?, ?, ?, ?);', (
            ts, username, url, tn, description))
        db.commit()
        cur = db.execute('select max(id) from consolidations;')
        ret = cur.fetchone()[0]
    return ret


def save_environment(cons_id, ts, env, phase, actions=[]):
    with closing(sqlite3.connect(DATABASE)) as db:
        for action in actions:
            db.execute(
                'insert into actions(\
                 consolidation_id, vm_id, src_host, dst_host, phase)\
                values(?, ?, ?, ?, ?);',
                (cons_id,
                 action["vm_id"],
                 action["src"],
                 action["dst"],
                 phase,
                 ))

        for host in env["hosts"]:
            db.execute(
                'insert into hypervisors(\
                 consolidation_id, hypervisor_id, cpu,\
                 cpu_util, capacity, memory_used,\
                 memory_capacity, power_consumption, phase,\
                 ip, no_vms, consolidation_ts,\
                 consumption_idle, consumption_max)\
                 values (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);',
                (cons_id,
                 host["id"],
                 host["cpu"],
                 host["util"],
                 host["capacity"],
                 host["ram_used"],
                 host["ram_capacity"],
                 host["power_consumption"],
                 phase,
                 host["host_ip"],
                 host["no_vms"],
                 ts,
                 host["consumption_idle"],
                 host["consumption_max"]))
        db.commit()
        print "SAVED!"
