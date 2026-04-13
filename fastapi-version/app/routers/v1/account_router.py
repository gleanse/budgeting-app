from fastapi import APIRouter
from app.core.dependencies import UserAuthenticationDep, DatabaseSessionDep
from app.models import Account
from sqlmodel import select

router = APIRouter(prefix="/accounts", tags=["accounts"])


# TODO: wip temporary for testing
@router.get("/")
async def get_my_accounts(
    current_user: UserAuthenticationDep, session: DatabaseSessionDep
):
    statement = select(Account).where(Account.user_id == current_user.id)
    accounts = session.exec(statement).all()
    return [{"id": a.id, "name": a.name} for a in accounts]
