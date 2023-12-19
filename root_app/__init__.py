from root_app.shared.database import Base, engine
from root_app.configuracoes.home.models import *
from root_app.shared.models_config import *

Base.metadata.create_all(bind=engine)
