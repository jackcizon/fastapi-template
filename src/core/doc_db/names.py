from dataclasses import dataclass


@dataclass
class DataBases:
    admin: str = "admin"
    local: str = "local"
    config: str = "config"


doc_db = DataBases()
