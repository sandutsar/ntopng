Host Policy
===========

ntopng is able to specify an host policy for selected devices that have special requirements including restrictions on host they contact.

A typical example is a network device such as a router or switch that should not initiate any type of traffic except some rare exceptions (e.g. contact the NTP server or check for updates). When relevant network hosts perform unexpected traffic, it is very likely that something wrong happened and this behaviour needs to be detected.

.. note::

  This feature is available with Enterprise L License or better.

Configuration
#############

In order to enable this feature, the 'Host Policy' behavioural check needs to be anabled.

.. figure:: ../img/host_policy_behaviour.png
  :align: center
  :alt: Host Policy Check

  Host Policy Check
  
Done this, you need to configure the host policies that are specified under Settings -> Network Configuration

.. figure:: ../img/host_policy_configuration.png
  :align: center
  :alt: Host Policy Configuration

  Host Policy Configuration
  
The configuration page allows you three type of host devices:

- Restricted Hosts (e.g. Servers, VPN servers).
- Core Hosts (e.g. Routers, Switches).
- Whitelisted Hosts: hosts that everyone can connect to (e.g. the local DNS server).

Alert Generation
################
  
An 'Host Policy' critical alert is triggered whenever:

- A restricted host connects to a public IP address not whitelisted.
- A restricted host connects to a core host.
- A core host connects to any non whitelisted address.


In case an alert is generated, the exact problem detection is reported

.. figure:: ../img/host_policy_alert.png
  :align: center
  :alt: Host Policy Alert

  Host Policy Alert
