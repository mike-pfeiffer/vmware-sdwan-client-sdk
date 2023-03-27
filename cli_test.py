#!/usr/bin/python3

import ipaddress
from api_rules import ApiRules
from api_groups import ApiGroups
from api_networks import ApiNetworks
from api_client_connectors import ApiClientConnectors

DEFINED_SERVICES = [
    "DHCP",
    "DNS",
    "FTP",
    "HTTP",
    "HTTPS",
    "ICMP",
    "IMAP",
    "LDAP",
    "MSFILESHARE",
    "NetBIOS",
    "NTP",
    "POP3",
    "RDP",
    "SMTP",
    "SNMP",
    "SSH"
]


class CliTest:
    """
    A class for for combining various api calls and logic to provide
    testing functionality via the cli utility.
    """

    def build_member_list(self, values):
        """
        A function for extracting individual members from groups,
        connectors, servers, and users.

        Args:
            - values (dict): a dictionary containing node details.

        Returns:
            - member_list (list): a full list of nodes from object.
        """

        member_list = []
        for value in values:

            if value["type"] == "group":
                nodes = ApiGroups().get_members(value["name"])
                if nodes:
                    for node in nodes:
                        if node["userType"] == "GATEWAY":
                            cc = self.get_cc_targets(node["name"])
                            member_list.extend(cc)
                        member_list.append(node["name"])

            elif value["type"] == "gateway":
                cc = self.get_cc_targets(value["name"])
                member_list.extend(cc)
                member_list.append(value["name"])

            else:
                member_list.append(value["name"])

        return member_list

    def find_network(self, args):
        """
        Finds a matching network for the specified parameters. At this time
        this function is missing support for including criteria for context.
        This function will only find networks by source, target, and ip rule.

        Args:
            - args (obj): argparse object containing match criteria.

        Returns:
            - reults (dict): all identified networks that matched.
        """

        networks = ApiNetworks().get_all()
        network_hits = []
        for network in networks:
            sources = network["topology"]["sourceNobs"]
            targets = network["topology"]["targetNobs"]
            new_sources = self.build_member_list(sources)
            new_targets = self.build_member_list(targets)
            rule = network["rules"]
            rule = self.validate_rule(rule, args.protocol, args.dport)

            if not rule:
                continue

            if network["type"] == "MESH":

                if args.source in new_sources and args.target in new_sources:

                    network_hits.append(network["name"])

            elif network["type"] == "HUB":
                if args.source in new_sources and args.target in new_targets:

                    network_hits.append(network["name"])

        results = {
            "Discovered Networks": network_hits
        }

        return results

    def validate_rule(self, rule, protocol, port):
        """
        Used to determine if the specified rule matches the supplied
        protocol and port.

        Args:
            - rule (str): the rule name.
            - protocol (str): tcp, udp, icmp or named service.
            - port (str): converted to int, destination port.

        Returns:
            - (boolean): True if match, False if no match.
        """

        if port is not None:
            port = int(port)
        else:
            port = 99999

        if rule is not None:
            rule = rule[0]
            rule = ApiRules().get(rule)

            predefined = rule["predefinedNetworkServices"]
            custom = rule["customNetworkServices"]

            if predefined is not None:
                for entry in predefined:
                    if entry == protocol.upper():
                        return True

            if custom is not None:
                for entry in custom:
                    port_from = int(entry["portFrom"])
                    port_to = int(entry["portTo"])
                    transport = entry["transportType"].lower()

                    if port_from <= port <= port_to and protocol == transport:
                        return True

        return False

    def get_cc_targets(self, name):
        """
        Used to retrieve the IP or DNS info the client connector advertises.

        Args:
            - name (str): the client connector name.

        Returns:
            - (boolean): A list of nodes, IPs, and DNS entries.
        """

        cc_targets = []
        cc = ApiClientConnectors().get(name)
        ips = cc["gatewayIps"]
        dns = cc["dnsHosts"]

        if ips:
            for ip in ips:
                start = ip["from"]
                stop = ip["to"]
                if start == stop:
                    cc_targets.append(start)
                else:
                    start = int(
                        ipaddress.IPv4Address(start).packed.hex(), 16
                    )

                    stop = int(
                        ipaddress.IPv4Address(stop).packed.hex(), 16
                    )
                    ip_range = range(start, stop + 1)
                    for ip_int in ip_range:
                        ip_addr = ipaddress.IPv4Address(ip_int)
                        ip_addr = str(ip_addr).split("/")[0]
                        cc_targets.append(ip_addr)

        if dns:
            for entry in dns:
                host = entry["hostname"]
                cc_targets.append(host)

        return cc_targets
