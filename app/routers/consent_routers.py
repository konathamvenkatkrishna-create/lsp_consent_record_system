from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from app.models.audit_logs import AuditLog
from app.models.consent_master import ConsentMaster
from app.models.users import User
from app.models.user_consent import UserConsent
from app.schemas.schema import UserConsentRequest, RevokeConsentRequest
from app.core.db import get_db

router = APIRouter(prefix="/api/v1/consent", tags=["Consent"])


@router.post("/record")
def record_consent(
    payload: UserConsentRequest,
    request: Request,
    db: Session = Depends(get_db)
):


    user_exists = db.query(User).filter(User.id == payload.user_id).first()
    if not user_exists:
        raise HTTPException(
            status_code=400,
            detail="Invalid user_id. User does not exist."
        )

    # Scroll validation
    if not payload.scroll_completed:
        raise HTTPException(
            status_code=400,
            detail="Please scroll through the entire document before accepting."
        )

    # Explicit acceptance check
    if not payload.accepted:
        raise HTTPException(
            status_code=400,
            detail="Consent not provided. Please accept to continue."
        )

    # Prevent duplicate active consent
    existing = db.query(UserConsent).filter(
        UserConsent.user_id == payload.user_id,
        UserConsent.consent_type == payload.consent_type,
        UserConsent.revoked_at.is_(None)
    ).first()

    if existing:
        raise HTTPException(
            status_code=400,
            detail="Active consent already exists for this type."
        )

    #  Get latest version from ConsentMaster
    latest_doc = db.query(ConsentMaster).filter(
        ConsentMaster.type == payload.consent_type,
        ConsentMaster.active == True
    ).order_by(ConsentMaster.version.desc()).first()

    if not latest_doc:
        raise HTTPException(
            status_code=404,
            detail="Consent document not found."
        )

    # Create consent
    consent = UserConsent(
        user_id=payload.user_id,
        consent_type=payload.consent_type,
        version=latest_doc.version,
        accepted=True,
        scroll_completed=True,
        device_info=payload.device_info,
        ip_address=request.client.host
    )

    db.add(consent)
    db.commit()
    db.refresh(consent)

    #  Audit log
    audit = AuditLog(
        action="CONSENT_ACCEPTED",
        user_id=payload.user_id,
        details=f"{payload.consent_type} v{latest_doc.version} accepted from IP {request.client.host}"
    )
    db.add(audit)
    db.commit()

    return {
        "status": "success",
        "message": "Consent recorded successfully."
    }


@router.get("/history")
def get_consent_history(user_id: int, db: Session = Depends(get_db)):

    user_exists = db.query(User).filter(User.id == user_id).first()
    if not user_exists:
        raise HTTPException(
            status_code=400,
            detail="Invalid user_id. User does not exist."
        )

    history = db.query(UserConsent).filter(
        UserConsent.user_id == user_id
    ).all()

    if not history:
        return {"message": "No consent history found for this user."}

    return history


@router.post("/revoke")
def revoke_consent(
    data: RevokeConsentRequest,
    request: Request,
    db: Session = Depends(get_db)
):

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
        details=f"Consent '{data.consent_type}' revoked from IP {request.client.host}"
    )
    db.add(audit_log)
    db.commit()

    return {
        "message": "Consent Revoked Successfully",
        "consent_id": consent.id
    }
