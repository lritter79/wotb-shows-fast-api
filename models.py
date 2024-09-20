from datetime import datetime
from typing import Union
from pydantic import BaseModel, Field


class Address(BaseModel):
    houseNumber: str
    streetName: str
    zipcode: str
    city: str
    state: str

class Show(BaseModel):
    id: str
    venueName: str
    address: Address
    otherBands: Union[list[str], None] = None
    entryTime: Union[datetime, None] = None
    startTime: datetime = Field(
        title="The start time of the show", 
        description="The time the show starts at in GMT", 
    )
    endTime: Union[datetime, None] = None
    timezone: str = Field(
        title="The timezone the show takes place in", 
        max_length=300,
        pattern="^[A-Za-z]+\/[A-Za-z_]+$"
    )
    ticketLink: Union[str, None] = None
    rvspLink: Union[str, None] = None
    isPast: Union[bool, None] = Field(default=None, deprecated=True)
    fbLink: Union[str, None] = None

    @staticmethod
    def from_doc(doc) -> "Show":
        return Show(
            id=str(doc["_id"]),
            venueName=doc["venueName"],
            address=doc["address"],
            otherBands=doc.get("otherBands"),
            entryTime=doc.get("entryTime"),
            startTime=doc["startTime"],
            endTime=doc.get("endTime"),
            timezone=doc["timezone"],
            ticketLink=doc.get("ticketLink"),
            rvspLink=doc.get("rvspLink"),
            isPast=doc.get("isPast"),
            fbLink=doc.get("fbLink"),
        )