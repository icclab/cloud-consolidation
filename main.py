import sys
import dbops
import environment as env_mod
import host as host_mod
import cons_core as cc_mod
import argparse

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', help='input file containing environment specs', nargs=1)
    parser.add_argument('-r', help='generates random environment with specified number of hosts [0] and VMs [1]', nargs=2)
    args = parser.parse_args()

    if args.r:
	env = env_mod.create_random_environment(int(args.r[0]),int(args.r[1]))
    elif args.f:
	env = env_mod.parse_environment(args.f[0])
    else:
	env = env_mod.get_environment()

    ts = dbops.get_ts_local()
    cons_id = dbops.save_cons_rec(ts, True)
    actions = []
 
    print "----------------Environment---------------------------------" 
    env_mod.print_env(env)
    print "Environment Energy Consumption: " +  str(env_mod.compute_env_consumption(env)) + "W"
    print "\n"
    print len(env_mod.get_unused_hypervisors(env))
    print len(env_mod.get_used_hypervisors(env))
    print host_mod.compute_pm_util_avg_rel(env)
    dbops.save_environment(cons_id, ts, env, "init", actions)

    actions = cc_mod.split(env)
    print "----------------Evironment after split----------------------"
    env_mod.print_env(env)
    print "No migrations: " + str(len(actions))
    #mig_mod.print_actions(actions)
    #env_mod.print_env(env)
    print "Environment Energy Consumption: " +  str(env_mod.compute_env_consumption(env)) + "W"
    print "\n"
    print host_mod.compute_pm_util_avg_rel(env)
    print len(env_mod.get_unused_hypervisors(env))
    print len(env_mod.get_used_hypervisors(env))
    dbops.save_environment(cons_id, ts, env, "split", actions)

    actions = cc_mod.consolidate(env)
    print "----------------Environment after consolidation-------------"
    env_mod.print_env(env)
    print "No migrations: " + str(len(actions))
    #mig_mod.print_actions(actions)
    #env_mod.print_env(env)
    print "Environment Energy Consumption: " +  str(env_mod.compute_env_consumption(env)) + "W" 
    print "\n"
    print host_mod.compute_pm_util_avg_rel(env)
    print len(env_mod.get_unused_hypervisors(env))
    print len(env_mod.get_used_hypervisors(env))
    dbops.save_environment(cons_id, ts, env, "cons", actions)

if __name__ == "__main__":
    main()
