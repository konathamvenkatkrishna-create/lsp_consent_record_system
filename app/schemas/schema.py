from pydantic import BaseModel
class ConsentMasterCreate(BaseModel):
    type: str
    version: str
    content: str
    active: bool = True

class UserConsentRequest(BaseModel):
    user_id: int
    consent_type: str                
    accepted: bool                    
    scroll_completed: bool            
    ip_address: str | None = None
    device_info: str | None = None

