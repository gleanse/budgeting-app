from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from app.core.dependencies import UserAuthenticationDep, AuthServiceDep
from app.schemas.v1.auth_schema import (
    UserCreate,
    UserResponse,
    UserCreateResponse,
    LoginResponse,
)

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post(
    "/register", response_model=UserCreateResponse, status_code=status.HTTP_201_CREATED
)
async def register_user(
    auth_service: AuthServiceDep, user_data: UserCreate
) -> UserCreateResponse:

    try:
        registered_user = auth_service.register_user(
            username=user_data.username,
            password=user_data.password,
        )
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

    return UserCreateResponse(
        user=UserResponse(id=registered_user.id, username=registered_user.username),
    )


@router.post("/login", response_model=LoginResponse)
async def login(
    auth_service: AuthServiceDep, form_data: OAuth2PasswordRequestForm = Depends()
) -> LoginResponse:

    try:
        access_token = auth_service.login(form_data.username, form_data.password)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(e),
            headers={"WWW-Authenticate": "Bearer"},
        )

    return LoginResponse(access_token=access_token, token_type="bearer")


@router.post("/logout", status_code=status.HTTP_200_OK)
async def logout(current_user: UserAuthenticationDep):
    return {"message": "Successfully logged out"}
