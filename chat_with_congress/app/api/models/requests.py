from pydantic import BaseModel, Field
from typing import List, Optional, Union, Dict

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
    district: Optional[Union[int, str]] = Field(None, description="The district the member represents.")  # Allow both int and str
    name: str = Field(..., description="The full name of the member.")
    partyName: str = Field(..., description="The political party the member belongs to.")
    state: str = Field(..., description="The state the member represents.")
    terms: Union[List[Term], Dict[str, List[Term]]] = Field(..., description="A list of terms served by the member.")  # Handle list or dict
    updateDate: str = Field(..., description="The last update date for the member's information.")
    url: str = Field(..., description="The URL to the member's profile.")

class MemberDetailsResponse(BaseModel):
    bioguideId: str = Field(..., description="The unique identifier assigned to a member of Congress.")
    birthYear: Optional[str] = Field(None, description="The birth year of the member.")
    deathYear: Optional[str] = Field(None, description="The death year of the member.")
    currentMember: Optional[bool] = Field(None, description="Indicates if the person is a current member of Congress.")
    depiction: Optional[Depiction] = Field(None, description="An object containing the member's image URL and attribution.")
    directOrderName: Optional[str] = Field(None, description="The member's full name in direct order (First Last).")
    firstName: Optional[str] = Field(None, description="The member's first name.")
    honorificName: Optional[str] = Field(None, description="The honorific title used for the member (e.g., Mr., Mrs.).")
    invertedOrderName: Optional[str] = Field(None, description="The member's full name in inverted order (Last, First).")
    lastName: Optional[str] = Field(None, description="The member's last name.")
    leadership: Optional[List[Dict[str, str]]] = Field(None, description="A list of leadership roles held by the member, including the Congress number and role type.")
    
    # Update here: startYear should be an integer if that's what's being returned by the API
    partyHistory: Optional[List[Dict[str, Union[str, int]]]] = Field(None, description="A list of the member's party affiliations over time.")
    
    sponsoredLegislation: Optional[Dict[str, Union[int, str]]] = Field(None, description="A dictionary containing information on legislation sponsored by the member, including count and URL.")
    cosponsoredLegislation: Optional[Dict[str, Union[int, str]]] = Field(None, description="A dictionary containing information on legislation cosponsored by the member, including count and URL.")
    state: Optional[str] = Field(None, description="The state that the member represents.")
    district: Optional[int] = Field(None, description="The district number of the member.")
    terms: Optional[List[Term]] = Field(None, description="A list of terms served by the member in Congress.")
    officialWebsiteUrl: Optional[str] = Field(None, description="The official website URL of the member.")
    updateDate: Optional[str] = Field(None, description="The date when the member's information was last updated.")



class MembersResponse(BaseModel):
    members: List[Member] = Field(..., description="A list of members matching the search criteria.")

class SourceSystem(BaseModel):
    code: Optional[int] = Field(None, description="Source system code.")  # Optional with default None
    name: str = Field(..., description="Source system name.")

class Action(BaseModel):
    actionCode: Optional[str] = Field(None, description="Code representing the type of action.")  # Optional with default None
    actionDate: str = Field(..., description="Date the action took place.")
    sourceSystem: SourceSystem = Field(..., description="Details about the source system.")
    text: str = Field(..., description="Description of the action.")
    type: str = Field(..., description="Type of action performed.")

class BillActionResponse(BaseModel):
    actions: List[Action] = Field(..., description="A list of actions taken on the bill.")

class LatestAction(BaseModel):
    actionDate: Optional[str] = Field(None, description="The date when the latest action occurred.")  # Optional
    actionTime: Optional[str] = Field(None, description="The time when the latest action occurred.")  # Optional
    text: Optional[str] = Field(None, description="The description of the latest action.")  # Optional

class Amendment1(BaseModel):
    congress: int = Field(..., description="The congress number in which the amendment was introduced.")
    description: Optional[str] = Field(None, description="A description of the amendment.")  # Optional
    latestAction: Optional[LatestAction] = Field(None, description="The latest action taken on the amendment.")  # Optional
    number: str = Field(..., description="The amendment number.")
    type: str = Field(..., description="The type of the amendment.")
    updateDate: str = Field(..., description="The date the amendment was last updated.")
    url: str = Field(..., description="The URL to the amendment details.")

