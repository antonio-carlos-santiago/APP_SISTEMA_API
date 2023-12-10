from datetime import datetime

from flet import Column
from flet_core import ScrollMode, MainAxisAlignment, ExpansionPanel, ListTile, Text, ExpansionPanelList

from root_app import Consulta
from root_app.shared.database import SessionLocal

sessao = SessionLocal()

