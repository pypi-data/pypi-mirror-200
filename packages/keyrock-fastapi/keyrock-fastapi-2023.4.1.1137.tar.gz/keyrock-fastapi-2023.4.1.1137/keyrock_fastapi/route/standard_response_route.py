import time
import traceback

from typing import Callable, List

from fastapi import Body, FastAPI, HTTPException, Request, Response
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from fastapi.routing import APIRoute


# class StandardResponseRoute(APIRoute):
#     def get_route_handler(self) -> Callable:
#         original_route_handler = super().get_route_handler()

#         async def custom_route_handler(request: Request) -> Response:
#             before = time.time()
#             try:
#                 response: Response = await original_route_handler(request)
#             except RequestValidationError as exc:
#                 detail = {
#                     "errors": exc.errors(),
#                 }
#                 raise HTTPException(status_code=422, detail=detail)
#             except Exception as exc:
#                 tb = traceback.format_tb(exc.__traceback__)
#                 detail = {
#                     "message": str(exc),
#                     "debug": {
#                         "loc": tb[-1],
#                         "stack": tb,
#                     }
#                 }
#                 raise HTTPException(status_code=500, detail=detail)
    
#             duration = 1000.0 * (time.time() - before)
#             response.headers["X-Response-Time-MS"] = str(duration)

#             return response

#         return custom_route_handler

class StandardResponseRoute(APIRoute):
    def get_route_handler(self) -> Callable:
        original_route_handler = super().get_route_handler()

        async def custom_route_handler(request: Request) -> Response:
            before = time.time()
            try:
                original_response: Response = await original_route_handler(request)
            except RequestValidationError as exc:
                detail = {
                    "errors": exc.errors(),
                }
                raise HTTPException(status_code=422, detail=detail)
            except HTTPException as exc:
                raise exc
            except Exception as exc:
                tb = traceback.format_tb(exc.__traceback__)
                response_data = {
                    'success': False,
                    'result': None,
                    'errors': [
                        {
                            "msg": str(exc),
                            "debug": {
                                "loc": tb[-1],
                                "stack": tb,
                            }
                        }
                    ]
                }
                wrapped_response = JSONResponse(response_data)
                return wrapped_response

            duration = 1000.0 * (time.time() - before)
            response.headers["X-Response-Time-MS"] = str(duration)
            return original_response

        return custom_route_handler