from typing import Annotated
from fastapi import Depends
from sqlmodel import Session
from app.database import get_session
from app.core.auth_core import get_current_user
from app.models import User
from app.services.v1 import (
    AuthService,
    TransactionService,
    CategoryService,
)

DatabaseSessionDep = Annotated[Session, Depends(get_session)]
UserAuthenticationDep = Annotated[User, Depends(get_current_user)]


def _get_auth_service(session: DatabaseSessionDep) -> AuthService:
    return AuthService(session)


def _get_transaction_service(session: DatabaseSessionDep) -> TransactionService:
    return TransactionService(session)


def _get_category_service(session: DatabaseSessionDep) -> CategoryService:
    return CategoryService(session)


# SERVICES dependencies
AuthServiceDep = Annotated[AuthService, Depends(_get_auth_service)]
TransactionServiceDep = Annotated[TransactionService, Depends(_get_transaction_service)]
CategoryServiceDep = Annotated[CategoryService, Depends(_get_category_service)]
