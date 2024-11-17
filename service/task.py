from dataclasses import dataclass

from repository import TaskRepository, TaskCacheRepository
from schema.task import TaskSchema


@dataclass
class TaskService:
    task_repository: TaskRepository
    task_cache: TaskCacheRepository


    def get_tasks(self):
        if cache_task := self.task_cache.get_all_tasks():
            return cache_task
        else:
            tasks = self.task_repository.get_tasks()
            tasks_schema = [TaskSchema.model_validate(task) for task in tasks]
            self.task_cache.set_tasks(tasks_schema)
            return tasks_schema