class BillAmendmentResponse(BaseModel):
    amendments: List[Amendment1] = Field(..., description="A list of amendments to the bill.")

class CommitteeActivity(BaseModel):
    date: str = Field(..., description="The date of the committee's activity.")
    name: str = Field(..., description="The name of the committee activity.")



class CommitteeHistory(BaseModel):
    committeeTypeCode: str = Field(..., description="The type of the committee.")
    establishingAuthority: Optional[str] = Field(None, description="The authority that established the committee.")
    libraryOfCongressName: str = Field(..., description="The Library of Congress name for the committee.")
    locLinkedDataId: Optional[str] = Field(None, description="The Linked Data ID from LOC.")
    naraId: Optional[str] = Field(None, description="The National Archives and Records Administration ID.")
    officialName: str = Field(..., description="The official name of the committee.")
    startDate: str = Field(..., description="The start date of the committee.")
    endDate: Optional[str] = Field(None, description="The end date of the committee.")
    superintendentDocumentNumber: Optional[str] = Field(None, description="The superintendent document number.")
    updateDate: str = Field(..., description="The date when the record was last updated.")

class Subcommittee(BaseModel):
    name: str = Field(..., description="The name of the subcommittee.")
    systemCode: str = Field(..., description="The system code for the subcommittee.")
    url: str = Field(..., description="The URL to the subcommittee details.")

class Committee(BaseModel):
    systemCode: str = Field(..., description="The system code for the committee.")
    type: str = Field(..., description="The type of committee (e.g., standing, select).")
    updateDate: str = Field(..., description="The date when the committee was last updated.")
    isCurrent: bool = Field(..., description="Indicates whether the committee is current.")
    history: List[CommitteeHistory] = Field(..., description="The history of the committee.")
    subcommittees: List[Subcommittee] = Field(..., description="A list of subcommittees under the committee.")
    bills: Optional[dict] = Field(None, description="Information about bills handled by the committee.")
    communications: Optional[dict] = Field(None, description="Information about communications handled by the committee.")
    reports: Optional[dict] = Field(None, description="Information about reports handled by the committee.")

class CommitteeResponse(BaseModel):
    committee: Committee = Field(..., description="Details about the specific committee.")



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

class CommunicationType(BaseModel):
    code: str = Field(..., description="The code representing the type of communication.")
    name: str = Field(..., description="The name of the communication type.")

class Communication(BaseModel):
    chamber: str = Field(..., description="The chamber related to the communication.")
    communicationType: CommunicationType = Field(..., description="Details of the communication type.")
    congress: int = Field(..., description="The congress number related to the communication.")
    number: Union[str, int] = Field(..., description="The communication number.")  # Accepts both str and int
    reportNature: Optional[str] = Field(None, description="The nature of the communication report.")
    submittingAgency: Optional[str] = Field(None, description="The agency that submitted the communication.")
    submittingOfficial: Optional[str] = Field(None, description="The official who submitted the communication.")
    updateDate: str = Field(..., description="The date the communication was last updated.")
    url: str = Field(..., description="The URL to the communication details.")

class Pagination(BaseModel):
    count: Union[str, int] = Field(..., description="The total number of items.")  # Accepts both str and int
    next: Optional[str] = Field(None, description="The URL to the next page of results.")

class CommunicationResponse(BaseModel):
    houseCommunications: List[Communication] = Field(..., description="A list of House communications based on the specified parameters.")
    pagination: Optional[Pagination] = Field(None, description="Pagination details for the response.")
    request: Optional[Dict[str, str]] = Field(None, description="Request details included in the response.")

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


class ChatResponse(BaseModel):
    response: str = Field(..., description="The response generated from the chat based on the member's information.")
    score: float = Field(..., description="The relevance score of the response based on the semantic search.")



# Models for nested structures

class Action(BaseModel):
    count: int = Field(..., description="Number of actions.")
    url: str = Field(..., description="URL to retrieve actions.")

class Amendment(BaseModel):
    count: int = Field(..., description="Number of amendments.")
    url: str = Field(..., description="URL to retrieve amendments.")

class CboCostEstimate(BaseModel):
    description: str = Field(..., description="Description of the CBO cost estimate.")
    pubDate: str = Field(..., description="Publication date of the estimate.")
    title: str = Field(..., description="Title of the estimate.")
    url: str = Field(..., description="URL to the full estimate.")

