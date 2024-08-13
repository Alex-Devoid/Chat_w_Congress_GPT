from pydantic import BaseModel, Field
from typing import List, Optional, Dict

class Depiction(BaseModel):
    attribution: str = Field(..., description="The attribution for the member's image.")
    imageUrl: str = Field(..., description="The URL of the member's image.")

class Term(BaseModel):
    chamber: str = Field(..., description="The chamber in which the member served.")
    endYear: Optional[int] = Field(None, description="The year the term ended.")
    startYear: int = Field(..., description="The year the term started.")

class Member(BaseModel):
    bioguideId: str = Field(..., description="The unique identifier assigned to a member of Congress.")
    depiction: Depiction = Field(..., description="The member's depiction object.")
    district: Optional[str] = Field(None, description="The district the member represents.")
    name: str = Field(..., description="The full name of the member.")
    partyName: str = Field(..., description="The political party the member belongs to.")
    state: str = Field(..., description="The state the member represents.")
    terms: List[Term] = Field(..., description="A list of terms served by the member.")
    updateDate: str = Field(..., description="The last update date for the member's information.")
    url: str = Field(..., description="The URL to the member's profile.")

class MembersResponse(BaseModel):
    members: List[Member] = Field(..., description="A list of members matching the search criteria.")

class Action(BaseModel):
    actionCode: str = Field(..., description="The code representing the type of action.")
    actionDate: str = Field(..., description="The date the action took place.")
    sourceSystem: Dict[str, str] = Field(..., description="Information about the system that provided the action data.")
    text: str = Field(..., description="A description of the action.")
    type: str = Field(..., description="The type of action performed.")

class BillActionResponse(BaseModel):
    actions: List[Action] = Field(..., description="A list of actions taken on the bill.")

class Amendment(BaseModel):
    congress: int = Field(..., description="The congress number in which the amendment was introduced.")
    description: str = Field(..., description="A description of the amendment.")
    latestAction: Dict[str, str] = Field(..., description="The latest action taken on the amendment.")
    number: str = Field(..., description="The amendment number.")
    type: str = Field(..., description="The type of the amendment.")
    updateDate: str = Field(..., description="The date the amendment was last updated.")
    url: str = Field(..., description="The URL to the amendment details.")

class BillAmendmentResponse(BaseModel):
    amendments: List[Amendment] = Field(..., description="A list of amendments to the bill.")

class CommitteeActivity(BaseModel):
    date: str = Field(..., description="The date of the committee's activity.")
    name: str = Field(..., description="The name of the committee activity.")

class Committee(BaseModel):
    activities: List[CommitteeActivity] = Field(..., description="A list of activities performed by the committee.")
    chamber: str = Field(..., description="The chamber the committee belongs to.")
    name: str = Field(..., description="The name of the committee.")
    systemCode: str = Field(..., description="The system code for the committee.")
    type: str = Field(..., description="The type of committee (e.g., standing, select).")
    url: str = Field(..., description="The URL to the committee details.")

class BillCommitteeResponse(BaseModel):
    committees: List[Committee] = Field(..., description="A list of committees associated with the bill.")

class Cosponsor(BaseModel):
    bioguideId: str = Field(..., description="The unique identifier of the cosponsor.")
    district: Optional[int] = Field(None, description="The district the cosponsor represents.")
    firstName: str = Field(..., description="The first name of the cosponsor.")
    fullName: str = Field(..., description="The full name of the cosponsor.")
    isOriginalCosponsor: bool = Field(..., description="Indicates if the cosponsor is an original cosponsor.")
    lastName: str = Field(..., description="The last name of the cosponsor.")
    middleName: Optional[str] = Field(None, description="The middle name of the cosponsor.")
    party: str = Field(..., description="The political party of the cosponsor.")
    sponsorshipDate: str = Field(..., description="The date the cosponsor signed onto the bill.")
    state: str = Field(..., description="The state the cosponsor represents.")
    url: str = Field(..., description="The URL to the cosponsor's details.")

class BillCosponsorResponse(BaseModel):
    cosponsors: List[Cosponsor] = Field(..., description="A list of cosponsors of the bill.")

class RelatedBill(BaseModel):
    congress: int = Field(..., description="The congress number related to the bill.")
    latestAction: Dict[str, str] = Field(..., description="The latest action taken on the related bill.")
    number: int = Field(..., description="The number of the related bill.")
    relationshipDetails: List[Dict[str, str]] = Field(..., description="Details of the relationship between the bills.")
    title: str = Field(..., description="The title of the related bill.")
    type: str = Field(..., description="The type of the related bill.")
    url: str = Field(..., description="The URL to the related bill details.")

class BillRelatedResponse(BaseModel):
    relatedBills: List[RelatedBill] = Field(..., description="A list of bills related to the specified bill.")

class Subject(BaseModel):
    name: str = Field(..., description="The name of the legislative subject.")
    updateDate: str = Field(..., description="The date the subject was last updated.")

class PolicyArea(BaseModel):
    name: str = Field(..., description="The name of the policy area.")

class BillSubjectResponse(BaseModel):
    subjects: Dict[str, List[Subject]] = Field(..., description="A dictionary of subjects related to the bill.")
    policyArea: PolicyArea = Field(..., description="The policy area related to the bill.")

class Summary(BaseModel):
    actionDate: str = Field(..., description="The date the summary was created.")
    actionDesc: str = Field(..., description="A description of the summary's action.")
    text: str = Field(..., description="The text of the summary.")
    updateDate: str = Field(..., description="The date the summary was last updated.")
    versionCode: str = Field(..., description="The version code of the summary.")

