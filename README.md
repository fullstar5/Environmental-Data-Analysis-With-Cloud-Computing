# Big Data Analytics on the Cloud

Team 48 - COMP90024 Cluster and Cloud Computing Assignment 2 

## Description

This project combines technologies such as the Melbourne Research Cloud, Kubernetes, Fission, and Elasticsearch to analyze data from Twitter, SUDO, EPA, and BoM. The project showcases scenarios involving data harvesting, streaming, and analysis to understand the relationship between air quality, weather conditions, and public sentiment.

## Links

* [Demo]()
* [Report]()
* [Wiki](https://github.com/fullstar5/CCC-Project-2-Group-48/wiki)

## Team members

* YiFei ZHANG (1174267)
* Hanzhang SUN (1379790)
* Liyang CHEN (1135879)
* Yueyang WU (1345511)
* 

## Structure

```bash
├── backend
│   ├── api
│   │   ├── bom
│   │   ├── epa
│   │   ├── health
│   │   └── twitter
│   └── harvesters
│       ├── bomharvester
│       └── epaharvester
├── data
│   ├── raw
│   └── sorted
├── data_process
├── docs
│   ├── API.md
│   ├── Elasticsearch.md
│   └── diagram
└── frontend

```
## Installation Instructions

1. Pre-requirements:
- OpenStack clients 6.3.x ([Installation instructions](https://docs.openstack.org/newton/user-guide/common/cli-install-openstack-command-line-clients.html)).
  > Note: Please ensure the following Openstack clients are installed: `python-cinderclient`, `python-keystoneclient`, `python-magnumclient`, `python-neutronclient`, `python-novaclient`, `python-octaviaclient`. See: [Install the OpenStack client](https://docs.openstack.org/newton/user-guide/common/cli-install-openstack-command-line-clients.html).
- JQ 1.6.x ([Installation instructions](https://jqlang.github.io/jq/download/)).
- Kubectl 1.26.8 ([Installation instructions](https://kubernetes.io/docs/tasks/tools/)).
- Helm 3.6.3 ([Installation instructions](https://helm.sh/docs/intro/install/)).
- Connect to [Campus network](https://studentit.unimelb.edu.au/wifi-vpn#uniwireless) if on-campus or [UniMelb Student VPN](https://studentit.unimelb.edu.au/wifi-vpn#vpn) if off-campus

2. Clone the repository:
    ```bash
    git clone https://github.com/fullstar5/CCC-Project-2-Group-48.git
    cd CCC-Project-2-Group-48
    ```
## Usage Instructions

1. Accessing the Kubernetes Cluster   
	The ``openrc`` file has to be source, replace the ``<path-to-openrc>`` with the path to your openrc file.
```shell
source <path-to-openrc> (e.g. ./unimelb-comp90024-2024-grp-48-openrc.sh)
```
2. Open an SSH tunnel. 
	Please replace the ``<path-to-private-key>`` with the path to the private key file.
```shell
ssh -i <path-to-private-key> (e.g. ~/Downloads/mykeypair.pem) -L 6443:$(openstack coe cluster show elastic -f json | jq -r '.master_addresses[]'):6443 ubuntu@$(openstack server show bastion -c addresses -f json | jq -r '.addresses["qh2-uom-internal"][]')
```
> NOTES: The SSH command may take up to 1 minute to complete.

3. Start a port forward from the Fission router in different shell:
```
kubectl port-forward service/router -n fission 9090:80
```
4. Launch Jupyter Notebook:
    ```bash
    jupyter notebook
    ```
5. Open and run the notebooks in the `frontend/` directory to interact with the data and visualize the results.

