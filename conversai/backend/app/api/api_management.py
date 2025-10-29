"""
API Management endpoints for ConversAI
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.api.schemas import APICreate, APIUpdate, APIResponse, APITestRequest, APITestResponse
from app.core.database import get_db
from app.models.database import APIRegistry
from app.services.api_handler import request_handler
from app.core.security import encryption_service
import logging

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/apis", tags=["api-management"])


@router.get("/list", response_model=List[APIResponse])
async def list_apis(
    include_system: bool = True,
    db: Session = Depends(get_db)
):
    """List all available APIs"""
    try:
        query = db.query(APIRegistry).filter(APIRegistry.is_active == True)
        
        if not include_system:
            query = query.filter(APIRegistry.is_system == False)
        
        apis = query.all()
        
        # Explicitly convert to dict to ensure all fields are included
        result = []
        for api in apis:
            api_dict = {
                "api_id": api.api_id,
                "api_name": api.api_name,
                "description": api.description,
                "category": api.category,
                "intent_keywords": api.intent_keywords,
                "endpoint": api.endpoint,
                "method": api.method,
                "auth_config": api.auth_config,
                "parameters": api.parameters,
                "response_mapping": api.response_mapping,
                "response_template": api.response_template,
                "rate_limit": api.rate_limit,
                "error_messages": api.error_messages,
                "is_active": api.is_active,
                "is_system": api.is_system,
                "created_at": api.created_at
            }
            result.append(api_dict)
        
        return result
        
    except Exception as e:
        logger.error(f"Error listing APIs: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error listing APIs: {str(e)}"
        )


@router.get("/{api_id}", response_model=APIResponse)
async def get_api(
    api_id: str,
    db: Session = Depends(get_db)
):
    """Get API details by ID"""
    try:
        api = db.query(APIRegistry).filter(APIRegistry.api_id == api_id).first()
        
        if not api:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="API not found"
            )
        
        return api
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting API: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error getting API: {str(e)}"
        )


@router.post("/register", response_model=APIResponse, status_code=status.HTTP_201_CREATED)
async def register_api(
    api_data: APICreate,
    db: Session = Depends(get_db)
):
    """Register a new custom API"""
    try:
        # Encrypt sensitive data if present
        auth_config = api_data.auth_config
        if auth_config and "key" in auth_config:
            auth_config["key"] = encryption_service.encrypt(auth_config["key"])
        
        # Create new API
        new_api = APIRegistry(
            user_id="demo-user",  # In production, get from auth
            api_name=api_data.api_name,
            description=api_data.description,
            intent_keywords=api_data.intent_keywords,
            category=api_data.category,
            endpoint=api_data.endpoint,
            method=api_data.method,
            auth_config=auth_config,
            parameters=api_data.parameters,
            response_mapping=api_data.response_mapping,
            response_template=api_data.response_template,
            rate_limit=api_data.rate_limit,
            error_messages=api_data.error_messages,
            is_system=False
        )
        
        db.add(new_api)
        db.commit()
        db.refresh(new_api)
        
        logger.info(f"Registered new API: {new_api.api_name}")
        return new_api
        
    except Exception as e:
        logger.error(f"Error registering API: {e}")
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error registering API: {str(e)}"
        )


@router.put("/{api_id}", response_model=APIResponse)
async def update_api(
    api_id: str,
    api_update: APIUpdate,
    db: Session = Depends(get_db)
):
    """Update an existing API"""
    try:
        logger.info(f"Updating API {api_id} with data: {api_update.dict(exclude_unset=True)}")
        
        api = db.query(APIRegistry).filter(APIRegistry.api_id == api_id).first()
        
        if not api:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="API not found"
            )
        
        if api.is_system:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Cannot modify system APIs"
            )
        
        # Update fields
        update_data = api_update.dict(exclude_unset=True)
        
        # Encrypt auth_config if present and has key
        if "auth_config" in update_data and update_data["auth_config"]:
            auth_config = update_data["auth_config"]
            if "key" in auth_config and auth_config["key"]:
                auth_config["key"] = encryption_service.encrypt(auth_config["key"])
            update_data["auth_config"] = auth_config
        
        for field, value in update_data.items():
            setattr(api, field, value)
        
        db.commit()
        db.refresh(api)
        
        logger.info(f"Successfully updated API: {api.api_name}")
        return api
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error updating API: {str(e)}", exc_info=True)
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error updating API: {str(e)}"
        )


@router.delete("/{api_id}")
async def delete_api(
    api_id: str,
    db: Session = Depends(get_db)
):
    """Delete a custom API"""
    try:
        api = db.query(APIRegistry).filter(APIRegistry.api_id == api_id).first()
        
        if not api:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="API not found"
            )
        
        if api.is_system:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Cannot delete system APIs"
            )
        
        db.delete(api)
        db.commit()
        
        logger.info(f"Deleted API: {api.api_name}")
        return {"message": f"API '{api.api_name}' deleted successfully"}
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error deleting API: {e}")
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error deleting API: {str(e)}"
        )


@router.post("/{api_id}/test", response_model=APITestResponse)
async def test_api(
    api_id: str,
    test_request: APITestRequest,
    db: Session = Depends(get_db)
):
    """Test an API with sample parameters"""
    try:
        from app.services.api_mapper import APIMapper
        
        api = db.query(APIRegistry).filter(APIRegistry.api_id == api_id).first()
        
        if not api:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="API not found"
            )
        
        # Prepare request
        api_mapper = APIMapper(db)
        request_config = api_mapper.prepare_api_request(api, test_request.test_params)
        
        if not request_config:
            return APITestResponse(
                success=False,
                error="Failed to prepare API request"
            )
        
        # Send test request
        response = await request_handler.send_request(
            request_config=request_config,
            category=api.category,
            use_cache=False  # Don't cache test requests
        )
        
        # Check for errors
        if "error" in response:
            return APITestResponse(
                success=False,
                error=response["error"]
            )
        
        return APITestResponse(
            success=True,
            data=response
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error testing API: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error testing API: {str(e)}"
        )
