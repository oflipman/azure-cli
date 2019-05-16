# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------

from azure.cli.testsdk import ScenarioTest, ResourceGroupPreparer
import unittest

_running_state = "Running"
_stopped_state = "Stopped"


class AzureKustoClusterTests(ScenarioTest):

    @ResourceGroupPreparer()
    def test_kusto_cluster_life_cycle(self, resource_group):
        self.kwargs.update({
            'sku': 'Standard_D13_v2',
            'name': self.create_random_name(prefix='test', length=20),
            'location': "Central US",
            'capacity': 4
        })

        # Create cluster
        self.cmd('az kusto cluster create -n {name} -g {rg} --sku {sku} --capacity {capacity}',
                 checks=[self.check('name', '{name}'),
                         self.check('sku.name', '{sku}'),
                         self.check('state', _running_state),
                         self.check('provisioningState', 'Succeeded'),
                         self.check('sku.capacity', '{capacity}')])

        # Get cluster
        self.cmd('az kusto cluster show -n {name} -g {rg}',
                 checks=[self.check('name', '{name}'),
                         self.check('sku.name', '{sku}'),
                         self.check('state', _running_state),
                         self.check('provisioningState', 'Succeeded'),
                         self.check('sku.capacity', '{capacity}')])

        # Update cluster
        self.kwargs.update({
            'sku': 'D14_v2',
            'capacity': 6
        })
        self.cmd('az kusto cluster update -n {name} -g {rg} --sku {sku} --capacity {capacity} ',
                 checks=[self.check('name', '{name}'),
                         self.check('sku.name', '{sku}'),
                         self.check('state', _running_state),
                         self.check('provisioningState', 'Succeeded'),
                         self.check('sku.capacity', '{capacity}')])

        # Delete cluster
        self.cmd('az kusto cluster delete -n {name} -g {rg} -y')

    @ResourceGroupPreparer()
    def test_kusto_cluster_stop_start(self, resource_group):
        self.kwargs.update({
            'sku': 'Standard_D13_v2',
            'name': self.create_random_name(prefix='test', length=20),
        })

        self.cmd('az kusto cluster create -n {name} -g {rg} --sku {sku}',
                 checks=[self.check('name', '{name}'),
                         self.check('sku.name', '{sku}'),
                         self.check('state', _running_state),
                         self.check('provisioningState', 'Succeeded')])

        self.cmd('az kusto cluster stop -n {name} -g {rg}')

        # Verify that the state is stopped
        self.cmd('az kusto cluster show -n {name} -g {rg}',
                 checks=[self.check('name', '{name}'),
                         self.check('sku.name', '{sku}'),
                         self.check('state', _stopped_state),
                         self.check('provisioningState', 'Succeeded')])

        self.cmd('az kusto cluster start -n {name} -g {rg}')

        # Verify that the state is running
        self.cmd('az kusto cluster show -n {name} -g {rg}',
                 checks=[self.check('name', '{name}'),
                         self.check('sku.name', '{sku}'),
                         self.check('state', _running_state),
                         self.check('provisioningState', 'Succeeded')])

        self.cmd('az kusto cluster delete -n {name} -g {rg} -y')


