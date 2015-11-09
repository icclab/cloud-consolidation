# Cloud Consolidation Tool

Simple cloud consolidation (simulation) tool for analysis of datacenteris energy consumption. Implemented consolidation algorithm computes close-to-optimum energy efficient VM placement across active cluster increasing physical hosts CPU utilization using VM live migration mechanism. Algorithm provides list of actions to be taken that can be later trigerred by DC operator.

Please note algorithm only provides a list of recommended migrations but DOES NOT actually trigger the migrations by default.

Following environment specifications are supported:
 - Randomly generated environmemt specifing:
    - Total number of physical hosts
    - Total number of VMs
 - Specified within provided input file
 - Loaded from active OpenStack environment with active ceilometer service

Web application presents prediction of environment's energy consumption before and after consolidation.

## Installation instructions
### (Optionable) Install virtualenv and create virtual environment

Install ```virtualenv```:

```
pip install virtualenv
```

Create project virtual environment:

```
virtualenv cloud_consol_env
source cloud_consol_env/bin/activate
```

### Install requirements

Install project dependencies:

```
pip install -r requirements.txt
```

### Init DB

Create ```/tmp/lmt.db``` file for storing results:

```
cd src/db/
python setup.py
```

### Run optimization

Browse to consolidation application directory:

```
cd src/core/
```

To optimize VM placement of randomly generated environment (```10 PMs, 100VMs```) run:

```
python main.py -r 10 100
```

To optimize VM placement specified in input file (```input_file.txt```) run:

```
python main.py -f input_file.txt
```

To optimize VM placement of you running OpneStack cluster run:

```
source admin.rc
python main.py
```

### Browse results

Runs Flask application:

```
cd src/web/
python vis_app.py
```

Point your browser to ```http://localhost:5000```
