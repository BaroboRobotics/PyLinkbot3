
Configuration
=============

Here are some configurable settings that are modifiable at runtime to change
the behaviour of the Linkbot package.

Transport Layer
---------------
By default, PyLinkbot3 uses WebSockets to communicate with the Linkbot Daemon.
The Linkbot Daemon uses WebSockets as its transport layer since Linkbot Labs
version 2.0, as well as Linkbot Hubs. Prior to this, Linkbot Labs used SFP as
the transport layer.

To modify this behavior, you may do::

    import linkbot3
    
    linkbot3.config(use_sfp=True) # Use SFP

Alternatively, you may set an environment variable in your shell::

    export LINKBOT_USE_SFP=1

Note that the environment variable setting will override any configuration
settings set with the "linkbot3.config()" function.

Daemon Address/Port
-------------------

By default, the Python package searches for the linkbotd daemon at
'localhost:42000'. If, instead, you would like to use a remote daemon (such as
a Linkbot-Hub), you may specify the address of the hub like so::

    import linkbot3

    linkbot3.config(daemon_hostport='linkbot-hub-3113.local:42000')

Or, you may set an environment variable in your shell::

    export LINKBOT_DAEMON_HOSTPORT=192.168.0.10:42000

Note that the environment variable setting will override any configuration
settings set with the "linkbot3.config()" function.