class AzureKustoDatabaseTests (ScenarioTest):
    @ResourceGroupPreparer()
    def test_kusto_database_life_cycle(self, resource_group):
        self.kwargs.update({
            'sku': 'Standard_D13_v2',
            'cluster_name': self.create_random_name(prefix='test', length=20),
            'database_name': self.create_random_name(prefix='testdb', length=20),
            'location': "Central US",
            'soft_delete_period': 'P10D',
            'hot_cache_period': 'P5D',
            'soft_delete_period_display': '10 days, 0:00:00',
            'hot_cache_period_display': '5 days, 0:00:00'
        })

        # Create cluster
        self.cmd('az kusto cluster create -n {cluster_name} -g {rg} --sku {sku}',
                 checks=[self.check('name', '{cluster_name}'),
                         self.check('sku.name', '{sku}')])

        # Create database
        self.cmd('az kusto database create --cluster-name {cluster_name} -g {rg} -n {database_name}  --soft-delete-period {soft_delete_period} --hot-cache-period {hot_cache_period}',
                 checks=[self.check('name', '{cluster_name}/{database_name}'),
                         self.check('softDeletePeriod', '{soft_delete_period_display}'),
                         self.check('hotCachePeriod', '{hot_cache_period_display}')])

        # Update database
        self.kwargs.update({
            'soft_delete_period': 'P20D',
            'hot_cache_period': 'P10D',
            'soft_delete_period_display': '20 days, 0:00:00',
            'hot_cache_period_display': '10 days, 0:00:00'
        })

        self.cmd('az kusto database update --cluster-name {cluster_name} -g {rg} -n {database_name}  --soft-delete-period {soft_delete_period} --hot-cache-period {hot_cache_period}',
                 checks=[self.check('name', '{cluster_name}/{database_name}'),
                         self.check('softDeletePeriod', '{soft_delete_period_display}'),
                         self.check('hotCachePeriod', '{hot_cache_period_display}')])

        # Delete database
        self.cmd('az kusto database delete --cluster-name {cluster_name} -g {rg} -n {database_name} -y')

        # Delete cluster
        self.cmd('az kusto cluster delete -n {cluster_name} -g {rg} -y')


    @ResourceGroupPreparer(random_name_length = 15)
    def test_kusto_database_principals(self, resource_group):
        self.kwargs.update({
            'sku': 'Standard_D13_v2',
            'cluster_name': self.create_random_name(prefix='test', length=20),
            'database_name': self.create_random_name(prefix='testdb', length=20),
            'location': "Central US",
            'soft_delete_period': 'P10D',
            'hot_cache_period': 'P5D',
            'soft_delete_period_display': '10 days, 0:00:00',
            'hot_cache_period_display': '5 days, 0:00:00',
            'name': "Oren Hasbani",
            'email': "orhasban@microsoft.com",
            'fqn': "aaduser=orhasban@microsoft.com",
            'role': "Admin",
            'type': "User"
        })


        # Create cluster
        self.cmd('az kusto cluster create -n {cluster_name} -g {rg} --sku {sku}',
                 checks=[self.check('name', '{cluster_name}'),
                         self.check('sku.name', '{sku}')])
        # Create database
        self.cmd('az kusto database create --cluster-name {cluster_name} -g {rg} --database-name {database_name}  --soft-delete-period {soft_delete_period} --hot-cache-period {hot_cache_period}',
                 checks=[self.check('name', '{cluster_name}/{database_name}'),
                         self.check('softDeletePeriod', '{soft_delete_period_display}'),
                         self.check('hotCachePeriod', '{hot_cache_period_display}')])
        
        instance = self.cmd('az kusto database principals list --cluster-name {cluster_name} -g {rg} --database-name {database_name}').get_output_in_json()
        principals_length = len(instance)

        a1 = self.cmd('az kusto database principals add --cluster-name {cluster_name} --resource-group {rg} --database-name {database_name} --principal-name "{name}" --email {email} --fqn {fqn} --role Admin --type User')#,
                 #checks=[self.check('length(value)', str(principals_length + 1)),
                 #        self.check('['+ str(principals_length) + '].name', '{name}')])
                 
        b1 = self.cmd('az kusto database principals remove --cluster-name {cluster_name} --resource-group {rg} --database-name {database_name} --principal-name "{name}" --email {email} --fqn {fqn} --role Admin --type User -y')#.get_output_in_json()#,
                 #checks=[self.check('length(value)', str(principals_length))])

        # Delete database
        self.cmd('az kusto database delete --cluster-name {cluster_name} -g {rg} --database-name {database_name} -y')

        # Delete cluster
        self.cmd('az kusto cluster delete -n {cluster_name} -g {rg} -y')


