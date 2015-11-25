"""Display details for a specified volume."""
# :license: MIT, see LICENSE for more details.

import SoftLayer
from SoftLayer.CLI import environment
from SoftLayer.CLI import formatting
from SoftLayer import utils

import click


@click.command()
@click.argument('volume_id')
@environment.pass_env
def cli(env, volume_id):
    """Display details for a specified volume."""
    file_manager = SoftLayer.FileStorageManager(env.client)
    file_volume = file_manager.get_file_volume_details(volume_id)
    file_volume = utils.NestedDict(file_volume)

    table = formatting.KeyValueTable(['Name', 'Value'])
    table.align['Name'] = 'r'
    table.align['Value'] = 'l'

    table.add_row(
        ['ID', file_volume['id']])
    table.add_row(
        ['Username', file_volume['username']])
    table.add_row(
        ['Type', file_volume['storageType']['keyName'].split('_').pop(0)])
    table.add_row(
        ['Capacity (GB)', "%iGB" % file_volume['capacityGb']])

    if file_volume['storageType']['keyName'].split('_').pop(0) == 'PERFORMANCE':
        table.add_row(
            ['IOPs', file_volume['iops']])
    if file_volume['storageType']['keyName'].split('_').pop(0) == 'ENDURANCE':
        table.add_row(
            ['Endurance Tier', file_volume['storageTierLevel']['description']])

    table.add_row(
        ['Data Center', file_volume['serviceResource']['datacenter']['name']])
    table.add_row(
        ['Bytes Used', file_volume['bytesUsed']])
    table.add_row(
        ['IP', file_volume['serviceResourceBackendIpAddress']])

    if file_volume['snapshotCapacityGb']:
        table.add_row(
            ['Snapshot Reserved (GB)', file_volume['snapshotCapacityGb']])
        table.add_row(
            ['Snapshot Used (Byes)', file_volume['snapshotSizeBytes']])

    env.fout(table)
