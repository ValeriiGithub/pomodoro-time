from redis import Redis

from schema.task import TaskSchema


class TaskCache:
    def __init__(self, redis: Redis):
        self.redis = redis

        def get_tasks(self):
            pass

        def set_tasks(self, tasks: TaskSchema):
            tasks_json = [task.json() for task in tasks]
            self.redis.set("tasks", *tasks_json)