class BillSummaryResponse(BaseModel):
    summaries: List[Summary] = Field(..., description="A list of summaries for the bill.")

class TextFormat(BaseModel):
    type: str = Field(..., description="The type of the text format (e.g., PDF, HTML).")
    url: str = Field(..., description="The URL to the text format.")

class TextVersion(BaseModel):
    date: Optional[str] = Field(None, description="The date the text version was created.")
    formats: List[TextFormat] = Field(..., description="A list of formats for the text version.")
    type: str = Field(..., description="The type of the text version (e.g., introduced, enrolled).")

class BillTextResponse(BaseModel):
    textVersions: List[TextVersion] = Field(..., description="A list of text versions for the bill.")

class Title(BaseModel):
    title: str = Field(..., description="The title of the bill.")
    titleType: str = Field(..., description="The type of the title (e.g., short, official).")
    titleTypeCode: int = Field(..., description="The code representing the title type.")
    updateDate: str = Field(..., description="The date the title was last updated.")

class BillTitleResponse(BaseModel):
    titles: List[Title] = Field(..., description="A list of titles for the bill.")

class CommitteePrint(BaseModel):
    chamber: str = Field(..., description="The chamber the committee print is associated with.")
    congress: int = Field(..., description="The congress number related to the committee print.")
    jacketNumber: int = Field(..., description="The jacket number for the committee print.")
    updateDate: str = Field(..., description="The date the committee print was last updated.")
    url: str = Field(..., description="The URL to the committee print details.")

class CommitteePrintResponse(BaseModel):
    committeePrints: List[CommitteePrint] = Field(..., description="A list of committee prints related to the specified parameters.")

class CommitteeMeeting(BaseModel):
    chamber: str = Field(..., description="The chamber where the meeting took place.")
    congress: int = Field(..., description="The congress number related to the committee meeting.")
    eventId: str = Field(..., description="The event identifier for the committee meeting.")
    updateDate: str = Field(..., description="The date the committee meeting was last updated.")
    url: str = Field(..., description="The URL to the committee meeting details.")

class CommitteeMeetingResponse(BaseModel):
    committeeMeetings: List[CommitteeMeeting] = Field(..., description="A list of committee meetings based on the specified parameters.")

class Communication(BaseModel):
    chamber: str = Field(..., description="The chamber related to the communication.")
    communicationType: Dict[str, str] = Field(..., description="The type of communication.")
    congressNumber: int = Field(..., description="The congress number related to the communication.")
    number: str = Field(..., description="The communication number.")
    reportNature: str = Field(..., description="The nature of the communication report.")
    submittingAgency: str = Field(..., description="The agency that submitted the communication.")
    submittingOfficial: str = Field(..., description="The official who submitted the communication.")
    updateDate: str = Field(..., description="The date the communication was last updated.")
    url: str = Field(..., description="The URL to the communication details.")

class CommunicationResponse(BaseModel):
    houseCommunications: List[Communication] = Field(..., description="A list of House communications based on the specified parameters.")

class SenateCommunicationResponse(BaseModel):
    senateCommunications: List[Communication] = Field(..., description="A list of Senate communications based on the specified parameters.")

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

class CommitteeRequest(BaseModel):
    congress: int = Field(..., description="The congress number.")
    chamber: str = Field(..., description="The chamber name. Value can be house, senate, or nochamber.")
    committeeCode: str = Field(..., description="The committee code to retrieve details.")

class CommunicationRequest(BaseModel):
    congress: int = Field(..., description="The congress number.")
    communication_type: str = Field(..., description="The type of communication. Value can be ec, ml, pm, or pt.")
    communication_number: int = Field(..., description="The communication’s assigned number.")

class MemberDetailsResponse(BaseModel):
    bioguideId: str = Field(..., description="The unique identifier assigned to a member of Congress.")
    birthYear: Optional[str] = Field(None, description="The birth year of the member.")
    depiction: Optional[Depiction] = Field(None, description="An object containing the member's image URL and attribution.")
    directOrderName: Optional[str] = Field(None, description="The member's full name in direct order (First Last).")
    firstName: Optional[str] = Field(None, description="The member's first name.")
    honorificName: Optional[str] = Field(None, description="The honorific title used for the member (e.g., Mr., Mrs.).")
    invertedOrderName: Optional[str] = Field(None, description="The member's full name in inverted order (Last, First).")
    lastName: Optional[str] = Field(None, description="The member's last name.")
    leadership: Optional[List[Dict[str, str]]] = Field(None, description="A list of leadership roles held by the member, including the Congress number and role type.")
    partyHistory: Optional[List[Dict[str, str]]] = Field(None, description="A list of the member's party affiliations over time.")
    sponsoredLegislation: Optional[Dict[str, str]] = Field(None, description="A dictionary containing information on legislation sponsored by the member, including count and URL.")
    cosponsoredLegislation: Optional[Dict[str, str]] = Field(None, description="A dictionary containing information on legislation cosponsored by the member, including count and URL.")
    state: Optional[str] = Field(None, description="The state that the member represents.")
    terms: Optional[List[Term]] = Field(None, description="A list of terms served by the member in Congress.")
    updateDate: Optional[str] = Field(None, description="The date when the member's information was last updated.")

class ChatResponse(BaseModel):
    response: str = Field(..., description="The response generated from the chat based on the member's information.")
    score: float = Field(..., description="The relevance score of the response based on the semantic search.")
