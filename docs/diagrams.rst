Class diagrams
==============

Core classes
------------

.. figure:: diagrams/core-nodes.png
    :scale: 50 %
    :alt: Core class diagram - nodes
    :figclass: align-center

.. figure:: diagrams/core-deployments.png
    :scale: 50 %
    :alt: Core class diagram - deployments
    :figclass: align-center

.. figure:: diagrams/core-config-tunnels.png
    :scale: 50 %
    :alt: Core class diagram - config and tunnels
    :figclass: align-center

Core classes are essentially a collection of user-facing interfaces.

Along free functions in the main :py:mod:`idact` module, they are everything
a user needs in order to take advantage of the system from a Python program.

Most of the core classes are intended to hide implementation details by being
abstract.

:py:mod:`idact` core classes:
 - :py:class:`.AuthMethod` (Enum not shown)
 - :py:class:`.Cluster`
 - :py:class:`.ClusterConfig`
 - :py:class:`.DaskDeployment`
 - :py:class:`.DaskDiagnostics`
 - :py:class:`.JupyterDeployment`
 - :py:class:`.KeyType` (Enum not shown)
 - :py:class:`.Node`
 - :py:class:`.NodeResourceStatus`
 - :py:class:`.Nodes`
 - :py:class:`.Retry` (Enum not shown)
 - :py:class:`.RetryConfig`
 - :py:class:`.SetupActionsConfig`
 - :py:class:`.SynchronizedDeployments`
 - :py:class:`.Tunnel`
 - :py:class:`.Walltime`

Core implementation classes
---------------------------

Nodes
~~~~~

.. figure:: diagrams/detail-core-nodes.png
    :scale: 50 %
    :alt: Core implementation class diagram
    :figclass: align-center

These classes implement the core interfaces related to nodes.

Detail classes are never intended to be manually instantiated by the user.

 - :py:class:`.ClusterImpl`
 - :py:class:`.NodeImpl`
 - :py:class:`.NodeInternal`
 - :py:class:`.NodeResourceStatusImpl`
 - :py:class:`.NodesImpl`

Deployments
~~~~~~~~~~~

.. figure:: diagrams/detail-core-deployments.png
    :scale: 50 %
    :alt: Core implementation class diagram - deployments
    :figclass: align-center

These classes implement the core interfaces related to deployments.

 - :py:class:`.DaskDeploymentImpl`
 - :py:class:`.DaskDiagnosticsImpl`
 - :py:class:`.JupyterDeploymentImpl`
 - :py:class:`.SynchronizedDeploymentsImpl`

Tunnels
~~~~~~~

.. figure:: diagrams/detail-core-tunnels.png
    :scale: 50 %
    :alt: Core implementation class diagram - tunnels
    :figclass: align-center

These classes implement the core interfaces related to tunnels.

 - :py:class:`.FirstHopTunnel`
 - :py:class:`.MultiHopTunnel`
 - :py:class:`.SshTunnel`
 - :py:class:`.TunnelInternal`

Config
~~~~~~

.. figure:: diagrams/detail-core-config.png
    :scale: 50 %
    :alt: Core implementation class diagram - config
    :figclass: align-center

These classes implement the core interfaces related to config.

 - :py:class:`.ClusterConfigImpl`
 - :py:class:`.RetryConfigImpl`
 - :py:class:`.SetupActionsConfigImpl`

Detail classes
--------------

Allocation
~~~~~~~~~~

.. figure:: diagrams/detail-allocation.png
    :scale: 50 %
    :alt: Allocation detail class diagram
    :figclass: align-center

The following classes are used internally for allocating nodes, currently
only using the Slurm workload manager.

Allocation detail classes:
 - :py:class:`.Allocation`
 - :py:class:`.AllocationParameters`
 - :py:class:`.SbatchArguments`
 - :py:class:`.SlurmAllocation`
 - :py:class:`.SqueueResult`

Deployments
~~~~~~~~~~~

.. figure:: diagrams/detail-deployment.png
    :scale: 50 %
    :alt: Deployment detail class diagram
    :figclass: align-center

These classes store information about programs deployed internally on allocated
nodes.

They provide ways to interact with the programs or cancel the deployments.

Deployment detail classes:
 - :py:class:`.DaskSchedulerDeployment`
 - :py:class:`.DaskWorkerDeployment`
 - :py:class:`.GenericDeployment`
 - :py:class:`.SshdPortInfo`

Deployment synchronization
~~~~~~~~~~~~~~~~~~~~~~~~~~

.. figure:: diagrams/detail-deployment-sync.png
    :scale: 50 %
    :alt: Deployment synchronization detail class diagram
    :figclass: align-center

Classes used internally for synchronizing deployments to and from a cluster.

Deployment detail classes:
 - :py:class:`.DeploymentDefinition`
 - :py:class:`.DeploymentDefinitions`

Config
~~~~~~

.. figure:: diagrams/detail-config.png
    :scale: 50 %
    :alt: Config detail class diagram
    :figclass: align-center

Internal config class that corresponds to a config file.

It contains all the information needed to create an :py:mod:`idact` user
environment.

Config detail classes:
 - :py:class:`.ClientConfig`

Other
~~~~~

.. figure:: diagrams/detail-other.png
    :scale: 50 %
    :alt: Other detail class diagram
    :figclass: align-center

Other classes used internally that do not belong to any of the categories
above.

Other detail classes:
 - :py:class:`.Binding`
 - :py:class:`.DebugLogFilter`
 - :py:class:`.Environment`
 - :py:class:`.EnvironmentProvider`
 - :py:class:`.GetpassExecutedError`
 - :py:class:`.LoggerProvider` (not shown)
 - :py:class:`.PasswordCache`
 - :py:class:`.Serializable`
