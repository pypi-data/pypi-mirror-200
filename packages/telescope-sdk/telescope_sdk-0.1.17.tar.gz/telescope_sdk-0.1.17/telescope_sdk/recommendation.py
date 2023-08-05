from decimal import Decimal
from enum import Enum
from typing import Optional

from telescope_sdk.common import UserFacingDataType


class RecommendationStatus(str, Enum):
    ACCEPTED = 'ACCEPTED'
    REJECTED = 'REJECTED'
    SAVED = 'SAVED'
    PENDING = 'PENDING'


class RecommendationRejectionReason(str, Enum):
    NOT_RELEVANT = 'NOT_RELEVANT'
    WRONG_POSITION_RIGHT_COMPANY = 'WRONG_POSITION_RIGHT_COMPANY'
    RIGHT_POSITION_WRONG_COMPANY = 'RIGHT_POSITION_WRONG_COMPANY'
    EXISTING_CUSTOMER = 'EXISTING_CUSTOMER'
    ALREADY_CONTACTED = 'ALREADY_CONTACTED'
    OTHER = 'OTHER'
    DISCARDED = 'DISCARDED'


class Recommendation(UserFacingDataType):
    campaign_id: str
    person_id: str
    recommendation_reason: str = None
    status: RecommendationStatus
    resolved_at: str = None
    relevance: Decimal = None
    rejection_reason: Optional[RecommendationRejectionReason] = None
    free_text_rejection_reason: Optional[str] = None
