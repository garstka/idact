Class diagrams
==============

Core classes
------------

.. figure:: diagrams/core.png
    :scale: 50 %
    :alt: Core class diagram
    :figclass: align-center

Core classes are essentially a collection of user-facing interfaces.

Along free functions in the main :py:mod:`idact` module, they are everything
a user needs in order to take advantage of the system from a Python program.

Most of the core classes are intended to hide implementation details by being
abstract.

:py:mod:`idact` core classes:
 - :py:class:`.AuthMethod`
 - :py:class:`.Cluster`
 - :py:class:`.ClusterConfig`
 - :py:class:`.DaskDeployment`
 - :py:class:`.DaskDiagnostics`
 - :py:class:`.JupyterDeployment`
 - :py:class:`.KeyType`
 - :py:class:`.Node`
 - :py:class:`.NodeResourceStatus`
 - :py:class:`.Nodes`
 - :py:class:`.Retry`
 - :py:class:`.RetryConfig`
 - :py:class:`.SetupActionsConfig`
 - :py:class:`.SynchronizedDeployments`
 - :py:class:`.Tunnel`
 - :py:class:`.Walltime`

Core implementation classes
---------------------------

.. figure:: diagrams/detail-core.png
    :scale: 50 %
    :alt: Core implementation class diagram
    :figclass: align-center

These classes implement the core interfaces.

They are never intended to be manually instantiated by the user.

Core implementation classes:
 - :py:class:`.ClusterConfigImpl`
 - :py:class:`.ClusterImpl`
 - :py:class:`.DaskDeploymentImpl`
 - :py:class:`.DaskDiagnosticsImpl`
 - :py:class:`.FirstHopTunnel`
 - :py:class:`.JupyterDeploymentImpl`
 - :py:class:`.MultiHopTunnel`
 - :py:class:`.NodeImpl`
 - :py:class:`.NodeInternal`
 - :py:class:`.NodeResourceStatusImpl`
 - :py:class:`.NodesImpl`
 - :py:class:`.RetryConfigImpl`
 - :py:class:`.SetupActionsConfigImpl`
 - :py:class:`.SynchronizedDeploymentsImpl`

Allocation detail classes
-------------------------

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

Deployment detail classes
-------------------------

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

Deployment synchronization detail classes
-----------------------------------------

.. figure:: diagrams/detail-deployment-sync.png
    :scale: 50 %
    :alt: Deployment synchronization detail class diagram
    :figclass: align-center

Classes used internally for synchronizing deployments to and from a cluster.

Deployment detail classes:
 - :py:class:`.DeploymentDefinition`
 - :py:class:`.DeploymentDefinitions`

Config detail classes
---------------------

.. figure:: diagrams/detail-config.png
    :scale: 50 %
    :alt: Config detail class diagram
    :figclass: align-center

Internal config class that corresponds to a config file.

It contains all the information needed to create an :py:mod:`idact` user
environment.

Config detail classes:
 - :py:class:`.ClientConfig`

Other detail classes
--------------------

.. figure:: diagrams/detail-other.png
    :scale: 50 %
    :alt: Other detail class diagram
    :figclass: align-center

Other classes used internally that do not belong to any of the categories
above.

Other detail classes:
 - :py:class:`.Binding`
 - :py:class:`.Environment`
 - :py:class:`.EnvironmentProvider`
 - :py:class:`.GetpassExecutedError`
 - :py:class:`.LoggerProvider`
 - :py:class:`.PasswordCache`
 - :py:class:`.Serializable`
