from pydantic import BaseModel

class Arguments(BaseModel):
    min_time_to_sleep: int
    max_time_to_sleep: int
    domain_root: str | None
    page_size: int
    username: str
    password: str
    dc_target: str
    ldap_attributes: list[str]
    filter: str | None
    function: str | None
    output: str
    breaks: list[list[str]]
    burst: int
    ssl: bool