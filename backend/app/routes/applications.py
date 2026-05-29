def create_application_route(payload: ApplicationCreate, db: Session = Depends(get_db)) -> ApplicationRead:
from app.routes.application import router
