Class diagrams
==============

Core classes
------------

.. figure:: diagrams/core.png
    :scale: 50 %
    :alt: Core class diagram
    :figclass: align-center

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

Core implementation classes:
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
 - :py:class:`.SynchronizedDeploymentsImpl`

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

Deployment detail classes
-------------------------

.. figure:: diagrams/detail-deployment.png
    :scale: 50 %
    :alt: Deployment detail class diagram
    :figclass: align-center

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

Deployment detail classes:
 - :py:class:`.DeploymentDefinition`
 - :py:class:`.DeploymentDefinitions`

Config detail classes
---------------------

.. figure:: diagrams/detail-config.png
    :scale: 50 %
    :alt: Config detail class diagram
    :figclass: align-center

Config detail classes:
 - :py:class:`.ClientConfig`
 - :py:class:`.ClusterConfigImpl`
 - :py:class:`.SetupActionsConfigImpl`

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
 - :py:class:`.GetpassExecutedError`
 - :py:class:`.LoggerProvider`
 - :py:class:`.PasswordCache`
 - :py:class:`.Serializable`
