from fastapi import FastAPI, Response, status
from random import randint

app = FastAPI()

VENDOR_CUSTOM_RESP_HEADERS = {
    'X-Vendor-ErrorCode': {
        'description': 'Error code defined by Vendor',
        'schema': { 'type': 'number' }
    }
}

@app.get('/demo', responses={
    200: { 'headers': VENDOR_CUSTOM_RESP_HEADERS },
    400: { 'headers': VENDOR_CUSTOM_RESP_HEADERS },
})
def demo(response: Response):
    is_success = randint(0, 1)
    if is_success:
        response.headers['X-Vendor-ErrorCode'] = '0'
        return { 'message': 'good' }
    else:
        response.headers['X-Vendor-ErrorCode'] = '1'
        response.status_code = status.HTTP_400_BAD_REQUEST
        return { 'message': 'bad' }
