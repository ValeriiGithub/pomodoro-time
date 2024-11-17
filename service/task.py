from repository import TaskRepository, TaskCacheRepository
from schema.task import TaskSchema


class TaskService:
    def __init__(self, task_repository: TaskRepository, task_cache: TaskCacheRepository):
        self.task_repository = task_repository
        self.task_cache = task_cache

    def get_tasks(self):
        if cache_task := self.task_cache.get_all_tasks():
            return cache_task
        else:
            tasks = self.task_repository.get_tasks()
            tasks_schema = [TaskSchema.model_validate(task) for task in tasks]
            self.task_cache.set_all_tasks(tasks_schema)
            return tasks_schema