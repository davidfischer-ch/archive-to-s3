=============
Archive to S3
=============

A simple script to archive (logs) to an AWS S3 bucket.

------------
Installation
------------

See `ansible-role-archive-to-s3 <https://github.com/davidfischer-ch/ansible-role-archive-to-s3>`_.

The role will install an entry in the crontab to execute it periodically.
However you are free to call it directly in the command line `archive-to-s3`.

.. Note:: The process is not preventing concurrent executions, so be aware of the risk.

-----
Usage
-----

Basic help::

    $ archive-to-s3 -h
    usage: archive-to-s3 [-h] --config CONFIG [--simulate] [--verbosity {0,1,2}]

    optional arguments:
      -h, --help           show this help message and exit
      --config CONFIG
      --simulate
      --verbosity {0,1,2}

    Archive stuff on S3.

Example configuration file (YAML)::

    enabled: true
    transfers:
      - name: logs
        bucket: my-app-log-archive
        delete: true
        directory: /var/log
        patterns: ".*\\.gz"
        # host_fqdn will be replaced by the result of socket.getfqdn()
        # e.g. ip-10-1-2-180.eu-west-1.compute.internal on Amazon Web Services
        prefix: logs/my-app/{host_fqdn}
