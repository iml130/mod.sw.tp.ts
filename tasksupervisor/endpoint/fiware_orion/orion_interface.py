import threading
import json
import logging

# import local libs
import tasksupervisor.my_globals as my_globals

from tasksupervisor.helpers import servercheck
from tasksupervisor.helpers.config_reader import ConfigReader

from tasksupervisor.flask_setup import create_flask_app

from tasksupervisor.endpoint.fiware_orion.entities.materialflow import Materialflow
from tasksupervisor.endpoint.fiware_orion.entities.sensor_agent_node import SensorAgent
from tasksupervisor.endpoint.fiware_orion.entities.materialflow_specification_state import MaterialflowSpecificationState
from tasksupervisor.endpoint.fiware_orion.entities.transport_order_update import TransportOrderUpdate
from tasksupervisor.endpoint.fiware_orion.entities.tasksupervisor_info import TaskSupervisorInfo
from tasksupervisor.endpoint.fiware_orion.entities.materialflow_update import MaterialflowUpdate

from tasksupervisor.endpoint.broker_interface import BrokerInterface
from tasksupervisor.endpoint.fiware_orion.contextbrokerhandler import ContextBrokerHandler

logger = logging.getLogger(__name__)

def callback_flask_server(flask_app):
    """ Callback method to create for the flask server """
    logger.info("Starting thread_flask_server")
    flask_app.run(host=my_globals.parsed_config_file.FLASK_HOST,
                  port=my_globals.parsed_config_file.TASKPLANNER_PORT,
                  threaded=True, use_reloader=False, debug=True)

class OrionInterface(BrokerInterface):
    """ Implements the BrokerInterface for the Orion Context Broker """

    def __init__(self, tasksupervisor_knowledge, broker_name = ""):
        BrokerInterface.__init__(self)

        self.tasksupervisor_knowledge = tasksupervisor_knowledge
        self.subscription_dict = {}
        self.broker_connector = tasksupervisor_knowledge.broker_connector

        self.flask_app = create_flask_app(tasksupervisor_knowledge, self)

        self.lock = threading.Lock()

        config_file_path = "./tasksupervisor/fiware_config.ini"

        try:
            parsed_config_file = ConfigReader(config_file_path)
            parsed_config_file.is_valid()
        except Exception:
            raise Exception("Error while parsing Fiware config file")
        
        self.context_broker_handler = ContextBrokerHandler(parsed_config_file.get_fiware_server_address())

        logger.info("Setting up thread_check_if_server_is_up")
        self.thread_check_if_server_is_up = threading.Thread(name='checkServerRunning',
                                                             target=servercheck.webserver_is_running,
                                                             args=("localhost", my_globals.parsed_config_file.TASKPLANNER_PORT,))

        logger.info("Setting up thread_flask_server")
        self.thread_flask_server = threading.Thread(name='callback_flask_server', target=callback_flask_server, args=(self.flask_app,))

    def start_interface(self):
        self.thread_check_if_server_is_up.start()
        self.thread_flask_server.start()
        logger.info("Starting Flask and wait")
        self.thread_check_if_server_is_up.join()
        logger.info("Flask is running")

    def subscribe(self, topic, opt_data=None, generic=False):
        with self.lock:
            class_name = str(topic.__class__.__name__)
            description = class_name + " subscription"
            notification = my_globals.parsed_config_file.get_taskplanner_address() + "/" + class_name.lower()

            if opt_data:
                description = opt_data.description
                if class_name == "SensorAgent":
                    notification = my_globals.parsed_config_file.get_taskplanner_address() + "/san/" + opt_data.to_id
                
            entities = [{"id": topic.id, "type": class_name}]
            sub_id = self.context_broker_handler.subscribe_to_entity(description, entities,
                                                                     notification, generic=generic)
            self.subscription_dict[sub_id] = class_name
            return sub_id

    def create(self, entity):
        fiware_entity = self.create_fiware_entity(entity)
        self.context_broker_handler.create_entity(fiware_entity)

    def update(self, entity):
        fiware_entity = self.create_fiware_entity(entity)
        fiware_entity.update_time()
        self.context_broker_handler.update_entity(fiware_entity)

    def delete(self, id, delete_entity=True):
        with self.lock:
            if delete_entity:
                self.context_broker_handler.delete_entity(id)
            else:
                self.context_broker_handler.delete_subscription_by_id(id)

    def create_fiware_entity(self, entity):
        class_name = str(entity.__class__.__name__)
        fiware_entity = None

        if class_name == "MaterialflowSpecificationState":
            fiware_entity = MaterialflowSpecificationState.from_api_object(entity)  
        elif class_name == "MaterialflowUpdate":
            fiware_entity = MaterialflowUpdate.from_api_object(entity) 
        elif class_name == "TaskSupervisorInfo":
            fiware_entity = TaskSupervisorInfo.from_api_object(entity) 
        elif class_name == "TransportOrderUpdate":
            fiware_entity =  TransportOrderUpdate.from_api_object(entity)
        else:
            raise ValueError("Creation of fiware entity for unknown class was requested: {}".format(class_name))

        return fiware_entity

    def retreive(self, json_requests):
        with self.lock:
            subscription_id = json_requests[my_globals.FI_SUB_ID]
            entity_type = self.subscription_dict[subscription_id]
            if entity_type == "Materialflow":
                # it might be possible that there are multiple entities
                # iterate over each json request
                for temp_json_request in json_requests[my_globals.FI_DATA]:
                    # create an entity from the json request
                    orion_materialflow = Materialflow.CreateObjectFromJson(temp_json_request)

                    api_materialflow = orion_materialflow.to_api_object()
                    api_materialflow.broker_ref_id = self.broker_id
                    self.broker_connector.retreive(api_materialflow, self)
            elif entity_type == "SensorAgent":
                for temp_json_request in json_requests[my_globals.FI_DATA]:
                    orion_sensor_agent = SensorAgent.CreateObjectFromJson(temp_json_request)
                    
                    api_sensor_agent = orion_sensor_agent.to_api_object()
                    self.broker_connector.retreive(api_sensor_agent, self)

    def shutdown(self):
        self.context_broker_handler.shutdown()
