import boto3
from app.utils import config


class DynamoDB:
    """Class for DynamoDB related logic"""

    def __init__(self) -> None:
        endpoint = config["DynamoDB"]["endpoint.url"]
        # DynamoDBClient = boto3.client('dynamodb', endpoint_url=endpoint)
        DynamoDBResource = boto3.resource("dynamodb", endpoint_url=endpoint)
        self.AadharPanTable = DynamoDBResource.Table("AadharPan")
        self.SessionTable = DynamoDBResource.Table("Session")
        self.ScreeningTable = DynamoDBResource.Table("Screening")
        self.TuringCustomerDetailsTable = DynamoDBResource.Table(
            "TuringCustomerDetails"
        )
        self.PickListTable = DynamoDBResource.Table("PickList")
        self.SendLinkTable = DynamoDBResource.Table("SendLink")
        self.VkycDetailsTable = DynamoDBResource.Table("VkycDetails")
        self.RiskRatingCalculation = DynamoDBResource.Table("RiskRatingCalculation")
        self.VaultAadharInsertTable = DynamoDBResource.Table("VaultAadharInsert")
    

