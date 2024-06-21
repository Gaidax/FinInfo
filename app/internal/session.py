from uuid import uuid4
from app.db.DynamoDB import DynamoDB
from fastapi import HTTPException, Depends, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials 

security = HTTPBasic()

class Session():
    """Custom middleware for session-based authentication"""

    @staticmethod
    def create_session(subtoken: str):#TODO:should probably use user_id instead of pan?
        """
        Static method that creates a session after user is authenticated

        :param user_pan: create a session and associate it with user pan
        :return: session id
        """
        dynamo = DynamoDB()
        session_id = uuid4().hex
        dynamo.SessionTable.put_item(Item={'session_id':session_id,'subtoken':subtoken})
        return session_id

    @staticmethod
    def get_authenticated_subtoken_from_session_id(session_id:str):
        """
        Static method for dependency injection that gets user pan from a session

        :param user_pan: create a session and associate it with user pan
        :return: session id
        """
        return session_id
        # dynamo = DynamoDB()
        # if session_id is None or not dynamo.SessionTable.get_item(Key={"session_id":session_id}).get('Item'):
        #     return None
        # Get the subtoken from the session
        # return dynamo.SessionTable.get_item(Key={"session_id":session_id}).get('Item').get('subtoken')
    
    @staticmethod
    def authenticate_user(credentials: HTTPBasicCredentials = Depends(security)):
        """
        Static method for dependency injection that authenticates user via basic credentials (as an example)
        
        not finished

        :param credentials: basic auth
        :return: session id
        """
        user = ""#userstable.getitem(credentials.username)
        if user is None:#or user["password"] != credentials.password:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid credentials",
                headers={"WWW-Authenticate": "Basic"},
            )
        return user
    
    @staticmethod
    def remove_session(session_id:str):
        """
        Static method that deletes a session

        :param session_id: session id to delete
        :return: None
        """
        dynamo = DynamoDB()
        dynamo.SessionTable.delete_item(Key={'session_id':session_id})
