# BEAURIS

 [![pipeline status](https://gitlab.com/beaur1s/beauris/badges/main/pipeline.svg)](https://gitlab.com/beaur1s/beauris/-/commits/main)

An automated system to deploy genome portals.

Originally written for genomes hosted by GOGEPP on https://bipaa.genouest.org and https://bbip.genouest.org, as well as ABIMS and SEBIMER.

This repository contains the common code needed to deploy any BEAURIS genome portal. To use it, you will need to create another GitLab repository, following the provided example.

## Authors

BEAURIS was developped initially by:

- GOGEPP/GenOuest (Rennes, France): used on [BIPAA](https://bipaa.genouest.org) and [BBIP](https://bbip.genouest.org)
- ABiMS (Roscoff, France)
- SEBIMER (Brest, France)

See [up-to-date contributors list](https://gitlab.com/beaur1s/beauris/-/graphs/main).

## Usage

General usage information, examples will be published soon.

### Repository content

A repository using the BEAURIS system should have the following content:

#### `./organisms`

This directory contains one yml file per organism to host. These file can be modified (or new created) by creating pull requests.

Yml files should conform to the schema in `beauris/validation/template/schema.yaml`. There are no constraints on the filenames, but it is adviced to name it using the pattern `genus_species.yml` or `genus_species_strain.yml`.

#### `./locked`

This directory contains yml files derived from the ones in `./organisms`. They are generated automatically by CI scripts to add internal information (like path/url to locked data).

No manual change should be done to these files. Ever. Period.

### Data processing

Adding a new genome means writing a new yml file in `.organisms` and proposing it in a Merge Request.

The data generation jobs are launched before merging because these steps will produce errors that we want to fix before merging (see "Data Locking" below).

We avoid rerunning steps for annotations that:
- have already been processed in a previous MR
- have already partially processed in case of error in the CI workflow.

This is done by comparing the content of the yml files in `./organisms` and `./locked`, and checking which files are already present in the "TEMP location" evoked earlier.

Adding a new annotation to an existing genome means modifying the existing yml file in `.organisms` and proposing the change in a Merge Request.

### Merge request labels and title

You can alter the way CI is run by using labels on MR, or by writing stuff in MR title.

Add a `run-everything` label to ignore any previous CI run and rerun all the tasks from scratch.

Add a `run-TASKID` label to ignore any previous CI run and rerun the task named "TASKID".

Add a `disable-everything` label to disable running all tasks.

Add a `disable-TASKID` label to avoid running the task named "TASKID".

Write `FU25` or `fu25` at the end of a MR title when you want to reuse the work dir from a previously merged MR (to fix problems in post merge pipeline typically). See #28 for details. (FU stands for Follow-Up (or anything else you prefer))

### GitLab runner / Cluster execution

Each platform will have its own GitLab repo, and needs a corresponding GitLab runner, and the ability to run jobs on a computing cluster.

At GOGEPP we do it like this:

- Docker GitLab runner, running on our Swarm cluster
- With mounted volumes to access data
- With mounted Slurm configuration files to be able to submit jobs
- CI jobs are launched as docker containers from the Docker GitLab runner

Environment variables that need to be defined in GitLab CI settings, or at the beginning of `.gitlab-ci.yml`:

```yaml
WORK_DIR: /some/path/  # Temporary data will be generated there (must be accessible from gitlab runner and cluster)

RUN_USER: 'foo'  # Cluster user that will own the created files and will run cluster jobs
RUN_GROUP: 'bar'  # Cluster user's group that will own the created files and will run cluster jobs
UID: 55914  # uid of RUN_USER
GID: 40259  # gid of RUN_USER

GALAXY_URL: https://usegalaxy.*/  # URL to the Galaxy server that will execute jobs

ANSIBLE_REMOTE_USER: "foo"
```

You also need these Environment variable that _must_ be defined only in GitLab CI settings (for security):

```yaml
GALAXY_API_KEY: xxxxxxxxxxxxxxxxxxxx  # API key to connect to the Galaxy server that will execute jobs
GITLAB_BOT_TOKEN: xxxxxxxxxxxxxxxxxx  # A project access token to the GitLab project ("api" scope, "reporter" role), used for posting comments from CI
GITLAB_RW_TOKEN: xxxxxxxxxxxxxxxxxxx  # A project access token to the GitLab project ("api" and "write_repository" scope, "maintainer" role), used for commiting/pushing lock files to master branch
```

Optionally, you can redefine some DRMAA variables if the [default values](https://github.com/genouest/docker_slurm_exec/blob/master/Dockerfile#L20) don't work for you:

```
SLURMGID: '992'
SLURMUID: '992'
MUNGEGID: '991'
MUNGEUID: '991'
DRMAA_LIBRARY_PATH: '/etc/slurm/drmaa/lib/libdrmaa.so.1'
```

### Job execution

We plan to have jobs running in various ways:

1. Slurm (or other HPC) jobs (e.g.: functional annotation)
2. Galaxy tool (and/or workflow) invocation (e.g. JBrowse, GeneNoteBook)
3. NextFlow workflows on a Slurm (or other HPC) infra (e.g. JBrowse at SEBIMER)

At GOGEPP, we have validated 1 and 2, with examples in workflows.

We should all be able to run these 3 sort of jobs (at least), monitor the status and fetch the corresponding results. Each site will be able to choose its preferred method for each job.

In all cases, we will have very long jobs (>1 day) exceeding the timeout of a CI job => we need a way to check the status/fetch the result/report errors regularly. Implemented in https://gitlab.inria.fr/gogepp_team/gogepp3000/-/merge_requests/4 (CI is able to catch up is ci job stops before cluster job)

### Ansible

Ansible is used to deploy / stop / update a swarm stack (for authelia)

#### Requirements

You need this environment variable that _must_ be defined only in GitLab CI settings (for security):

```
ANSIBLE_SSH_KEY: xxxxxxxxxxxxxxxxxxxx  # A private ssh key, stored as variable (not file). The public key must be in the authorized_keys of the user on the swarm controller
```

On the host, the following python modules are required by the ansible playbook:

- jsondiff
- pyyaml

#### Ansible customization

Several parameters are defined in the beauris.yml file:

```yaml
host: 192.168.1.119 # Swarm controller ip
envvars: # Various ansible environment variables
  ANSIBLE_REMOTE_USER: bipaaweb # Remote ansible user. Ansible will ssh the controller using this user
  ANSIBLE_TASK_TIMEOUT: 600 # Make sure ansible does not hang
extravars: # Various ansible extra variables
  ansible_python_interpreter: /usr/bin/python3 # If not using python2 on the host
```

### Functional annotation with the Nextflow pipeline Orson

The `func_annot_orson` task runs:
- busco (coming)
- beedeem
- diamond on uniref90
- interproscan
- eggnogmapper

Nextflow handles job submissions on SLURM (or other environments) and supervises the jobs.

#### Requirements

Requires singularity, nextflow, graphviz.

Download Orson code and singularity images (put them into `orson/containers`)
```bash
git clone https://gitlab.ifremer.fr/bioinfo/workflows/orson.git
wget -r -nc -l1 -nH --cut-dirs=6 -A '*.sif' ftp://ftp.ifremer.fr/ifremer/dataref/bioinfo/sebimer/tools/ORSON/ -P orson/containers
```

Download the nextflow config file for your cluster, e.g.:
```bash
wget https://github.com/nf-core/configs/blob/master/conf/abims.config
```

You also need the uniref90 blast bank, indexed with diamond.

#### Usage

- Set the CI step `func_annot` to use `beauris.workflows.drmaa.func_annot_orson`
- Set `job_specs` as follows in `beauris.yml`:

```yaml
job_specs:
  drmaa:
    func_annot_orson:
      # SCRATCH_WORK_DIR is supposed to be a scratch storage area for nextflow that can be cleaned up once the computation is completed.
      env : >
        source /etc/profile.d/modules.sh; module load nextflow/22.10.0 graphviz/2.40.1;
        export ORSON_PATH=/path/to/orson/;
        export BLAST_DB_PATH=/path/to/uniref90/diamond/uniref90_2022_03/uniref90.dmnd;
        export CLUSTER_CONFIG_PATH=/path/to/cluster.config;
        export SCRATCH_WORK_DIR=/path/to/scratch/workdir
```

#### Options
HECTAR (for heterokonts) is activated when it is defined as a task option in the yaml of the organism:
```yaml
    annotations:
      - version: "OGS1.0"
        [...]
        task_options:
          func_annot_orson:
            hectar: true
```

Note: HECTAR can only be used on the ABIMS cluster for now because the source code is still not published.
