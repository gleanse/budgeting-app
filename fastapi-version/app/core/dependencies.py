from typing import Annotated
from fastapi import Depends
from sqlmodel import Session
from app.database import get_session
from app.core.auth_core import get_current_user
from app.models import User
from app.services.v1.transaction_service import TransactionService
from app.services.v1.auth_service import AuthService

DatabaseSessionDep = Annotated[Session, Depends(get_session)]
UserAuthenticationDep = Annotated[User, Depends(get_current_user)]


def get_transaction_service(session: DatabaseSessionDep) -> TransactionService:
    return TransactionService(session)


def get_auth_service(session: DatabaseSessionDep) -> AuthService:
    return AuthService(session)


TransactionServiceDep = Annotated[TransactionService, Depends(get_transaction_service)]
AuthServiceDep = Annotated[AuthService, Depends(get_auth_service)]
