# sdwan-client-api

This is an unofficial SDK for the VMware SD-WAN Client API.

This SDK includes a CLI utility called **sdwc.py** to allow for CLI-based
interaction with the API.

## Table of Contents

- [Requirements](#requirements)
- [Authentication](#authentication)
- [Basic Usage](#basic)
- [Create Commands](#create)
- [Delete Commands](#delete)
- [Show Commands](#show)
- [Test Commands](#test)

<div id='requirements'/>

## Requirements

Python3

<div id='authentication'/>

## Authentication 

Authentication to the API requires that you export both the API Key and Base URL to environment variables.

```shell
export SDWC_BASE_URL=https://api.example.net
export SDWC_API_KEY=TRhOWUtODNhZC04NTA2Y
```

The URL and API entry above are examples and do not reflect the correct URL or structure for the API key. Consult the vendor documentation on how to retrieve these values.

<div id='basic'/>

## Basic Usage 

The CLI is built using argparse and comes with built-in help functionality. Simply type "-h" or "--help" after each positional argument to see the available features.

```shell
$ ./sdwc.py --help
usage: sdwc.py [-h] {create,delete,show,test} ...

SD-WAN Client API CLI

positional arguments:
  {create,delete,show,test}
    create              add an object
    delete              remove an object
    show                get object details
    test                validate configurations

options:
  -h, --help            show this help message and exit
```

<div id='create'/>

## Create Commands

Below are examples of creating various objects in the client orchestrator.

```shell
$ ./sdwc.py create connectors --name "Test Client Connector" --interface ens5

$ ./sdwc.py create servers --name demo_server --subdomain demo

$ ./sdwc.py create users --name "Mike Test Users" --role standard --email onetwothree@velocloud.net

$ ./sdwc.py create rules --name empty_rule

$ ./sdwc.py create contexts --name empty_context

$ ./sdwc.py create groups --name "Demo Group"

$ ./sdwc.py create networks --name "Demo Network" --type mesh --rule empty_rule --context empty_context --sources demo_server
```

<div id='delete'/>

## Delete Commands

Below are examples of deleting various objects in the client orchestrator.

```shell
$ ./sdwc.py delete networks --name "Demo Network"

$ ./sdwc.py delete rules --name empty_rule

$ ./sdwc.py delete contexts --name empty_context

$ ./sdwc.py delete connectors --name "Test Client Connector"

$ ./sdwc.py delete servers --name demo_server

$ ./sdwc.py delete groups --name "Demo Group"

$ ./sdwc.py delete users --name "Mike Test Users"
```

<div id='show'/>

## Show Commands

Below are examples of show info on various objects in the client orchestrator.

```shell
$ ./sdwc.py show connectors --name cc-alpha

$ ./sdwc.py show servers --name farmland

$ ./sdwc.py show users --name "Some One"

$ ./sdwc.py show groups --name cc-group

$ ./sdwc.py show rules --name rdp-only

$ ./sdwc.py show contexts --name only-us

$ ./sdwc.py show networks --name full-mesh
```

<div id='test'/>

## Test Commands

This is a work in progress. At the time of this writing you can validate if a network matches specified sources, targets, and rules. Contexts will be added later.

```shell
$ ./sdwc.py test networks --source auser@example.com --target 172.31.255.1 --protocol tcp --dport 3389

$ ./sdwc.py test networks --source auser@example.com --target *.example.internal --protocol rdp
```
