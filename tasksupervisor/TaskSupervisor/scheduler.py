import queue
import logging
import threading


from lotlan_scheduler.scheduler import LotlanScheduler

from tasksupervisor.TaskSupervisor.materialflow import Materialflow

logger = logging.getLogger(__name__)


INDEGREE_ZERO = 0
SUCCESS_TASK = 1
END_TASK = 2

class Scheduler(threading.Thread):

    def __init__(self, _materialflow, task_supervisor_knowledge):
        threading.Thread.__init__(self)
        logger.info("taskScheduler init")
        self.id = _materialflow.id
        self.run_forever = True
        self.tasklanguage = _materialflow.specification
        self._task_supervisor_knowledge = task_supervisor_knowledge

        self.lotlan_scheduler = LotlanScheduler(self.tasklanguage)
        self._materialflows = self.lotlan_scheduler.get_materialflows()

        self.name = _materialflow.ownerId
        self.owner = _materialflow.ownerId

        self.running_materialflows = []
        self.processed_materialflows = []
        self.materialflow_manager = []
        self.queue = queue.Queue()
        self.active = True
        self.broker_ref_id = _materialflow.broker_ref_id

        logger.info("taskScheduler init_end")

    def set_active(self, is_active):
        self.active = is_active
        for tm in self.materialflow_manager:
            tm.set_active(is_active)

    # def addTask(self, new_task):
    #     logger.info("taskScheduler addTask %s", new_task.name)
    #     if new_task not in self.running_materialflows:
    #         self.running_materialflows.append(new_task)
    #     logger.info("taskScheduler addTask_end")

    def run(self):
        logger.info("taskScheduler start")

        # self.lotlan_scheduler.start(self.tasklanguage)

        for materialflow in self._materialflows:
            self.materialflow_manager.append(Materialflow(
                self.owner, materialflow, self.queue, self._task_supervisor_knowledge, self.broker_ref_id))

        for tm in self.materialflow_manager:
            logger.info(
                "taskScheduler, MaterialflowUpdate spawn: %s", tm.task_manager_name)
            self.running_materialflows.append(tm)
            tm.start()

        while self.active:
            res = self.queue.get()
            logger.info(
                "taskScheduler, taskSMaterialflowUpdateet finished: %s", res)
            for temp_materialflow in self.running_materialflows:
                if temp_materialflow.task_manager_name == res:
                    temp_materialflow.join()
                    # tR.deleteEntity()
                    self.running_materialflows.remove(temp_materialflow)
                    temp_materialflow = None
            if len(self.running_materialflows) == 0:
                self.active = False
                print("End of Scheduler reached")

        logger.info("taskScheduler start_end")

    def status(self):
        # return states
        pass
