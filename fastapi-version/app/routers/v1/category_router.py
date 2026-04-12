from fastapi import APIRouter, HTTPException, status
from app.core.dependencies import UserAuthenticationDep, CategoryServiceDep
from app.schemas.v1.category_schema import (
    CategoryCreate,
    CategoryResponse,
    CategoryCreateResponse,
    CategoryDelete,
    CategoryDeleteResponse,
)

router = APIRouter(prefix="/categories", tags=["categories"])


@router.get("/", response_model=list[CategoryResponse])
async def get_categories(
    current_user: UserAuthenticationDep, category_service: CategoryServiceDep
) -> list[CategoryResponse]:
    return category_service.list_by_user(current_user.id)


@router.post(
    "/", response_model=CategoryCreateResponse, status_code=status.HTTP_201_CREATED
)
async def create_category(
    current_user: UserAuthenticationDep,
    category_service: CategoryServiceDep,
    category_data: CategoryCreate,
) -> CategoryCreateResponse:

    try:
        created_category = category_service.create(
            name=category_data.name,
            type=category_data.type,
            user_id=current_user.id,
        )
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

    return CategoryCreateResponse(
        category=CategoryResponse(
            id=created_category.id,
            name=created_category.name,
            type=created_category.type,
            user_id=created_category.user_id,
        )
    )


@router.delete("/{category_id}", response_model=CategoryDeleteResponse)
async def delete_category(
    current_user: UserAuthenticationDep,
    category_service: CategoryServiceDep,
    category_id: int,
) -> CategoryDeleteResponse:

    try:
        deleted_category = category_service.delete(
            id=category_id, user_id=current_user.id
        )
    except ValueError as e:
        if "not found" in str(e):
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
        else:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

    return CategoryDeleteResponse(
        deleted_item=CategoryDelete(
            id=deleted_category.id,
            name=deleted_category.name,
            type=deleted_category.type,
        )
    )
