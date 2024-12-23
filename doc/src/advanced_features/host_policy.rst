Host Policy
===========

ntopng is able to specify an host policy for selected devices that have special requirements including restrictions on host they contact.

.. note::

  This feature is available with at least Enterprise L License.

Configuration
#############

In order to enable this feature, the 'Host Policy' behavioural check needs to be anabled.

.. figure:: ../img/host_policy_behaviour.png
  :align: center
  :alt: Host Policy Check

Done this, you need to configure the host policies that are specified under Settings -> Network Configuration

.. figure:: ../img/host_policy_configuration.png
  :align: center
  :alt: Host Policy Configuration

The configuration page allows you three type of host devices:

- Restricted Hosts (e.g. Servers, VPN servers)
- Core Hosts (e.g. Routers, Switches)
- Whitelisted Hosts: hosts that everyone can connect to


An 'Host Policy' critical alert is triggered whenever:

- A restricted host connects to a public IP address not whitelisted.
- A restricted host connects to a core host.
- A core host connects to any non whitelisted address.


In case an alert is generated, the exact problem detection is reported

.. figure:: ../img/host_policy_alert.png
  :align: center
  :alt: Host Policy Alert
