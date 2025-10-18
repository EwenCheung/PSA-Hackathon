"""
API v1: Sample Router

This is an example showing how to structure FastAPI routers in the api/v1 directory.
Each module should define its routes using APIRouter and export it to be included in main.py.

Pattern:
1. Create an APIRouter instance with prefix and tags
2. Define route handlers as async functions decorated with @router.get/post/etc
3. Use Pydantic models for request/response validation
4. Handle errors and return appropriate HTTP status codes
5. Export the router to be included in main.py
"""

from fastapi import APIRouter, HTTPException, status
from typing import List
from pydantic import BaseModel

# Create router with prefix and tags for API documentation
router = APIRouter(
    prefix="/api/v1/sample",
    tags=["Sample"],
)


# Example Pydantic models for request/response
class SampleItem(BaseModel):
    id: str
    name: str
    description: str


class SampleCreateRequest(BaseModel):
    name: str
    description: str


# Example GET endpoint
# GET http://127.0.0.1:8000/api/v1/sample/items
@router.get("/items", response_model=List[SampleItem])
async def list_items():
    """
    List all sample items.
    
    Returns:
        List[SampleItem]: List of sample items
    """
    # This is where you'd call your service layer
    return [
        SampleItem(id="1", name="Item 1", description="First item"),
        SampleItem(id="2", name="Item 2", description="Second item"),
    ]


# Example GET endpoint with path parameter
@router.get("/items/{item_id}", response_model=SampleItem)
async def get_item(item_id: str):
    """
    Get a specific sample item by ID.
    
    Args:
        item_id: The ID of the item to retrieve
        
    Returns:
        SampleItem: The requested item
        
    Raises:
        HTTPException: 404 if item not found
    """
    # Example: Call service layer to get item
    if item_id == "1":
        return SampleItem(id="1", name="Item 1", description="First item")
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Item with id {item_id} not found"
        )


# Example POST endpoint
@router.post("/items", response_model=SampleItem, status_code=status.HTTP_201_CREATED)
async def create_item(request: SampleCreateRequest):
    """
    Create a new sample item.
    
    Args:
        request: Item creation request with name and description
        
    Returns:
        SampleItem: The newly created item
    """
    # Example: Call service layer to create item
    new_item = SampleItem(
        id="3",
        name=request.name,
        description=request.description
    )
    return new_item


# Example endpoint with error handling
@router.delete("/items/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_item(item_id: str):
    """
    Delete a sample item by ID.
    
    Args:
        item_id: The ID of the item to delete
        
    Raises:
        HTTPException: 404 if item not found
        HTTPException: 500 for internal errors
    """
    try:
        # Example: Call service layer to delete item
        if item_id == "999":
            raise ValueError("Item not found")
        
        # No return needed for 204 No Content
        return None
        
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Internal error: {str(e)}"
        )
