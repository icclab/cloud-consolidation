import migration as mig_mod

action = {"vm_id":"a329fe15-5243-4034-997d-d0f7810fd86b", "action":"live-migrate", "dst":"node-6"}
mig_mod.exec_migration(action)
