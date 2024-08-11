from pydantic import BaseModel, Field
from typing import List, Optional, Dict

class Depiction(BaseModel):
    attribution: str
    imageUrl: str

class Term(BaseModel):
    chamber: str
    endYear: Optional[int]
    startYear: int

class Member(BaseModel):
    bioguideId: str
    depiction: Depiction
    district: Optional[str]
    name: str
    partyName: str
    state: str
    terms: List[Term]
    updateDate: str
    url: str

class MembersResponse(BaseModel):
    members: List[Member]

class Action(BaseModel):
    actionCode: str
    actionDate: str
    sourceSystem: Dict[str, str]
    text: str
    type: str

class BillActionResponse(BaseModel):
    actions: List[Action]

class Amendment(BaseModel):
    congress: int
    description: str
    latestAction: Dict[str, str]
    number: str
    type: str
    updateDate: str
    url: str

class BillAmendmentResponse(BaseModel):
    amendments: List[Amendment]

class CommitteeActivity(BaseModel):
    date: str
    name: str

class Committee(BaseModel):
    activities: List[CommitteeActivity]
    chamber: str
    name: str
    systemCode: str
    type: str
    url: str

class BillCommitteeResponse(BaseModel):
    committees: List[Committee]

class Cosponsor(BaseModel):
    bioguideId: str
    district: Optional[int]
    firstName: str
    fullName: str
    isOriginalCosponsor: bool
    lastName: str
    middleName: Optional[str]
    party: str
    sponsorshipDate: str
    state: str
    url: str

class BillCosponsorResponse(BaseModel):
    cosponsors: List[Cosponsor]

class RelatedBill(BaseModel):
    congress: int
    latestAction: Dict[str, str]
    number: int
    relationshipDetails: List[Dict[str, str]]
    title: str
    type: str
    url: str

class BillRelatedResponse(BaseModel):
    relatedBills: List[RelatedBill]

class Subject(BaseModel):
    name: str
    updateDate: str

class PolicyArea(BaseModel):
    name: str

class BillSubjectResponse(BaseModel):
    subjects: Dict[str, List[Subject]]
    policyArea: PolicyArea

class Summary(BaseModel):
    actionDate: str
    actionDesc: str
    text: str
    updateDate: str
    versionCode: str

class BillSummaryResponse(BaseModel):
    summaries: List[Summary]

class TextFormat(BaseModel):
    type: str
    url: str

class TextVersion(BaseModel):
    date: Optional[str]
    formats: List[TextFormat]
    type: str

class BillTextResponse(BaseModel):
    textVersions: List[TextVersion]

class Title(BaseModel):
    title: str
    titleType: str
    titleTypeCode: int
    updateDate: str

class BillTitleResponse(BaseModel):
    titles: List[Title]

class CommitteePrint(BaseModel):
    chamber: str
    congress: int
    jacketNumber: int
    updateDate: str
    url: str

class CommitteePrintResponse(BaseModel):
    committeePrints: List[CommitteePrint]

class CommitteeMeeting(BaseModel):
    chamber: str
    congress: int
    eventId: str
    updateDate: str
    url: str

class CommitteeMeetingResponse(BaseModel):
    committeeMeetings: List[CommitteeMeeting]

class Communication(BaseModel):
    chamber: str
    communicationType: Dict[str, str]
    congressNumber: int
    number: str
    reportNature: str
    submittingAgency: str
    submittingOfficial: str
    updateDate: str
    url: str

class CommunicationResponse(BaseModel):
    houseCommunications: List[Communication]

class SenateCommunicationResponse(BaseModel):
    senateCommunications: List[Communication]

# Example Request Models
class MemberSearchRequest(BaseModel):
    name: str = Field(..., description="The name of the member of Congress to search for.")

class MemberDetailsRequest(BaseModel):
    member_id: str = Field(..., description="The ID of the member of Congress to get details for.")

class ChatRequest(BaseModel):
    question: str = Field(..., description="The question to ask about the member of Congress.")
    member_id: str = Field(..., description="The ID of the member of Congress to chat about.")

class BillRequest(BaseModel):
    congress: int = Field(..., description="The congress number.")
    bill_type: str = Field(..., description="The bill type (e.g., hr, s, hres, sres).")
    bill_number: int = Field(..., description="The bill number.")

class CommitteePrintRequest(BaseModel):
    congress: int = Field(..., description="The congress number.")
    chamber: str = Field(..., description="The chamber name. Value can be house, senate, or nochamber.")
    jacket_number: int = Field(..., description="The jacket number for the print.")

class CommitteeMeetingRequest(BaseModel):
    congress: int = Field(..., description="The congress number.")
    chamber: str = Field(..., description="The chamber name. Value can be house, senate, or nochamber.")
    event_id: str = Field(..., description="The event identifier.")

class CommunicationRequest(BaseModel):
    congress: int = Field(..., description="The congress number.")
    communication_type: str = Field(..., description="The type of communication. Value can be ec, ml, pm, or pt.")
    communication_number: int = Field(..., description="The communication’s assigned number.")
