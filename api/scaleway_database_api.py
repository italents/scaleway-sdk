import json
from models.region import Region
from models.rdb.database import Database
from models.rdb.instance import Instance
from models.pagination import Pagination
from .scaleway_api import ScalewayAPI
from pydantic import validate_arguments


class ScalewayDataBaseAPI(ScalewayAPI):

    def __init__(self, region: str = "fr-par"):
        super().__init__(name="rdb", version="v1", region=region)

    # INSTANCES #

    @validate_arguments
    def list_instances(
        self,
        name: str = None,
        pagination: Pagination = Pagination(),
        ordering: Instance.Ordering = Instance.Ordering(),
        project_id: str = None,
        organization_id: str = None
    ): return [Instance(**data) for data in json.loads(
            self.request("/instances", data={
                "organization_id": organization_id, "project_id": project_id,
                "name": name} | pagination.dict() | ordering.dict()))["instances"]]

    @validate_arguments
    def list_databases(
        self,
        instance: Instance,
        name: str = None,
        managed: bool = None,
        owner: str = None,
        ordering: Database.Ordering = Database.Ordering(),
    ): return [Database(**data) for data in json.loads(
            self.request(f"/instances/{instance.id}/databases", data={
                "owner": owner,
                "managed": managed,
                "name": name} | pagination.dict() | ordering.dict()))["databases"]]
