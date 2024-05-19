# Cluster-and-Cloud-Computing-Project-2-Group-48  

## Quick Guide
[Pre-requirements](#pre-requirements)  
[Accessing the Kubernetes Cluster](#accessing-the-kubernetes-cluster)  
[ElasticSearch API and the Kibana User Interface](#elasticsearch-api-and-the-kibana-user-interface)
## Pre-requirements

- OpenStack clients 6.3.x ([Installation instructions](https://docs.openstack.org/newton/user-guide/common/cli-install-openstack-command-line-clients.html)).
  > Note: Please ensure the following Openstack clients are installed: `python-cinderclient`, `python-keystoneclient`, `python-magnumclient`, `python-neutronclient`, `python-novaclient`, `python-octaviaclient`. See: [Install the OpenStack client](https://docs.openstack.org/newton/user-guide/common/cli-install-openstack-command-line-clients.html).
- JQ 1.6.x ([Installation instructions](https://jqlang.github.io/jq/download/)).
- Kubectl 1.26.8 ([Installation instructions](https://kubernetes.io/docs/tasks/tools/)).
- Helm 3.6.3 ([Installation instructions](https://helm.sh/docs/intro/install/)).
- Connect to [Campus network](https://studentit.unimelb.edu.au/wifi-vpn#uniwireless) if on-campus or [UniMelb Student VPN](https://studentit.unimelb.edu.au/wifi-vpn#vpn) if off-campus


## Accessing the Kubernetes Cluster
Before get access to the ElasticSearch, need to open an SSH tunnel that allows the connection of your computer to the Kubernetes cluster.    
1. The ``openrc`` file has to be source, replace the ``<path-to-openrc>`` with the path to your openrc file.
```shell
source <path-to-openrc> (e.g. ./unimelb-comp90024-2024-grp-48-openrc.sh)
```
2. Open an SSH tunnel. Please replace the ``<path-to-private-key>`` with the path to the private key file.
```shell
ssh -i <path-to-private-key> (e.g. ~/Downloads/mykeypair.pem) -L 6443:$(openstack coe cluster show elastic -f json | jq -r '.master_addresses[]'):6443 ubuntu@$(openstack server show bastion -c addresses -f json | jq -r '.addresses["qh2-uom-internal"][]')
```
> NOTES: The SSH command may take up to 1 minute to complete.

## ElasticSearch API and the Kibana User Interface
To access the ElasticSearch API and the Kibana User Interface, an SSH tunnel to the bastion node has to be opened in a different shell and kept open (see [here](#accessing-the-kubernetes-cluster)). In addition, the ``openrc`` file has to be source and ``kubeconfig`` file put under the ``~/.kube`` directory.  

  
1. To access services on the cluster, one has to use the ``port-forward`` command of ``kubectl`` in a *new terminal window*.
```shell
kubectl port-forward service/elasticsearch-master -n elastic 9200:9200
```
> NOTES: This is particularly useful for development and testing purposes, allowing direct local access without the need to interact directly with the remote Kubernetes cluster.
2. To access the Kibana user interface, one has to use the ``port-forward`` command of ``kubectl`` (*another terminal window*):
```shell
kubectl port-forward service/kibana-kibana -n elastic 5601:5601
```
  
Test the Kibana user interface by pointing the browser to: [http://127.0.0.1:5601/](http://127.0.0.1:5601/) (the default credentials are ``elastic:elastic``).  

> NOTES: Thess commands will start the port forwarding so please keep the terminals open and do not close it.
Note: The port forwarding can be stopped by pressing ``Ctrl + C`` and closing the terminal window. The port forwarding is only active when the terminal window is open. Once it is stopped, you need to re-run the command to start the port forwarding again.

