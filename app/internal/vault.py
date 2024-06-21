from app.internal.ApiCommons import ApiCommons
from app.config.vault import config


class VaultApi(ApiCommons):
    ApiBASE = config.base_url
    ApiInsert = config.insert_api_endpoint
    ApiGetByRefId = config.get_by_refid_api_endpoint
    ApiGetByRefData = config.get_by_refdata_api_endpoint

    @classmethod
    async def insert(cls, payload: dict) -> tuple:
        return await cls.make_async_request(
            "POST",
            cls.ApiInsert,
            payload=payload,
        )

    @classmethod
    async def GetByRefId(cls, ref_id: str) -> tuple:
        url = f"{cls.ApiGetByRefId}?refId={ref_id}"
        return await cls.make_async_request("GET", url=url)

    @classmethod
    async def GetByRefData(cls) -> tuple:
        return await cls.make_async_request(
            "GET",
            cls.ApiGetByRefData,
        )
