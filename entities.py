from sqlalchemy import ForeignKey, DateTime
from sqlalchemy.orm import DeclarativeBase, relationship, Mapped, mapped_column
from sqlalchemy.sql import func
from typing import List
from datetime import datetime

import utils

class Base(DeclarativeBase):
    
    def __eq__(self, other):
        return str(self) == str(other)
     
    def __hash__(self):
        return hash(str(self))
    
class Activity(Base):

    __tablename__ = 'activities'

    activity_id: Mapped[str] = mapped_column(primary_key=True)
    visitor_id: Mapped[str] = mapped_column(ForeignKey('target_population.visitor_id'), index=True)
    clicked_dt: Mapped[datetime] = mapped_column()
    clicked_campaign: Mapped[str] = mapped_column(ForeignKey('campaigns.campaign_id'), index=True)
    clicked_channel: Mapped[str] = mapped_column(ForeignKey('channels.channel_id'), index=True)

    def __repr__(self):
        return f'ac_{self.activity_id}'

class Application(Base):

    __tablename__ = 'applications'

    application_id: Mapped[str] = mapped_column(primary_key=True)
    status_dt: Mapped[datetime] = mapped_column(primary_key=True) # require if we want to tie it back to activities
    status: Mapped[str] = mapped_column() # does it capture conversion?
    visitor_id: Mapped[str] = mapped_column(ForeignKey('visitors.visitor_id'))
    conversion_flag: Mapped[bool] = mapped_column(default=False) # necessary if we have status?

    # missing these columns?
    campaign_id: Mapped[str] = mapped_column(ForeignKey('campaigns.campaign_id'))
    channel_id: Mapped[str] = mapped_column(ForeignKey('channels.channel_id'))

    def __repr__(self):
        return f'ap_{self.application_id}_{self.status_dt.strftime(utils.DATETIME_FORMAT)}'

# eligibility table?
class TargetPopulation(Base):

    __tablename__ = 'target_population'
    # should there be an cus_id?

    visitor_id: Mapped[str] = mapped_column(ForeignKey('visitors.visitor_id'), primary_key=True)
    # don't we need the columns below?
    campaign_id: Mapped[str] = mapped_column(ForeignKey('campaigns.campaign_id'), primary_key=True)
    channel_id: Mapped[str] = mapped_column(ForeignKey('channels.channel_id'), primary_key=True)

    resp_prob: Mapped[float] = mapped_column(default=0.0) # soft pull
    conv_prob: Mapped[float] = mapped_column(default=0.0) # hard pull
    cus_value: Mapped[float] = mapped_column(default=0.0) # null for prospect?

    eligibility_flag: Mapped[bool] = mapped_column(default=False)
    expected_approval_rate: Mapped[float] = mapped_column(default=0.0)


    def __repr__(self):
        return f'tp_{self.visitor_id}_{self.spend_id}'

# campaign?
class MarketingSpend(Base):

    __tablename__ = 'marketing_spend'

    # !!!!! depends on if campaign_id encodes channel
    campaign_id: Mapped[str] = mapped_column(ForeignKey('campaigns.campaign_id'), primary_key=True) # same ID across channels?
    channel_id: Mapped[str] = mapped_column(ForeignKey('channels.channel_id'), primary_key=True)

    # how does channel spend come about at the campaign level?
    channel_spend: Mapped[float] = mapped_column(default=0.0)
    campaign_spend: Mapped[float] = mapped_column(default=0.0)
    start_dt: Mapped[datetime] = mapped_column(nullable=True) # what does it refer to?
    end_dt: Mapped[datetime] = mapped_column(nullable=True) # what does it refer to?

    def __repr__(self):
        return f'ms_{self.spend_id}'

class Channel(Base):

    __tablename__ = 'channels'

    channel_id: Mapped[str] = mapped_column(primary_key=True)
    channel_name: Mapped[str] = mapped_column(default='')

    def __repr__(self):
        return f'h_{self.channel_id}'

# ! could be duplicated depending on what marketing spend actually is
class Campaign(Base):

    __tablename__ = 'campaigns'

    campaign_id: Mapped[str] = mapped_column(primary_key=True)
    campaign_name: Mapped[str] = mapped_column(default='')

    # ! may need additional attribution for similarity

    def __repr__(self):
        return f'c_{self.campaign_id}'

class Visitor(Base):

    __tablename__ = 'visitors'

    visitor_id: Mapped[str] = mapped_column(primary_key=True)
    customer_id: Mapped[str] = mapped_column(ForeignKey('customers.customer_id'), nullable=True)

    # ! need additional attribution for similarity
    
    def __repr__(self):
        return f'v_{self.visitor_id}'

class Customer(Base):

    __tablename__ = 'customers'

    customer_id: Mapped[str] = mapped_column(primary_key=True)

    # ! need additional attribution for similarity

    def __repr__(self):
        return f'u_{self.customer_id}'