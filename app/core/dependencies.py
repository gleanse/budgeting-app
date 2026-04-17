from typing import Annotated
from fastapi import Depends
from sqlmodel import Session
from app.database import get_session
from app.core.auth_core import get_current_user
from app.models import User
from app.services.v1 import (
    AuthService,
    CategoryService,
    AccountService,
    TransactionService,
)

DatabaseSessionDep = Annotated[Session, Depends(get_session)]
UserAuthenticationDep = Annotated[User, Depends(get_current_user)]


def _get_auth_service(session: DatabaseSessionDep) -> AuthService:
    return AuthService(session)


def _get_category_service(session: DatabaseSessionDep) -> CategoryService:
    return CategoryService(session)


def _get_account_service(session: DatabaseSessionDep) -> AccountService:
    return AccountService(session)


def _get_transaction_service(session: DatabaseSessionDep) -> TransactionService:
    return TransactionService(session)


# SERVICES dependencies
AuthServiceDep = Annotated[AuthService, Depends(_get_auth_service)]
CategoryServiceDep = Annotated[CategoryService, Depends(_get_category_service)]
AccountServiceDep = Annotated[AccountService, Depends(_get_account_service)]
TransactionServiceDep = Annotated[TransactionService, Depends(_get_transaction_service)]
