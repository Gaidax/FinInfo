import jwt, time, uvloop,asyncio, json
from fastapi import FastAPI, Request, status
from fastapi.responses import PlainTextResponse
from fastapi.exceptions import RequestValidationError
from logging.handlers import RotatingFileHandler
from fastapi.middleware.cors import CORSMiddleware
from pathlib import Path
from fastapi import Request

asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
THIS_FOLDER = Path(__file__).parent.resolve()

app = FastAPI()

@app.get('/getAccountDetailsListByMobileNumber')
async def dummyAPIpayload(mobileNumber: str,status_code=200):
    """
    Dummy endpoint that emulates response from the integrated API, reads JSON file and sends it's content.

    :param mobileNumber: url param for mobile number
    :return: Response JSON
    """
    with open(THIS_FOLDER / 'sample.json') as f_in:
        return json.load(f_in)
    
@app.post('/ramp/webservices/createToken')
async def createToken(request: Request):
    print(request.headers)
    with open(THIS_FOLDER / 'test_payloads/create_token.json') as f_in:
        return json.load(f_in)
    
@app.post('/v1/agent/generate_token')
async def generate_token(request: Request):
    print(request.headers)
    print(await request.json())
    payload = {
    "sub": "unity_uat",
    "iss": "ipv_api_IonicApp",
    "role": "agent",
    "exp": 1740351157,
    "iat": 1740351157,
    "aud": "usr"
    }
    token = jwt.encode(payload, key="somekey", algorithm="HS256")
    return {
        "Token": token,
        "status_code": 200,
        "success": True
    }
    
@app.post('/ramp/webservices/request/handle-ramp-request')
async def rampRequest(request: Request):
    print(request.headers)
    print(await request.json())
    with open(THIS_FOLDER / 'test_payloads/screening.json') as f_in:
        return json.load(f_in)
    
@app.post('/v1/agent/sendLink')
async def sendLink(request: Request):
    print(request.headers)
    print(await request.json())
    with open(THIS_FOLDER / 'test_payloads/send_link.json') as f_in:
        return json.load(f_in)
    
@app.get('/v1/session/get_details/{session_id}')
async def get_details(session_id: str,request: Request):
    print(request.headers)
    print(session_id)
    with open(THIS_FOLDER / 'test_payloads/get_details.json') as f_in:
        return json.load(f_in)


@app.get('/v1/system/turing-crm-api/common-apis/get-customer-details')
async def get_details(customerId: str,request: Request):
    print(request.headers)
    print(customerId)
    with open(THIS_FOLDER / 'test_payloads/get_customer_details.json') as f_in:
        return json.load(f_in)
    
@app.get('/v1/system/turing-crm-api/picklist/get_pick_list')
async def get_pick_list(typeCode:str,orderBy:str,request: Request):
    print(request.headers)
    with open(THIS_FOLDER / 'test_payloads/get_pick_list.json') as f_in:
        return json.load(f_in)
    
@app.post('/turing/get-customer-by-aadhar')
async def get_pick_list(request: Request):
    print(request.headers)
    print(await request.json())
    with open(THIS_FOLDER / 'test_payloads/get_customer_id_by_aadhar.json') as f_in:
        return json.load(f_in)

@app.post('/401_test', status_code=401)
async def rampRequest(request: Request):
    return {"error":"this is a test error"}

@app.post('turing/insert-authorize-customer')
async def turingOnboarding(request: Request):
    print(request.headers)
    print(await request.json())
    with open(THIS_FOLDER / 'test_payloads/onboard_customer.json') as f_in:
        return json.load(f_in)
    

@app.post('orck/on-boarding/calculate-risk')
async def calculateRisk(request: Request):
    print(request.headers)
    print(await request.json())
    with open(THIS_FOLDER / 'test_payloads/calculate_risk.json') as f_in:
        return json.load(f_in)
    
app.add_middleware(
	CORSMiddleware,
	allow_origins=['*'],
	allow_methods=["GET","POST","PUT","OPTIONS"],
	allow_headers=["*"],
)

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc):
	rootLogger.error("422 EXCEPTION")
	rootLogger.error(exc.errors())
	return PlainTextResponse(str(exc), status_code=status.HTTP_422_UNPROCESSABLE_ENTITY)