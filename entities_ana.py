from sqlalchemy import ForeignKey, DateTime
from sqlalchemy.orm import DeclarativeBase, relationship, Mapped, mapped_column
from sqlalchemy.sql import func
from typing import List
from datetime import datetime, date

import utils

class Base(DeclarativeBase):
    
    def __eq__(self, other):
        return str(self) == str(other)
     
    def __hash__(self):
        return hash(str(self))

class Visitor(Base):

    __tablename__ = 'visitors'

    visitor_key: Mapped[int] = mapped_column(primary_key=True)
    cims_acct_key: Mapped[int] = mapped_column(ForeignKey('card_members.cims_acct_key'))
    dpl_acct_key: Mapped[int] = mapped_column(ForeignKey('dpl_customers.dpl_acct_key'))

class CardMember(Base):

    __tablename__ = 'card_members'

    cims_acct_key: Mapped[int] = mapped_column(primary_key=True)

    # can a card member have multiple email address?
    email_address: Mapped[str] = mapped_column()
    email_opted_out: Mapped[bool] = mapped_column()

class DPLCustomer(Base):

    __tablename__ = 'dpl_customers'
    
    dpl_acct_key: Mapped[int] = mapped_column(primary_key=True)

class RiskEligibility(Base):

    # history or future?
    __tablename__ = 'risk_eligibilities'

    # how about eligibility for DPL customers?

    cims_acct_key: Mapped[str] = mapped_column(ForeignKey('card_members.cims_acct_key'), primary_key=True)
    perf_week: Mapped[date] = mapped_column(primary_key=True)

    risk_elig: Mapped[bool] = mapped_column()
    risk_non_elig_reason: Mapped[str] = mapped_column()

class MarketEligibility(Base):

    __tablename__ = 'market_eligibilities'

    # how about eligibility for DPL customers?
    cims_acct_key: Mapped[str] = mapped_column(ForeignKey('card_members.cims_acct_key'), primary_key=True)
    perf_week: Mapped[date] = mapped_column(primary_key=True)

    market_elig: Mapped[bool] = mapped_column()
    market_nonelig_reason: Mapped[str] = mapped_column()

class OfferEligibility(Base):

    # channel eligibilities?
    __tablename__ = 'offer_eligibilities'

    cims_acct_key: Mapped[int] = mapped_column(ForeignKey('card_members.cims_acct_key'), primary_key=True)
    perf_week: Mapped[date] = mapped_column(primary_key=True)
    # channel_id: Mapped[str] = mapped_column(ForeignKey('channels.channel_id'), primary_key=True)

    # can a customer receive multiple offer id in a week (primary key)?
    offer_id: Mapped[str] = mapped_column(ForeignKey('offers.offer_id'))
    offer_elig: Mapped[bool] = mapped_column()
    # missing this?
    respond_score: Mapped[float] = mapped_column(default=0.0)
    conversion_score: Mapped[float] = mapped_column(default=0.0)
    ltv_score: Mapped[float] = mapped_column(default=0.0)

class CampaignEligibility(Base):
    # missing this?
    __tablename__ = 'campaign_eligibilities'

    visitor_key: Mapped[int] = mapped_column(ForeignKey('visitors.visitor_key'), primary_key=True)
    perf_week: Mapped[date] = mapped_column(primary_key=True)
    # channel_id: Mapped[str] = mapped_column(ForeignKey('channels.channel_id'), primary_key=True)
    campaign_id: Mapped[str] = mapped_column(ForeignKey('campaigns.campaign_id'))
    campaign_elig: Mapped[bool] = mapped_column()
    respond_score: Mapped[float] = mapped_column(default=0.0)
    conversion_score: Mapped[float] = mapped_column(default=0.0)
    ltv_score: Mapped[float] = mapped_column(default=0.0)

class Campaign(Base):

    __tablename__ = 'campaigns'

    campaign_id: Mapped[str] = mapped_column(primary_key=True)
    channel_id: Mapped[str] = mapped_column(ForeignKey('channels.channel_id'))
    start_dt: Mapped[date] = mapped_column()
    end_dt: Mapped[date] = mapped_column()

class Channel(Base):

    __tablename__ = 'channels'

    channel_id: Mapped[str] = mapped_column(primary_key=True)
    channel_description: Mapped[str] = mapped_column()

class Offer(Base):

    __tablename__ = 'offers'

    offer_id: Mapped[str] = mapped_column(primary_key=True)
    channel_id: Mapped[str] = mapped_column(ForeignKey('channels.channel_id'))
    start_dt: Mapped[date] = mapped_column()
    end_dt: Mapped[date] = mapped_column()

class UnsolicitedHistory(Base):

    __tablename__ = 'unsolicited_history'

    visitor_key: Mapped[int] = mapped_column(ForeignKey('visitors.visitor_key'), primary_key=True)
    campaign_id: Mapped[str] = mapped_column(ForeignKey('campaigns.campaign_id'), primary_key=True)
    event_dt: Mapped[date] = mapped_column(primary_key=True)
    event_cd: Mapped[str] = mapped_column(primary_key=True)

    region: Mapped[str] = mapped_column()
    perf_month: Mapped[date] = mapped_column()
    creative_id: Mapped[str] = mapped_column()

class SolicitedHistory(Base):

    __tablename__ = 'solicited_history'

    cims_acct_key: Mapped[int] = mapped_column(ForeignKey('card_members.cims_acct_key'), primary_key=True)
    # channel_id: Mapped[int] = mapped_column(ForeignKey('channels.channel_id'), primary_key=True)
    offer_id: Mapped[str] = mapped_column(ForeignKey('offers.offer_id'), primary_key=True)
    event_dt: Mapped[date] = mapped_column(primary_key=True)

    # sent, retarget, click, converted
    event_cd: Mapped[str] = mapped_column(primary_key=True)

    # what level is this information (offer)?
    region: Mapped[str] = mapped_column()

    # what is this?
    perf_month: Mapped[date] = mapped_column()
    
    # should this be in the offer eligibility table instead?
    creative_id: Mapped[str] = mapped_column()

    # retargeting_ind: Mapped[bool] = mapped_column(nullable=True)

    # are scores refreshed once per month?
    # should this be in the eligibility table?
    # respond_score: Mapped[float] = mapped_column(nullable=True)

    # DM_MDL_SCR
    # EM_CHANNEL_SCR (what is this?)
    # EM_CLCK_SCR
    
class Application(Base):

    __tablename__ = 'applications'
    
    application_id: Mapped[str] = mapped_column(primary_key=True)
    updated_dt: Mapped[datetime] = mapped_column(primary_key=True)
    status: Mapped[str] = mapped_column()
    visitor_key: Mapped[int] = mapped_column(ForeignKey('visitors.visitor_key'))

class MarketSpendHistory(Base):

    __tablename__ = 'market_spend_history'

    campaign_id: Mapped[str] = mapped_column(ForeignKey('campaigns.campaign_id'), primary_key=True)
    perf_week: Mapped[date] = mapped_column(primary_key=True)
    
    # how does channel spend come about at the campaign level?
    channel_spend: Mapped[float] = mapped_column(default=0.0)
    campaign_spend: Mapped[float] = mapped_column(default=0.0)