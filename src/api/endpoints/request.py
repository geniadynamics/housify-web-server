from fastapi import APIRouter, Depends, HTTPException

router = APIRouter()


@router.get("/requests")
async def get_requests():
    """
    Get a list of requests.

    Returns:
    - List of requests.
    """
    example_requests = [
        {"id": 1, "description": "Request 1"},
        {"id": 2, "description": "Request 2"},
    ]

    return example_requests


@router.get("/requests/{request_id}")
async def get_request(request_id: int):
    """
    Get details of a specific request.

    Parameters:
    - `request_id`: ID of the request to be retrieved.

    Returns:
    - Details of the specific request.
    """
    example_request = {"id": request_id, "description": f"Request {request_id}"}

    return example_request


@router.post("/requests")
async def create_request(request_data: dict):
    """
    Create a new request.

    Parameters:
    - `request_data`: Data of the new request to be created.

    Returns:
    - Details of the newly created request.
    """
    created_request = {"id": 3, "description": "New Request", **request_data}

    return created_request
