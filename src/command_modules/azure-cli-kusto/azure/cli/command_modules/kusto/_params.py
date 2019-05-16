# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------

# pylint: disable=line-too-long
from knack.arguments import CLIArgumentType

from azure.cli.core.commands.parameters import (name_type, get_enum_type)
from azure.mgmt.kusto.models import DatabasePrincipal

from .custom import (
    AzureSkuName
)


def load_arguments(self, _):

    # Kusto clusters
    sku_arg_type = CLIArgumentType(help='The name of the sku.',
                                   arg_type=get_enum_type(AzureSkuName))
    time_format_explenation = 'Duration in ISO8601 format (for example, 100 days would be P100D).'

    with self.argument_context('kusto cluster') as c:
        c.ignore('kusto_management_request_options')
        c.argument('cluster_name', arg_type=name_type, help='The name of the cluster.', id_part='name')
        c.argument('sku', arg_type=sku_arg_type)
        c.argument('capacity', type=int, help='The instance number of the VM.')

    # Kusto databases
    with self.argument_context('kusto database') as c:
        c.ignore('kusto_management_request_options')
        c.argument('cluster_name', help='The name of the cluster.', id_part='name')
        c.argument('database_name', arg_type=name_type, help='The name of the database.', id_part='child_name_1')
        c.argument('soft_delete_period', help='Amount of time that data should be kept so it is available to query. ' + time_format_explenation)
        c.argument('hot_cache_period', help='Amount of time that data should be kept in cache.' + time_format_explenation)

    # Kusto database list
    with self.argument_context('kusto database list') as c:
        c.argument('cluster_name', id_part=None)

    # Kusto data connections
    with self.argument_context('kusto database data_connection') as c:
        c.ignore('kusto_management_request_options')
        c.argument('cluster_name', help='The name of the cluster.', id_part='name')
        c.argument('database_name', help='The name of the database.', id_part='child_name_1')
        c.argument('data_connection_name', arg_type=name_type, help='The name of the data connection.', id_part='child_name_2')


    # Kusto data connections
    with self.argument_context('kusto database principals') as c:
        c.ignore('kusto_management_request_options')
        c.argument('cluster_name', help='The name of the cluster.')
        c.argument('database_name', help='The name of the database.')
        c.argument('role', help='The role of the principal.')
        c.argument('principal_name', help='The name of the principal.')
        c.argument('type', help='The type of the principal.')
        c.argument('fqn', help='The fqn of the principal.')
        c.argument('email', help='The email of the princiapl.')
        c.argument('app_id', help='The app id of the principal.')
