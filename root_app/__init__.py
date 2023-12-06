from root_app.shared.database import Base, engine
from root_app.configuracoes.home.models import *

Base.metadata.create_all(bind=engine)
