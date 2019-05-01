# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------

# pylint: disable=line-too-long

from azure.cli.command_modules.kusto._client_factory import cf_cluster, cf_database, cf_data_connection
from azure.cli.command_modules.kusto._validators import validate_cluster_args


def load_command_table(self, _):
    from azure.cli.core.commands import CliCommandType

    clusters_operations = CliCommandType(
        operations_tmpl='azure.mgmt.kusto.operations.clusters_operations#ClustersOperations.{}',
        client_factory=cf_cluster)

    database_operations = CliCommandType(
        operations_tmpl='azure.mgmt.kusto.operations.databases_operations#DatabasesOperations.{}',
        client_factory=cf_database)

    data_connection_operations = CliCommandType(
        operations_tmpl='azure.mgmt.kusto.operations.data_connections_operations#DataConnectionsOperations.{}',
        client_factory=cf_data_connection)

    with self.command_group('kusto cluster',
                            clusters_operations,
                            client_factory=cf_cluster) as g:
        g.custom_command('create', 'cluster_create', supports_no_wait=True, validator=validate_cluster_args)
        g.custom_command('stop', 'cluster_stop', supports_no_wait=True)
        g.custom_command('start', 'cluster_start', supports_no_wait=True)
        g.command('list', 'list_by_resource_group')
        g.show_command('show', 'get')
        g.command('delete', 'delete', confirmation=True)
        g.generic_update_command('update', custom_func_name='update_kusto_cluster')
        g.wait_command('wait')

    with self.command_group('kusto database',
                            database_operations,
                            client_factory=cf_database) as g:
        g.custom_command('create', 'database_create', supports_no_wait=True)
        g.command('delete', 'delete', confirmation=True)
        g.generic_update_command('update', custom_func_name='update_kusto_database', supports_no_wait=True)
        g.command('list', 'list_by_cluster')
        g.show_command('show', 'get')
        g.wait_command('wait')

    with self.command_group('kusto database data_connection',
                            data_connection_operations,
                            client_factory=cf_data_connection) as g:
        g.custom_command('create_eventhub_connection', 'data_connection_create_eventhub', supports_no_wait=True)
        g.custom_command('create_eventgrid_connection', 'data_connection_create_eventgrid', supports_no_wait=True)
        g.command('delete', 'delete', confirmation=True)
        g.generic_update_command('update', custom_func_name='update_kusto_data_connection', supports_no_wait=True)
        g.command('list', 'list_by_database')
        g.show_command('show', 'get')
        g.wait_command('wait')

    with self.command_group('kusto database principals',
                            database_operations,
                            client_factory=cf_database) as g:
        g.custom_command('add', 'database_principal_add', supports_no_wait=True)
        g.custom_command('remove', 'database_principal_remove', confirmation=True)
        g.command('list', 'list_principals')
