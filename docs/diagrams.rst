Class diagrams
==============

Core classes
------------

.. figure:: diagrams/core.png
    :scale: 60 %
    :alt: Core class diagram
    :figclass: align-center

:py:mod:`idact.core` classes:
 - :py:class:`.AuthMethod`
 - :py:class:`.Cluster`
 - :py:class:`.Node`
 - :py:class:`.Nodes`
 - :py:class:`.Tunnel`
 - :py:class:`.Walltime`

Core implementation classes
---------------------------

.. figure:: diagrams/detail-core.png
    :scale: 50 %
    :alt: Core implementation class diagram
    :figclass: align-center

Core implementation classes:
 - :py:class:`.ClusterImpl`
 - :py:class:`.NodeImpl`
 - :py:class:`.NodesImpl`

Allocation detail classes
-------------------------

.. figure:: diagrams/detail-allocation.png
    :scale: 50 %
    :alt: Allocation detail class diagram
    :figclass: align-center

Allocation detail classes:
 - :py:class:`.Allocation`
 - :py:class:`.AllocationParameters`
 - :py:class:`.SbatchArguments`
 - :py:class:`.SlurmAllocation`
 - :py:class:`.SqueueResult`

Config detail classes
---------------------

.. figure:: diagrams/detail-config.png
    :scale: 50 %
    :alt: Config detail class diagram
    :figclass: align-center

Config detail classes:
 - :py:class:`.ClientClusterConfig`
 - :py:class:`.ClientConfig`

Other detail classes
--------------------

.. figure:: diagrams/detail-other.png
    :scale: 50 %
    :alt: Other detail class diagram
    :figclass: align-center

Other detail classes:
 - :py:class:`.Binding`
 - :py:class:`.Environment`
 - :py:class:`.EnvironmentProvider`
 - :py:class:`.FirstHopTunnel`
 - :py:class:`.MultiHopTunnel`
 - :py:class:`.PasswordCache`
