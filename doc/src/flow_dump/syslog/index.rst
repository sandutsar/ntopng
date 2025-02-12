.. _Syslog:

Syslog
------

To dump flows to Syslog, specify :code:`-F="syslog"`. Flows are dumped to Syslog in JSON format.
This allows external applications to consume dumped flows easily, and it simplifies the delivery of flows
to downstream applications such as Logstash.

An example of flow dumped to Syslog is the following

.. code:: bash

  { "IPV4_SRC_ADDR": "192.168.2.222", "SRC_ADDR_LOCAL": true, "SRC_ADDR_BLACKLISTED": false, "SRC_ADDR_SERVICES": 0, "IPV4_DST_ADDR": "192.168.2.1", "DST_ADDR_LOCAL": true, "DST_ADDR_BLACKLISTED": false, "DST_ADDR_SERVICES": 0, "SRC_TOS": 0, "DST_TOS": 0, "L4_SRC_PORT": 38294, "L4_DST_PORT": 22, "PROTOCOL": 6, "L7_PROTO": 92, "L7_PROTO_NAME": "SSH", "TCP_FLAGS": 31, "IN_PKTS": 7, "IN_BYTES": 471, "OUT_PKTS": 5, "OUT_BYTES": 2028, "FIRST_SWITCHED": 1610381756, "LAST_SWITCHED": 1610381756, "CLIENT_NW_LATENCY_MS": 0.010000, "SERVER_NW_LATENCY_MS": 0.205000, "SRC_IP_COUNTRY": "", "SRC_IP_LOCATION": [ 0.000000, 0.000000 ], "DST_IP_COUNTRY": "", "DST_IP_LOCATION": [ 0.000000, 0.000000 ], "NTOPNG_INSTANCE_NAME": "devel", "INTERFACE": "eno1" }

Packaged versions of ntopng install a rule in :code:`/etc/rsyslog.d/20-ntopng.conf` to dump flows and all other ntopng-generated Syslog logs to :code:`/var/log/ntopng.log`.
This behavior can be changed by editing or removing :code:`/etc/rsyslog.d/20-ntopng.conf`.

To process or see all ntopng-generated Syslog logs, the file :code:`/var/log/ntopng.log` can be accessed directly. On systemd-based systems, such logs
can be accessed also using the :code:`journalctl` facility. For example, to get all the logs of ntopng running as daemon, one can run

.. code:: bash

  $ sudo journalctl -u ntopng

.. warning::

  In case :code:`/var/log/ntopng.log` is edited/removed manually, service :code:`rsyslogd` may need a restart. To restart :code:`rsyslogd` type in a console :code:`sudo service rsyslog restart`


.. note::

  Syslog flows dump is not available on Windows