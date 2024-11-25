from motor.motor_asyncio import AsyncIOMotorClient
from pymongo.errors import DuplicateKeyError
from bson import ObjectId

import asyncio

class Database:
    def __init__(self, host):
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
            await self.users.insert_one(document=insert_query_users)
            await self.tasks.insert_one(document=insert_query_tasks)
            return True
        except DuplicateKeyError:
            return False


    async def add_task(self, user_id, task_name):
        task_id = str(ObjectId())
        task = {
            "task_id": task_id,
            "task_name": task_name
        }

        try:
            await self.tasks.find_one_and_update(
                filter={"uuid": user_id},
                update={"$push": {"tasks": task}},
                return_document=True
            )
            return True
        except Exception as e:
            raise e
            return False

    async def remove_task(self, user_id, task_id):
        try:
            result = await self.tasks.find_one_and_delete(
                filter={"uuid": user_id},
                projection={"task_id": task_id}
            )
            return True
        except Exception as e:
            raise e
            return False

    async def get_task(self, user_id, task_id):
        try:
            result = await self.tasks.find_one(filter={"uuid": user_id, "tasks.task_id": task_id})
            if result:
                task = next((task for task in result['tasks'] if task['task_id'] == task_id), None)
                return task.get("task_name")
            
            return False
        except Exception as e:
            raise e
            return False
    
    async def get_all_tasks(self, user_id):
        try:
            cursor = self.tasks.find(filter={
                "uuid": user_id
            })

            tasks = await cursor.to_list(length=None)
            
            return tasks
            
        except Exception as e:
            raise e

async def main():
    db = Database(host="mongodb://localhost:27017")
    print(await db.get_task(user_id=123, task_id="67447e0c522188299719823c"))
    print(await db.get_all_tasks(user_id=123))

asyncio.run(main())