import json
import sqlite3
from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash, jsonify

DATABASE = '/tmp/lmt.db'

app = Flask(__name__)
app.config.from_object(__name__)

def connect_db():
    return sqlite3.connect(app.config['DATABASE'])

@app.before_request
def before_request():
    g.db = connect_db()

@app.teardown_request
def teardown_request(exception):
    db = getattr(g, 'db', None)
    if db is not None:
        db.close()

def get_consolidations():
    consolidations = []
    cur = g.db.execute('select id, timestamp, username, url, tenant_name\
                            from consolidations;')
    cons_cur = cur.fetchall()
    for con_cur in cons_cur:
        consolidations.append({ "id":con_cur[0],
                                "timestamp":con_cur[1],
                                "username":con_cur[2],
                                "url":con_cur[3],
                                "tenant_name":con_cur[4]})
    return consolidations

def get_actions(cons_id):
    actions = []
    migdict = {};
    cur = g.db.execute('select vm_id, src_host, dst_host, phase\
                            from actions\
                            where consolidation_id=?;',(cons_id,))
    actions_cur = cur.fetchall()
    for action_cur in actions_cur:
	k = action_cur[1]+' '+action_cur[2]
	if k in migdict.keys():
	    migdict[k] = migdict[k]+1
	else:
	    migdict[k] = 1

	for key in migdict.keys():
	    hosts = key.split()
	    actions.append([hosts[0],hosts[1],migdict[k]])
    return actions


def get_hypervisors(cons_id):
    hypervisors = []
    cur = g.db.execute('select id, consolidation_id, hypervisor_id, cpu, cpu_util, capacity,\
                            memory_used, memory_capacity, power_consumption, phase, ip, no_vms\
                            from hypervisors where consolidation_id=?;',(cons_id,))
    cons_cur = cur.fetchall()
    for con_cur in cons_cur:
        hypervisors.append({ "id":con_cur[0],
                                    "consolidation_id":con_cur[1],
                                    "hypervisor_id":con_cur[2],
                                    "cpu":con_cur[3],
                                    "cpu_util":con_cur[4],
                                    "capacity":con_cur[5],
                                    "memory_used":con_cur[6],
                                    "memory_capacity":con_cur[7],
                                    "power_consumption":con_cur[8],
                                    "phase":con_cur[9],
                                    "ip":con_cur[10],
                                    "no_vms":con_cur[11]})
    return hypervisors

def get_hypervisors_consumption(cons_id):
    data = {}
    data["cols"] = []
    data["rows"] = []
    data["cols"].append({"label":"phase", "type":"string"})

    cur = g.db.execute('select distinct(hypervisor_id) \
			    from hypervisors \
			    where consolidation_id=? \
			    order by hypervisor_id;',(cons_id,))
    hypervisors = cur.fetchall()
    for hypervisor in hypervisors:
	data["cols"].append({"label":hypervisor[0],"type":"number"})

    phases = ["init", "consolidate"]
    
    for phase in phases:
	cur = g.db.execute('select hypervisor_id, power_consumption \
				from hypervisors \
				where consolidation_id=? and phase=? \
				order by hypervisor_id;',(cons_id, phase,))
	hypervisors = cur.fetchall()
    
	data["rows"].append({"c":[]})
	data["rows"][-1]["c"].append({"v":phase})
	for hypervisor in hypervisors:
	    data["rows"][-1]["c"].append({"v":hypervisor[1]})
    return data

def get_energy_bardata(cons_id):
    bardata = {}
    cur = g.db.execute('select distinct(hypervisor_id) \
			    from hypervisors \
			    where consolidation_id=?;',(cons_id,))
    hypervisors = cur.fetchall()
    for hypervisor in hypervisors:
        bardata[hypervisor[0]] = []

    phases = ["init", "cons"]
    for phase in phases:
        cur = g.db.execute('select hypervisor_id, power_consumption \
				from hypervisors \
				where consolidation_id=? and phase=? \
				order by hypervisor_id;',(cons_id, phase,))
        hypervisors = cur.fetchall()
        for hypervisor in hypervisors:
	    bardata[hypervisor[0]].append(hypervisor[1])
    print bardata        
    return bardata

def get_energy_piedata(cons_id, phase):
    piedata = {}
    cur = g.db.execute('select distinct(hypervisor_id) \
			    from hypervisors \
			    where consolidation_id=?;',(cons_id,))
    hypervisors = cur.fetchall()
    for hypervisor in hypervisors:
        piedata[hypervisor[0]] = []

    cur = g.db.execute('select hypervisor_id, power_consumption \
			    from hypervisors \
			    where consolidation_id=? and phase=? \
			    order by hypervisor_id;',(cons_id, phase,))
    hypervisors = cur.fetchall()
    for hypervisor in hypervisors:
        piedata[hypervisor[0]].append(hypervisor[1])
    print piedata
    return piedata

@app.route('/')
def show_entries():
    consolidations = get_consolidations()
    print consolidations
    return render_template('show_entries.html', consolidations = consolidations)

@app.route('/show')
def show():
    actions = None
    cons_id = request.args.get('id')
    actions = get_actions(cons_id)
    hypervisors = get_hypervisors(cons_id)
    cons = get_hypervisors_consumption(cons_id)
    bardata = get_energy_bardata(cons_id)
    piedata1 = get_energy_piedata(cons_id, "init")
    piedata2 = get_energy_piedata(cons_id, "cons")
    return render_template('show.html',
				actions = json.dumps(actions), 
				bardata=json.dumps(bardata), 
				piedata1=json.dumps(piedata1),
				piedata2=json.dumps(piedata2), 
				hypervisors = hypervisors, 
				cons = json.dumps(cons, separators=(',', ': ')))

if __name__ == '__main__':
    app.run()
