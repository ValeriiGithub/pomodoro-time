from typing import Any

from redis import Redis
import json
from schema.task import TaskSchema

#
# class TaskCache:
#     def __init__(self, redis: Redis):
#         self.redis = redis
#
#     def get_tasks(self):
#         pass
#
#     def set_tasks(self, tasks: list[TaskSchema]):
#         tasks_json = [task.json() for task in tasks]
#         self.redis.lpush("tasks", *tasks_json)


class TaskCacheRepository:

    def __init__(self, cache_session: Redis) -> None:
        self.cache_session = cache_session

    async def get_all_tasks(self, key: str = "all_tasks") -> list[Any] | None:
        tasks_json = await self.cache_session.get(key)
        if tasks_json is None:
            return None
        return [TaskSchema.model_validate(task) for task in json.loads(tasks_json)]

    async def set_all_tasks(
        self,
        tasks: list[TaskSchema],
        key: str = "all_tasks"
    ) -> None:
        tasks_json = json.dumps([task.model_dump() for task in tasks], ensure_ascii=False)
        await self.cache_session.set(key, tasks_json, ex=60)