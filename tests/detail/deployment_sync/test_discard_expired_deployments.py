import datetime

import dateutil.tz

import idact
from idact.detail.deployment_sync.deployment_definition import \
    DeploymentDefinition
from idact.detail.deployment_sync.deployment_definitions import \
    DeploymentDefinitions
from idact.detail.deployment_sync.discard_expired_deployments import \
    discard_expired_deployments


def test_discard_expired_deployments():
    base = datetime.datetime(2017, 11, 12, 10, 00).replace(
        tzinfo=dateutil.tz.tzutc())
    deployments = DeploymentDefinitions(
        nodes={
            '30s in the past': DeploymentDefinition(
                value={},
                expiration_date=base - datetime.timedelta(seconds=30)),
            '15s in the past': DeploymentDefinition(
                value={},
                expiration_date=base - datetime.timedelta(seconds=15)),
            'now': DeploymentDefinition(
                value={},
                expiration_date=base),
            '15s in the future': DeploymentDefinition(
                value={},
                expiration_date=base + datetime.timedelta(seconds=15)),
            '30s in the future': DeploymentDefinition(
                value={},
                expiration_date=base + datetime.timedelta(seconds=30)),
            '45s in the future': DeploymentDefinition(
                value={},
                expiration_date=base + datetime.timedelta(seconds=45)),
            '60s in the future': DeploymentDefinition(
                value={},
                expiration_date=base + datetime.timedelta(seconds=60))})
    assert len(deployments.nodes) == 7
    old_utc_now = \
        idact.detail.deployment_sync.discard_expired_deployments.utc_now

    def fake_utc_now():
        return base

    try:
        idact.detail.deployment_sync.discard_expired_deployments.utc_now = \
            fake_utc_now
        new_deployments = discard_expired_deployments(deployments=deployments)
    finally:
        idact.detail.deployment_sync.discard_expired_deployments.utc_now = \
            old_utc_now

    assert len(deployments.nodes) == 7
    assert new_deployments.nodes == {
        '30s in the future': DeploymentDefinition(
            value={},
            expiration_date=base + datetime.timedelta(seconds=30)),
        '45s in the future': DeploymentDefinition(
            value={},
            expiration_date=base + datetime.timedelta(seconds=45)),
        '60s in the future': DeploymentDefinition(
            value={},
            expiration_date=base + datetime.timedelta(seconds=60))}
