import importlib.util
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Any, Callable, Dict, Optional

import aiofiles
import databases
import shortuuid
import sqlalchemy
from mako.template import Template

WORKDIR = Path(__file__).resolve().parent

metadata = sqlalchemy.MetaData()


@dataclass
class SeedNode:
    seed_id: str
    seed: Callable[..., Any]
    previous_seed_id: Optional[str] = None
    next_seed: Optional["SeedNode"] = None


class Seed:
    def __init__(self, scripts_path: Path, database_url: str | None = None):
        """Initialize a Seed object.

        :param scripts_path: A pathlib.Path object representing
            the path to the directory where seed scripts are stored.
        :param database_url: A url for connecting to the database
        """
        self.scripts_path = scripts_path
        self.database_url = database_url

    def __find_latest_seed(self) -> Optional[str]:
        """Find the most recently created seed script in the scripts' directory.

        :returns: The name of the most recently created seed
            script, or None if no seed scripts are found in the directory.
        """
        files = Path(self.scripts_path).iterdir()
        try:
            latest_file = max(files, key=lambda f: f.stat().st_ctime)
        except ValueError:
            return None
        return latest_file.stem

    async def create_file(self, message: str):
        """Create a new seed file with the given message as part of the filename.

        :param message: A string message to be included as part of the filename.
        """
        seed_id = shortuuid.uuid()
        template = Template(filename=str(WORKDIR / "seeds.py.mako"))
        latest_seed = self.__find_latest_seed()
        file_content = template.render(
            seed_id=seed_id,
            created_at=datetime.now(),
            previous_seed=latest_seed or "",
        )

        file_name = f"{seed_id}.py"
        if message:
            file_name = message.replace(" ", "_") + file_name
        file_path = self.scripts_path / file_name
        async with aiofiles.open(file_path, mode="w") as f:
            await f.write(file_content)

    def __create_linked_list(self) -> SeedNode | None:
        """Create a linked list of SeedNode objects
            from seed scripts in the scripts directory.

        :returns: The head node of the linked list.
        """
        root = None
        seed_dict: Dict[str, SeedNode] = {}
        for script in self.scripts_path.iterdir():
            if script.name.endswith(".py"):
                module_name = script.stem

                # Import the module dynamically
                spec = importlib.util.spec_from_file_location(
                    module_name, str(script)
                )
                module = importlib.util.module_from_spec(spec)  # type:ignore
                spec.loader.exec_module(module)  # type:ignore

                # Access the desired function from the module
                seed_id = getattr(module, "seed_id")
                previous_seed_id = getattr(module, "previous_seed_id")
                seed_function = getattr(module, "seed")
                # Create a SeedNode object for the current seed_id
                seed_node = SeedNode(
                    seed_id=seed_id,
                    seed=seed_function,
                    previous_seed_id=previous_seed_id,
                )

                if previous_seed_id is None:
                    root = seed_node

                if previous_seed_id in seed_dict:
                    previous_seed_node = seed_dict[previous_seed_id]
                    previous_seed_node.next_seed = seed_node

                # Add the SeedNode object to the dictionary
                seed_dict[seed_id] = seed_node
        return root

    async def create_table(self):
        """Creates table in database"""
        async with databases.Database(self.database_url) as database:
            query = """
            CREATE TABLE "seed" (
              "id" varchar(30) PRIMARY KEY,
              "previous_seed_id" varchar(30) REFERENCES "seed"("id"),
              "sown_at" timestamp
            );
            """
            await database.execute(query)

    @staticmethod
    async def write_to_database(
        database: databases.Database,
        seed_id: str,
        previous_seed_id: str | None = None,
    ):
        """
        Insert records to database

        :param database: database object to execute query
        :type database: databases.Database
        :param seed_id: identifier of the current seed
        :type seed_id: str
        :param previous_seed_id: identifier of the seed that precedes
            current one, defaults to None
        :type previous_seed_id: str | None, optional
        """
        query = """
            INSERT INTO "seed" ("id", "previous_seed_id", "sown_at")
            VALUES (:seed_id, :previous_seed_id, NOW()::timestamp);
            """
        await database.execute(
            query,
            values={"seed_id": seed_id, "previous_seed_id": previous_seed_id},
        )

    @staticmethod
    async def exists(
        database: databases.Database,
        seed_id: str,
    ) -> bool:
        """Check if seed exists in the database

        :param database: database object to execute query
        :type database: databases.Database
        :param seed_id: identifier of the seed we are looking for
        :type seed_id: str
        :return: true if the seed exists and false otherwise
        :rtype: bool
        """
        query = """
            SELECT EXISTS (
              SELECT 1
              FROM "seed"
              WHERE "id" = :seed_id
            );
        """
        record = await database.fetch_one(query, values={"seed_id": seed_id})
        return record.exists

    async def execute(self):
        """Execute the seed scripts in the order specified by the linked list.

        The linked list is created by calling the __create_linked_list method.
        """
        database = databases.Database(self.database_url)
        if not database.is_connected:
            await database.connect()
        async with database.transaction():
            head = self.__create_linked_list()

            while head is not None:
                if not await self.exists(database, head.seed_id):
                    await head.seed()
                    await self.write_to_database(
                        database=database,
                        seed_id=head.seed_id,
                        previous_seed_id=head.previous_seed_id,
                    )

                head = head.next_seed
        if database.is_connected:
            await database.disconnect()
