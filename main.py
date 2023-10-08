from fastapi import FastAPI, Response, status, HTTPException
from pydantic import BaseModel
from random import randint


class DemoResponse(BaseModel):
    message: str


class ErrorResponse(BaseModel):
    detail: str


app = FastAPI()

RESP_HEADERS = [{  # X-Vendor-ErrorCode
    'description': '0 means normal, 1 means error.',
    'schema': {'type': 'number'},
}, {  # X-Vendor-ErrorMessage
    'description': 'error message for given error code',
    'schema': {'type': 'string'},
}, {  # X-Vendor-RequestId
    'description': 'request id for the given error response',
    'schema': {'type': 'string'}
}]


@app.get('/demo', responses={
    200: {'headers': {'X-Vendor-ErrorCode': RESP_HEADERS[0]}, 'model': DemoResponse},
    400: {'headers': {'X-Vendor-ErrorCode': RESP_HEADERS[0], 'X-Vendor-ErrorMessage': RESP_HEADERS[1]}, 'model': ErrorResponse},
    500: {'headers': {'X-Vendor-ErrorCode': RESP_HEADERS[0], 'X-Vendor-RequestId': RESP_HEADERS[2]}, 'model': ErrorResponse},
})
def demo(response: Response):
    # randomly response with 200, 400 or 500
    status = randint(0, 2)

    match status:
        case 0:
            response.headers['X-Vendor-ErrorCode'] = '0'
            return DemoResponse(message='good')
        case 1:
            raise HTTPException(
                status_code=400,
                headers={
                    'X-Vendor-ErrorCode': '1',
                    'X-Vendor-ErrorMessage': 'Something went wrong on your end.',
                },
            )
        case 2:
            raise HTTPException(
                status_code=500,
                headers={
                    'X-Vendor-ErrorCode': '2',
                    'X-Vendor-RequestId': '8b8461cd-3120-4687-81a9-e2dc25705b7e',
                },
            )
