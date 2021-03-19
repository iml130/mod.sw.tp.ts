import threading
from threading import Thread
import json
import logging
import tasksupervisor.my_globals as my_globals 

# import local libs
from tasksupervisor.endpoint.broker_interface import BrokerInterface
from tasksupervisor.flask_setup import create_flask_app
from tasksupervisor.helpers.config_reader import ConfigReader
from tasksupervisor.api.materialflow import Materialflow
from tasksupervisor.endpoint.fiware_orion.entities import materialflow
from tasksupervisor.endpoint.fiware_orion.contextbrokerhandler import ContextBrokerHandler

from tasksupervisor.endpoint.broker_connector import BrokerConnector
from tasksupervisor.task_supervisor_knowledge import TaskSupervisorKnowledge
from tasksupervisor.__main__ import callback_new_materialflow


logger = logging.getLogger(__name__)

class OrionInterface(BrokerInterface):
    """ Implements the BrokerInterface for the Orion Context Broker """

    lock = threading.Lock()

    def __init__(self, tasksupervisor_knowledge):
        threading.Thread.__init__(self)
        self.tasksupervisor_knowledge = tasksupervisor_knowledge
        self.subscription_dict = {}
        self.broker_connector = tasksupervisor_knowledge.broker_connector

        config_file_path = "./tasksupervisor/fiware_config.ini"

        try:
            parsed_config_file = ConfigReader(config_file_path)
            parsed_config_file.is_valid()
        except Exception:
            raise Exception("Error while parsing Fiware config file")
        
        self.context_broker_handler = ContextBrokerHandler(parsed_config_file.get_fiware_server_address())
        
        self.thread_new_materialflow = Thread(target=callback_new_materialflow,
                                              args=(my_globals.taskQueue, tasksupervisor_knowledge))
        self.app = create_flask_app(tasksupervisor_knowledge, self)
    
    def start_interface(self):
        self.thread_new_materialflow.start()
        self.start()

    def run(self):
        self.app.run(host=my_globals.parsed_config_file.FLASK_HOST,
                port=my_globals.parsed_config_file.TASKPLANNER_PORT,
                threaded=True, use_reloader=False, debug=True)

    def subscribe(self, topic, opt_data=None, generic=False):
        class_name = str(topic.__class__.__name__)
        description = class_name + " subscription"
        if opt_data:
            description = opt_data.description
        notification = my_globals.parsed_config_file.get_taskplanner_address() + "/" + class_name.lower()
        entities = [{"id": topic.id, "type": class_name}]
        sub_id = self.context_broker_handler.subscribe_to_entity(description, entities,
                                                                 notification, generic=generic)
        self.subscription_dict[sub_id] = class_name

    def create(self, data):
        pass

    def update(self, data):
        pass

    def delete(self, data):
        pass

    def retreive(self, json_requests):
        subscription_id = json_requests[my_globals.FI_SUB_ID]
        entity_type = self.subscription_dict[subscription_id]
        if entity_type == "Materialflow":
            # it might be possible that there are multiple entities
            # iterate over each json request
            for temp_json_request in json_requests[my_globals.FI_DATA]:
                # create an entity from the json request
                orion_materialflow = materialflow.Materialflow.CreateObjectFromJson(
                    temp_json_request)

                api_materialflow = orion_materialflow.to_api_object()
                self.broker_connector.retreive(api_materialflow, self)

    def shutdown(self):
        pass

if __name__ == "__main__":
    broker_connector = BrokerConnector()
    task_supervisor = TaskSupervisorKnowledge()
    task_supervisor.broker_connector = broker_connector

    interface = OrionInterface(task_supervisor)

    broker_connector.register_interface(interface)
    interface.start_interface()

    new_materialflow = Materialflow()
    broker_connector.subscribe_generic(new_materialflow)