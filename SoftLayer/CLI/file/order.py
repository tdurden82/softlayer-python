"""Order a file storage volume."""
# :license: MIT, see LICENSE for more details.

import SoftLayer
from SoftLayer.CLI import environment
from SoftLayer.CLI import exceptions
import click


@click.command()
@click.option('--storage_type',
              help='Type of storage volume',
              type=click.Choice(['performance', 'endurance']),
              required=True)
@click.option('--size',
              help='Size of storage volume',
              required=True)
@click.option('--iops',
              help='Performance Storage IOPs')
@click.option('--tier',
              help='Endurance Storage Tier (IOP per GB)',
              type=click.Choice(['0.25', '2', '4']))
@click.option('--location',
              help='Size of storage volume',
              required=True)
@environment.pass_env
def cli(env, storage_type, size, iops, tier, location):
    """Order a file storage volume."""
    file_manager = SoftLayer.FileStorageManager(env.client)

    if storage_type == 'performance':
        if iops is None:
            raise exceptions.CLIAbort('Option --iops required with performance')

        order = file_manager.order_file_volume(
            storage_type='performance_storage_nfs',
            location=location,
            size=size,
            iops=iops
        )

    if storage_type == 'endurance':
        if tier is None:
            raise exceptions.CLIAbort('Option --tier required with performance')

        order = file_manager.order_file_volume(
            storage_type='storage_service_enterprise',
            location=location,
            size=size,
            tier_level=tier
        )

    if 'placedOrder' in order.keys():
        print "Order #{0} placed successfully!".format(
            order['placedOrder']['id'])
        for item in order['placedOrder']['items']:
            print " > %s" % item['description']
    else:
        print "Order could not be placed! Please verify your options " \
              "and try again."
