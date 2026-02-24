from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core import db
from app.models.audit_logs import AuditLog
from app.models.user import User
from app.models.user_consent import UserConsent
from app.repositories.consent_repository import ConsentRepository
from app.schemas.schema import UserConsentRequest, RevokeConsentRequest
from app.core.db import get_db
from app.service.services import record_consent, revoke_consent
from app.models.audit_logs import AuditLog
router = APIRouter(prefix="/api/v1/consent", tags=["Consent"])

@router.post("/consent/record")
def record_consent(payload: UserConsentRequest, db: Session = Depends(get_db)):
    
    user_exists = db.query(User).filter(User.id == payload.user_id).first()
    if not user_exists:
        raise HTTPException(
            status_code=400,
            detail="Invalid user_id. User does not exist."
        )
    
    if not payload.scroll_completed:
        raise HTTPException(
            status_code=400,
            detail="Please scroll through the entire document before accepting."
        )

    if not payload.accepted:
        raise HTTPException(
            status_code=400,
            detail="Consent not provided. Please accept to continue."
        )

    consent = UserConsent(
        user_id=payload.user_id,
        consent_type=payload.consent_type,
        version=payload.version,
        accepted=True,
        scroll_completed=True,
        device_info=payload.device_info,
        ip_address=payload.ip_address,
        accepted_at=datetime.utcnow()
    )

    db.add(consent)
    db.commit()
    db.refresh(consent)

    audit = AuditLog(
        action="CONSENT_ACCEPTED",
        user_id=payload.user_id,
        details=f"{payload.consent_type} v{payload.version} accepted"
    )
    db.add(audit)
    db.commit()

    return {"status": "success", "message": "Consent recorded successfully."}


@router.get("/history")
def get_consent_history(user_id: int, db: Session = Depends(get_db)):
    from app.models.user_consent import UserConsent
    
    user_exists = db.query(User).filter(User.id == user_id).first()
    if not user_exists:
        raise HTTPException(
            status_code=400,
            detail="Invalid user_id. User does not exist."
        )


    history = db.query(UserConsent).filter(UserConsent.user_id == user_id).all()

    if not history:
        return {"message": "No consent history found for this user."}

    return history

@router.post("/consent/revoke")
def revoke_consent(data: RevokeConsentRequest, db: Session = Depends(get_db)):
    
    user_exists = db.query(User).filter(User.id == data.user_id).first()
    if not user_exists:
        raise HTTPException(status_code=404, detail="User ID does not exist")
    
    consent = db.query(UserConsent).filter(
        UserConsent.user_id == data.user_id,
        UserConsent.consent_type == data.consent_type,
        UserConsent.revoked_at.is_(None)
    ).first()

    if not consent:
        raise HTTPException(status_code=404, detail="No active consent found to revoke")
    
    consent.revoked_at = datetime.utcnow()
    db.commit()
    db.refresh(consent)

    audit_log = AuditLog(
        action="CONSENT_REVOKED",
        user_id=data.user_id,
        details=f"Consent '{data.consent_type}' revoked"
    )
    db.add(audit_log)
    db.commit()

    return {"message": "Consent Revoked Successfully", "consent_id": consent.id}
