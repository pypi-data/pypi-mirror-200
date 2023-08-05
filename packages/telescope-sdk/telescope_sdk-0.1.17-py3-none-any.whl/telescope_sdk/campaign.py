from enum import Enum

from telescope_sdk.common import UserFacingDataType
from pydantic import BaseModel
from telescope_sdk.company import CompanySizeRange


class CampaignStatus(str, Enum):
    RUNNING = 'RUNNING'
    PAUSED = 'PAUSED'
    ERROR = 'ERROR'


class ExampleCompany(BaseModel):
    id: str
    name: str


class IdealCustomerProfile(BaseModel):
    example_companies: list[ExampleCompany]
    job_titles: list[str]
    keywords: list[str] = None
    negative_keywords: list[str] = None
    country_codes: list[list[str]] = None
    employee_country_codes: list[list[str]] = None
    industries: list[str] = None
    company_size_range: CompanySizeRange = None
    company_types: list[str] = None


class Campaign(UserFacingDataType):
    name: str
    status: CampaignStatus
    sequence_id: str
    replenish: bool
    icp: IdealCustomerProfile
