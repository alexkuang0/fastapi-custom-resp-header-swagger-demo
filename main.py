from fastapi import FastAPI, Response, status, HTTPException
from pydantic import BaseModel
from random import randint

class DemoResponse(BaseModel):
    message: str

app = FastAPI()

VENDOR_CUSTOM_RESP_HEADERS = {
    'X-Vendor-ErrorCode': {
        'description': '0 means normal, 1 means error.',
        'schema': { 'type': 'number' }
    }
}

@app.get('/demo', responses={
    200: { 'headers': VENDOR_CUSTOM_RESP_HEADERS },
    400: { 'headers': VENDOR_CUSTOM_RESP_HEADERS },
    500: { 'headers': VENDOR_CUSTOM_RESP_HEADERS },
})
def demo(response: Response) -> DemoResponse:
    # randomly response with 200, 400 or 500
    status = randint(0, 2)

    match status:
        case 0:
            response.headers['X-Vendor-ErrorCode'] = '0'
            return DemoResponse(message='good')
        case 1:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                headers={ 'X-Vendor-ErrorCode': '1' },
            )
        case 2:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail={ 'request_id': '095e5265-1788-4a3e-a94f-67a09d021933' },
                headers={ 'X-Vendor-ErrorCode': '2' },
            )