class AzureKustoDataConnectionTests (ScenarioTest):
    @ResourceGroupPreparer(random_name_length = 15)
    def test_kusto_data_connection_life_cycle(self, resource_group):
        self.kwargs.update({
            'sku': 'Standard_D13_v2',
            'cluster_name': self.create_random_name(prefix='test', length=20),
            'database_name': self.create_random_name(prefix='testdb', length=20),
            'eventhub_data_connection_name': self.create_random_name(prefix='testehdc', length=20),
            'storage_name': self.create_random_name(prefix='testsa', length=20),
            'eventhub_namespace_name' : self.create_random_name(prefix='testehnname', length=20),
            'eventhub_name' : self.create_random_name(prefix='testehname', length=20),
            'topic_name':self.create_random_name(prefix='testegtopic', length=20),
            'event_subscription_name': self.create_random_name(prefix='testes', length=20),
            'eventhub_consumer_group': '$Default',
            'location': "Central US",
            'soft_delete_period': 'P10D',
            'hot_cache_period': 'P5D',
            'soft_delete_period_display': '10 days, 0:00:00',
            'hot_cache_period_display': '5 days, 0:00:00',
            'kind': 'eventhub',
            'consumer_group': '$Default',
        })

        ## create storage account
        #storage_instance = self.cmd('az storage account create -n {storage_name} -g {rg} -l "{location}"').get_output_in_json()

        ## create event hub namespace
    #    eventhub_namepsace_instance = self.cmd('az eventhubs namespace create --name {eventhub_namespace_name} --resource-group {rg} -l "{location}"').get_output_in_json()
    #
    #    # create event hub 
    #    eventhub_instance = self.cmd('az eventhubs eventhub create --name {eventhub_name} --resource-group {rg} --namespace-name {eventhub_namespace_name}').get_output_in_json()

        self.kwargs.update({
            'event_hub_resource_id': "eventhubresourceid",
            #'event_hub_resource_id': eventhub_instance["id"],
        })

        # Create cluster
   #     self.cmd('az kusto cluster create -n {cluster_name} -g {rg} --sku {sku}',
   #              checks=[self.check('name', '{cluster_name}'),
   #                      self.check('sku.name', '{sku}')])

        # Create database
        #self.cmd('az kusto database create --cluster-name {cluster_name} -g {rg} -n {database_name}  --soft-delete-period {soft_delete_period} --hot-cache-period {hot_cache_period}',
        ##self.cmd('az kusto database create --cluster-name {cluster_name} -g {rg} --database-name {database_name}  --soft-delete-period {soft_delete_period} --hot-cache-period {hot_cache_period}',
        #         checks=[self.check('name', '{cluster_name}/{database_name}'),
        #                 self.check('softDeletePeriod', '{soft_delete_period_display}'),
        #                 self.check('hotCachePeriod', '{hot_cache_period_display}')])

        # Create eventhub data connection
        self.cmd('az kusto database data_connection create_eventhub_connection -n {eventhub_data_connection_name} --cluster-name {cluster_name} -g {rg} --database-name {database_name} --data-format csv --consumer-group {consumer_group} --event-hub-resource-id {event_hub_resource_id}')#,
                 #checks=[self.check('name', '{cluster_name}/{database_name}/{eventhub_data_connection_name}'),
                 #        self.check('eventHubResourceId', '{event_hub_resource_id}'),
                 #        self.check('consumerGroup', '{consumer_group}')] )
        
        # Get event hub data connection
        self.cmd('az kusto database data_connection show -n {eventhub_data_connection_name} --cluster-name {cluster_name} -g {rg} --database-name {database_name}',
                 checks=[self.check('name', '{cluster_name}/{database_name}/{eventhub_data_connection_name}'),
                         self.check('eventHubResourceId', '{event_hub_resource_id}'),
                         self.check('consumerGroup', '{consumer_group}')] )
        
         # Update eventhub data connection
        self.kwargs.update({
            'data_format': 'tsv'
        })

        self.cmd('az kusto database data_connection update -n {eventhub_data_connection_name} --cluster-name {cluster_name} -g {rg} --database-name {database_name} --data-format {data_format}',
                 checks=[self.check('name', '{cluster_name}/{database_name}/{eventhub_data_connection_name}'),
                         self.check('eventHubResourceId', '{event_hub_resource_id}'),
                         self.check('consumerGroup', '{consumer_group}'),
                         self.check('dataFormat', '{data_format}')] )

        # Delete eventhub data connection
        self.cmd('az kusto database data_connection delete -n {eventhub_data_connection_name} --cluster-name {cluster_name} -g {rg} --database-name {database_name} -y')


        #=======================================================
        #self.kwargs.update({
        #    'eventgrid_data_connection_name': self.create_random_name(prefix='testegdc', length=20),
        #    'kind': 'eventgrid',
        #})

        ## Create eventgrid data connection
        #self.cmd('az kusto database data_connection create_eventgrid_connection -n {eventgrid_data_connection_name} --cluster-name {cluster_name} -g {rg} --database-name {database_name} --data-format tsv --consumer-group {consumer_group} --event-hub-resource-id {event_hub_resource_id} --storage-account-resource-id {storage_account_resource_id}',
        #         checks=[self.check('name', '{cluster_name}/{database_name}/{eventgrid_data_connection_name}'),
        #                 self.check('eventHubResourceId', '{event_hub_resource_id}'),
        #                 self.check('consumerGroup', '{consumer_group}')] )
        
        ## Get eventgrid data connection
        #self.cmd('az kusto database data_connection show -n {eventgrid_data_connection_name} --cluster-name {cluster_name} -g {rg} --database-name {database_name}',
        #         checks=[self.check('name', '{cluster_name}/{database_name}/{eventgrid_data_connection_name}'),
        #                 self.check('eventHubResourceId', '{event_hub_resource_id}'),
        #                 self.check('consumerGroup', '{consumer_group}')] )
        
        # # Update eventgrid data connection
        #self.kwargs.update({
        #    'data_format': 'csv'
        #})

        #self.cmd('az kusto database data_connection update -n {eventhub_data_connection_name} --cluster-name {cluster_name} -g {rg} --database-name {database_name} --data-format {data_format}',
        #         checks=[self.check('name', '{cluster_name}/{database_name}/{eventhub_data_connection_name}'),
        #                 self.check('eventHubResourceId', '{event_hub_resource_id}'),
        #                 self.check('consumerGroup', '{consumer_group}'),
        #                 self.check('dataFormat', '{data_format}')] )

        ## Delete eventgrid data connection
        #self.cmd('az kusto database data_connection delete -n {eventhub_data_connection_name} --cluster-name {cluster_name} -g {rg} --database-name {database_name} -y')
        #======================================



        # Delete database
        self.cmd('az kusto database delete --cluster-name {cluster_name} -g {rg} -n {database_name} -y')
        #self.cmd('az kusto database delete --cluster-name {cluster_name} -g {rg} --database-name {database_name} -y')

        # Delete cluster
        self.cmd('az kusto cluster delete -n {cluster_name} -g {rg} -y')

if __name__ == '__main__':
    unittest.main()
