import json
import pytest
import jwt
from app.main import app
from app.schemas.pan import VerifyPanRequestSchema
from app.internal.ramp import RampAPI
from app.internal.vkyc import VkycAPI
from app.internal.turing import TuringAPI
from app.internal.session import Session
from app.internal.orck import OrckAPI
from app.utils import config
from app.database import get_db
from app.internal.ApiCommons import ApiCommons
from fastapi.testclient import TestClient

client = TestClient(app)

pytest_plugins = ('pytest_asyncio',)

@pytest.mark.asyncio
async def testTokenCreation():
    await RampAPI.token_creation_method()
    assert config['RampAPI']['api.ramp.token'] == "41b1e7655-2fdb-4f3a-8ceb-67d247cd5c11"

@pytest.mark.asyncio
async def testScreening():
    screen_req = dict()
    with open('request_payloads/screening.json') as f_in:
        screen_req = json.load(f_in)
    response = await RampAPI.ramp_screening(screen_req)
    print(response)
    screen_resp = dict()
    with open('test_payloads/screening.json') as f_in:
        screen_resp = json.load(f_in)
    assert response == screen_resp

@pytest.mark.asyncio
async def non_GenerateToken():
    decoded_token = {
    "sub": "unity_uat",
    "iss": "ipv_api_IonicApp",
    "role": "agent",
    "exp": 1740351157,
    "iat": 1740351157,
    "aud": "usr"
    }
    encoded_token = jwt.encode(decoded_token, key="somekey", algorithm="HS256")
    await VkycAPI.token_creation_method()
    assert config['VkycAPI']['api.vkyc.token'] == encoded_token

@pytest.mark.asyncio
async def SendLink():
    send_link_req = dict()
    with open('request_payloads/send_link.json') as f_in:
        send_link_req = json.load(f_in)
    api_response = await VkycAPI.vkycSendLink(send_link_req)
    send_link_resp = dict()
    with open('test_payloads/send_link.json') as f_in:
        send_link_resp = json.load(f_in)
    assert api_response == send_link_resp

@pytest.mark.asyncio
async def GetVkycDetails():
    get_details_resp = dict()
    api_response = await VkycAPI.getDetails("some_id")
    with open('test_payloads/get_details.json') as f_in:
        get_details_resp = json.load(f_in)
    assert get_details_resp == api_response

@pytest.mark.asyncio
async def not_testTuringSigning():
    signed_headers_resp = dict()
    api_response = TuringAPI.create_request_headers({"test":"payload"})
    with open('test_payloads/signed_payload.json') as f_in:
        signed_headers_resp = json.load(f_in)
    assert signed_headers_resp == api_response

@pytest.mark.asyncio
async def CustomerDetails():
    get_details_resp = dict()
    api_response = await TuringAPI.get_customer_details("12345")
    with open('test_payloads/get_customer_details.json') as f_in:
        get_details_resp = json.load(f_in)
    assert get_details_resp == api_response

@pytest.mark.asyncio
async def get_pick_list():
    get_pick_list_resp = dict()
    api_response = await TuringAPI.get_pick_list("303","C")
    with open('test_payloads/get_pick_list.json') as f_in:
        get_pick_list_resp = json.load(f_in)
    assert get_pick_list_resp == api_response

@pytest.mark.asyncio
async def test401():
    api_response = await RampAPI.ramp_screening401({'test':'payload'})
    assert {"error":"AUTH ERROR OCCURED"} == api_response

@pytest.mark.asyncio
async def CustomerIdByAadhar():
    get_aadhar_resp = dict()
    api_response = await TuringAPI.get_customer_id_by_pan_aadhar("472472614048","ARFPK2874E")
    with open('test_payloads/get_customer_id_by_aadhar.json') as f_in:
        get_aadhar_resp = json.load(f_in)
    assert get_aadhar_resp == api_response

@pytest.mark.asyncio
async def CustomerIdByAadhar():
    get_aadhar_resp = dict()
    api_response = await TuringAPI.customer_onboarding("","")
    with open('test_payloads/customer_onboarding.json') as f_in:
        get_aadhar_resp = json.load(f_in)
    assert get_aadhar_resp == api_response

@pytest.mark.asyncio
async def testCalculateRisk():
    risk_calculation_response = dict()
    _db = None 
    for db in get_db():
        _db = db
    await OrckAPI.risk_rating_calculation(_db,"123456")
    with open('test_payloads/risk_calculation.json') as f_in:
        risk_calculation_response = json.load(f_in)
    dbdata = ApiCommons.check_session_data(_db,"123456",OrckAPI.TAG_RISK_RATING_ORCK_RESPONSE)
    print(dbdata)
    assert risk_calculation_response == dbdata

def not_test_pan_verify():
    payload = VerifyPanRequestSchema(pan="ARFPK2874E",name="Man Moon",dob="2004-02-26",consent=True)
    sess = Session.create_session("ARFPK2874E")#creating session without auth for testing purposes
    response = client.post("/verify-pan",headers={"session-id":sess},json=payload.model_dump())
    response_json = response.json()
    del response_json['id']#session id is different every time
    Session.remove_session(sess)
    assert response.status_code == 200
    assert response_json == {'status': 'failed','status_remark': 'User is a returning user, no need for this step','type': 'pan'}
#{"user_id":1443520,"aadhar":"472472614048","pan":"ARFPK2874E"}