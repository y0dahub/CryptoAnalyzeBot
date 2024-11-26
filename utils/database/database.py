from motor.motor_asyncio import AsyncIOMotorClient
from pymongo.errors import DuplicateKeyError
from bson import ObjectId

import asyncio

class Database:
    def __init__(self, host: str):
        self.host = host
        self.connection = AsyncIOMotorClient(host=self.host)

        self.db = self.connection.get_database(name="cryptobase")
        self.users = self.db.get_collection(name="users")
        self.tasks = self.db.get_collection(name="tasks")

    async def add_user(self, user_id):
        insert_query_users = {
            "uuid": user_id
        }

        insert_query_tasks = {
            "uuid": user_id,
            "tasks": []
        }
        try:
            user_exists = await self.users.find_one({"uuid": user_id})
            if not user_exists:
                await self.users.insert_one(document=insert_query_users)

            tasks_exists = await self.tasks.find_one({"uuid": user_id})
            if not tasks_exists:
                await self.tasks.insert_one(document=insert_query_tasks)

            return True
        except Exception as e:
            raise e

    async def add_task(self, user_id, currency_pair, condition):
        task_id = str(ObjectId())
        task = {
            "task_id": task_id,
            "currency_pair": currency_pair,
            "condition": condition,
            "status": "pending"
        }

        try:
            await self.tasks.update_one(
                filter={"uuid": user_id},
                update={"$push": {"tasks": task}},
                upsert=True
            )
            return task_id
        except Exception as e:
            raise e
            return False

    async def get_task(self, user_id, task_id):
        try:
            result = await self.tasks.find_one(filter={"uuid": user_id, "tasks.task_id": task_id})
            if result:
                task = next((task for task in result['tasks'] if task['task_id'] == task_id), None)
                return task
            
            return False
        except Exception as e:
            raise e
            return False
    
    async def get_all_tasks(self, user_id):
        try:
            result = await self.tasks.find_one(filter={"uuid": user_id})

            if result:
                return result.get("tasks", [])

            return False
        except Exception as e:
            raise e
            return False

    async def complete_task(self, user_id, task_id):
        try:
            result = await self.tasks.update_one(
                filter={"uuid": user_id, "tasks.task_id": task_id},
                update={"$set": {"tasks.$.status": "completed"}}
            )
            return result.modified_count > 0
        except Exception as e:
            raise e