class CommitteeReport(BaseModel):
    citation: str = Field(..., description="Citation for the committee report.")
    url: str = Field(..., description="URL to retrieve the report.")

class Committee(BaseModel):
    count: int = Field(..., description="Number of committees.")
    url: str = Field(..., description="URL to retrieve committees.")

class Cosponsor(BaseModel):
    count: int = Field(..., description="Number of cosponsors.")
    countIncludingWithdrawnCosponsors: int = Field(..., description="Total number including withdrawn cosponsors.")
    url: str = Field(..., description="URL to retrieve cosponsors.")

class LatestAction(BaseModel):
    actionDate: str = Field(..., description="Date of the latest action.")
    text: str = Field(..., description="Text describing the latest action.")

class Law(BaseModel):
    number: str = Field(..., description="Law number.")
    type: str = Field(..., description="Type of law (e.g., Public Law).")

class PolicyArea(BaseModel):
    name: str = Field(..., description="Name of the policy area.")

class RelatedBill(BaseModel):
    count: int = Field(..., description="Number of related bills.")
    url: str = Field(..., description="URL to retrieve related bills.")

class Sponsor(BaseModel):
    bioguideId: str = Field(..., description="Biographical ID of the sponsor.")
    district: Optional[int] = Field(None, description="District of the sponsor.")
    firstName: str = Field(..., description="First name of the sponsor.")
    fullName: str = Field(..., description="Full name of the sponsor.")
    isByRequest: str = Field(..., description="Indicates if the sponsor was by request.")
    lastName: str = Field(..., description="Last name of the sponsor.")
    middleName: Optional[str] = Field(None, description="Middle name of the sponsor.")
    party: str = Field(..., description="Party of the sponsor.")
    state: str = Field(..., description="State of the sponsor.")
    url: str = Field(..., description="URL to retrieve sponsor details.")

class Subject(BaseModel):
    count: int = Field(..., description="Number of subjects.")
    url: str = Field(..., description="URL to retrieve subjects.")

class Summary(BaseModel):
    count: int = Field(..., description="Number of summaries.")
    url: str = Field(..., description="URL to retrieve summaries.")

class TextVersion(BaseModel):
    count: int = Field(..., description="Number of text versions.")
    url: str = Field(..., description="URL to retrieve text versions.")

class Title(BaseModel):
    count: int = Field(..., description="Number of titles.")
    url: str = Field(..., description="URL to retrieve titles.")

# Main Bill model

class Bill(BaseModel):
    actions: Action = Field(..., description="Bill actions details.")
    amendments: Amendment = Field(..., description="Bill amendments details.")
    cboCostEstimates: List[CboCostEstimate] = Field(..., description="CBO cost estimates for the bill.")
    committeeReports: List[CommitteeReport] = Field(..., description="Committee reports for the bill.")
    committees: Committee = Field(..., description="Committees related to the bill.")
    congress: int = Field(..., description="Congress number.")
    constitutionalAuthorityStatementText: str = Field(..., description="Constitutional authority statement text.")
    cosponsors: Cosponsor = Field(..., description="Cosponsors details.")
    introducedDate: str = Field(..., description="Date the bill was introduced.")
    latestAction: LatestAction = Field(..., description="Latest action taken on the bill.")
    laws: List[Law] = Field(..., description="Laws associated with the bill.")
    number: str = Field(..., description="Bill number.")
    originChamber: str = Field(..., description="Chamber where the bill originated.")
    policyArea: PolicyArea = Field(..., description="Policy area of the bill.")
    relatedBills: RelatedBill = Field(..., description="Related bills information.")
    sponsors: List[Sponsor] = Field(..., description="Sponsors of the bill.")
    subjects: Subject = Field(..., description="Subjects related to the bill.")
    summaries: Summary = Field(..., description="Summaries of the bill.")
    textVersions: TextVersion = Field(..., description="Text versions of the bill.")
    title: str = Field(..., description="Title of the bill.")
    titles: Title = Field(..., description="Bill titles details.")
    type: str = Field(..., description="Type of the bill (e.g., HR, S).")
    updateDate: str = Field(..., description="Date when the bill was last updated.")
    updateDateIncludingText: str = Field(..., description="Date when the bill text was last updated.")

# Response model

class BillDetailResponse(BaseModel):
    bill: Bill = Field(..., description="Detailed information about the bill.")
