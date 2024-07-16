from sqlalchemy import ForeignKey, DateTime
from sqlalchemy.orm import DeclarativeBase, relationship, Mapped, mapped_column
from sqlalchemy.sql import func
from typing import List
from datetime import datetime, date

import utils

# miss channel and offer tables
# miss campaign and offer relationship
# miss campaign table
# why no click in any communication history table?
# why campaign and channel go together?
# inconsistent datatype for id (mstr_apln_id)
# difficult for onmichannel view

class Base(DeclarativeBase):
    
    def __eq__(self, other):
        return str(self) == str(other)
     
    def __hash__(self):
        return hash(str(self))

class RiskEligibilityHistory(Base):

    # history or future?
    __tablename__ = 'risk_eligibility_history'

    # how about eligibility for DPL customers?
    cims_acct_key: Mapped[int] = mapped_column(
        ForeignKey('cardmembers.cims_acct_key'), 
        primary_key=True,
        comment='Acct key for Card Members'
    )
    perf_week: Mapped[date] = mapped_column(primary_key=True)
    risk_elig: Mapped[str] = mapped_column()

class MarketingEligibilityHistory(Base):

    __tablename__ = 'marketing_eligibility_history'

    cims_acct_key: Mapped[int] = mapped_column(
        ForeignKey('cardmembers.cims_acct_key'), 
        primary_key=True,
        comment='Acct key for Card Members'
    )
    perf_week: Mapped[date] = mapped_column(primary_key=True)
    sls_actv_pgm_eligble_ind: Mapped[str] = mapped_column()

class SolicitedHistory(Base):

    __tablename__ = 'solicited_history'

    cims_acct_key: Mapped[int] = mapped_column(
        ForeignKey('cardmembers.cims_acct_key'), 
        primary_key=True,
        comment='Acct key for Card Members'
    )
    perf_week: Mapped[date] = mapped_column(primary_key=True)

    # not an efficient way to store offer id
    dm_offer_id: Mapped[str] = mapped_column(nullable=True)
    dm_offer_strt_dt: Mapped[date] = mapped_column(nullable=True)
    dm_offer_end_dt: Mapped[date] = mapped_column(nullable=True)

    email_offer_id: Mapped[str] = mapped_column(nullable=True)
    email_offer_strt_dt: Mapped[date] = mapped_column(nullable=True)
    email_offer_end_dt: Mapped[date] = mapped_column(nullable=True)

    wt_offer_id: Mapped[str] = mapped_column(nullable=True)
    wt_offer_strt_dt: Mapped[date] = mapped_column(nullable=True)
    wt_offer_end_dt: Mapped[date] = mapped_column(nullable=True)

    # what is this?
    wt_elig: Mapped[str] = mapped_column()

class ModelScoreHistory(Base):

    __tablename__ = 'model_score_history'

    cims_acct_key: Mapped[int] = mapped_column(
        ForeignKey('cardmembers.cims_acct_key'), 
        primary_key=True,
        comment='Acct key for Card Members'
    )
    perf_mthly_dt: Mapped[date] = mapped_column(primary_key=True)
    rsp_mdl_scr: Mapped[float] = mapped_column(
        default=0.0, 
        comment='response score for DM'
    )
    em_channel_pref_scr: Mapped[float] = mapped_column(
        default=0.0, 
        comment='probability the email is active'
    )
    dpl_email_clk_scr: Mapped[float] = mapped_column(
        default=0.0, 
        comment='probability of click for email'
    )
    # what is this?
    wt_alloc_mdl_scr: Mapped[float] = mapped_column(
        default=0.0, 
        comment=''
    )

class CardmemberProfile(Base):

    __tablename__ = 'cardmember_profiles'

    cims_acct_key: Mapped[int] = mapped_column(
        ForeignKey('cardmembers.cims_acct_key'), 
        primary_key=True,
        comment='Acct key for Card Members'
    )
    perf_mnth: Mapped[date] = mapped_column(primary_key=True)
    transactor: Mapped[str] = mapped_column(nullable=True)
    mob: Mapped[float] = mapped_column(nullable=True)
    eighteen_mnth_score: Mapped[float] = mapped_column(nullable=True)
    otb: Mapped[float] = mapped_column(nullable=True) 
    fico: Mapped[int] = mapped_column(nullable=True)

class CardMember(Base):

    __tablename__ = 'cardmembers'

    cims_acct_key: Mapped[int] = mapped_column(
        primary_key=True, 
        comment='Acct key for Card Members'
    )

class DMCommunicationHistory(Base):

    __tablename__ = 'dm_communication_history'

    # what is the comment about? what is BM?
    cims_acct_key: Mapped[int] = mapped_column(
        ForeignKey('cardmembers.cims_acct_key'), 
        primary_key=True,
        comment='CIMS account key for CM, will be missing for BM, will be bank account key for DPL'
    )
    mail_drop_dt: Mapped[date] = mapped_column(
        primary_key=True, 
        comment='Mail drop date'
    )
    dm_offer_id: Mapped[str] = mapped_column(primary_key=True)

    unica_source_code: Mapped[str] = mapped_column(
        comment='Unica source code of the campaign (distinct campaign id)'
    )
    week: Mapped[int] = mapped_column()
    description: Mapped[str] = mapped_column(
        nullable=True, 
        comment='Creative description'
    )

class EmailCommunicationHistory(Base):

    __tablename__ = 'email_communication_history'

    cims_acct_key: Mapped[int] = mapped_column(
        ForeignKey('cardmembers.cims_acct_key'), 
        primary_key=True,
        comment='Acct key for Card Members'
    )
    # inconsistent column naming
    email_dlvy_dt: Mapped[date] = mapped_column(
        primary_key=True, 
        comment='Email delivery date'
    )
    day_part: Mapped[str] = mapped_column(
        primary_key=True,
        comment='Time of Day email was delivered'
    )
    email_offer_id: Mapped[str] = mapped_column(
        primary_key=True
    )
    email_mail_cmpgn_nm: Mapped[str] = mapped_column(nullable=True)
    email_offr_srcde: Mapped[str] = mapped_column(nullable=True)
    email_campg_group: Mapped[str] = mapped_column(nullable=True)
    description: Mapped[str] = mapped_column(nullable=True)

class WTCommunicationHistory(Base):

    __tablename__ = 'wt_communication_history'

    cims_acct_key: Mapped[int] = mapped_column(
        ForeignKey('cardmembers.cims_acct_key'), 
        primary_key=True,
        comment='Acct key for Card Members'
    )
    wt_date: Mapped[date] = mapped_column(
        primary_key=True,
        comment='Date of Impression'
    )
    page_name: Mapped[str] = mapped_column(
        primary_key=True,
        comment='Page of impression'
    )
    wt_offer_id: Mapped[str] = mapped_column(primary_key=True)
    # what is this?
    area_nm: Mapped[str] = mapped_column(
        nullable=True,
        comment='Name of module'
    )
    cont_nm: Mapped[str] = mapped_column(
        nullable=True,
        comment='Description of impression content'
    ) 
    usr_os: Mapped[str] = mapped_column(
        nullable=True,
        comment='Operating System'
    )
    dev_type: Mapped[str] = mapped_column(
        nullable=True,
        comment='Device Type'
    )

class UnsolicitedHistory(Base):

    __tablename__ = 'unsolicited_history'

    unique_visitors: Mapped[int] = mapped_column(
        primary_key=True
    )
    visit_date: Mapped[date] = mapped_column(
        primary_key=True
    )
    visit_timestamp: Mapped[str] = mapped_column(
        primary_key=True
    )
    channel: Mapped[str] = mapped_column()
    campaign_id: Mapped[str] = mapped_column(nullable=True)

class MarketingSpendHistory(Base):

    __tablename__ = 'marketing_spend_history'

    perf_week: Mapped[date] = mapped_column(
        primary_key=True
    )
    channel: Mapped[str] = mapped_column(
        primary_key=True
    )
    campaign_id: Mapped[str] = mapped_column(
        primary_key=True
    )
    dollar_spend: Mapped[float] = mapped_column(default=0.0)

class ResponderHistory(Base):

    __tablename__ = 'responder_history'

    # no key if not approved?
    bnk_acct_key: Mapped[int] = mapped_column(
        primary_key=True,
        comment='DPL Account number (for approved Apps)'
    )
    cims_acct_key: Mapped[int] = mapped_column(
        ForeignKey('cardmembers.cims_acct_key'), 
        primary_key=True,
        comment='CIMS account key for CM, will be missing for BM'
    )
    mstr_apln_id: Mapped[int] = mapped_column(
        primary_key=True,
        comment='DPL ApplicationID'
    )
    application_date: Mapped[date] = mapped_column(
        # primary_key=True,
        comment='Date DPL Application was received'
    )
    decision_waterfall: Mapped[str] = mapped_column(
        comment='Application Decision'
    )
    aprv_loan_amt: Mapped[float] = mapped_column(
        default=0.0, 
        comment='Loan Amount'
    )
    loan_apr: Mapped[float] = mapped_column(
        default=0.0, 
        comment='Loan APR'
    )
    # why highlighted?
    risk_score: Mapped[float] = mapped_column(
        default=0.0, 
    )
    loan_purpose: Mapped[str] = mapped_column(
        comment='Reason for Loan'
    )
    loan_trm_mth_cnt: Mapped[int] = mapped_column(
        default=0, 
        comment='Loan Term Month Count'
    )
    digital_segment: Mapped[str] = mapped_column(
        nullable=True,
        comment='Channel credited for Applicaation'
    )
    # inconsistent naming
    source_cd: Mapped[str] = mapped_column(
        nullable=True,
        comment='Source code matched to DM'
    )
    # year and week?
    week: Mapped[str] = mapped_column(
        comment='Week matched to DM'
    )
    drop_date: Mapped[date] = mapped_column(
        nullable=True,
        comment='Drop date matched to DM'
    )
    em_src_cd: Mapped[str] = mapped_column(
        nullable=True,
        comment='Source code matched to Email'
    )
    # notification?
    email_dlvy_dt: Mapped[date] = mapped_column(
        primary_key=True, 
        comment='Email delivery date'
    )
    # what is this?
    # inconsistent data type
    offer_mtch_ind: Mapped[int] = mapped_column()
    # inconsistent data type
    reeng_ind: Mapped[int] = mapped_column(
        comment='is this a reengaged customer?'
    )
    # inconsistent data type
    solicited_flag: Mapped[int] = mapped_column(
        comment='was this applicant solicited?'
    )

class ExternalVariables(Base):

    __tablename__ = 'external_variables'

    perf_week: Mapped[date] = mapped_column(primary_key=True)
    unemployment_rate: Mapped[float] = mapped_column(nullable=True)
    fed_rate: Mapped[float] = mapped_column(nullable=True)
    cpi: Mapped[float] = mapped_column(nullable=True)
    inflation: Mapped[float] = mapped_column(nullable=True)

# class Visitor(Base):

#     __tablename__ = 'visitors'

#     visitor_key: Mapped[int] = mapped_column(primary_key=True)
#     cims_acct_key: Mapped[int] = mapped_column(ForeignKey('cardmembers.cims_acct_key'))
#     dpl_acct_key: Mapped[int] = mapped_column(ForeignKey('dpl_customers.dpl_acct_key'))

# class CardMember(Base):

#     __tablename__ = 'cardmembers'

#     cims_acct_key: Mapped[int] = mapped_column(primary_key=True)

#     # can a card member have multiple email address?
#     email_address: Mapped[str] = mapped_column()
#     email_opted_out: Mapped[bool] = mapped_column()

# class DPLCustomer(Base):

#     __tablename__ = 'dpl_customers'
    
#     dpl_acct_key: Mapped[int] = mapped_column(primary_key=True)

# class OfferEligibility(Base):

#     # channel eligibilities?
#     __tablename__ = 'offer_eligibilities'

#     cims_acct_key: Mapped[int] = mapped_column(ForeignKey('cardmembers.cims_acct_key'), primary_key=True)
#     perf_week: Mapped[date] = mapped_column(primary_key=True)
#     # channel_id: Mapped[str] = mapped_column(ForeignKey('channels.channel_id'), primary_key=True)

#     # can a customer receive multiple offer id in a week (primary key)?
#     offer_id: Mapped[str] = mapped_column(ForeignKey('offers.offer_id'))
#     offer_elig: Mapped[bool] = mapped_column()
#     # missing this?
#     respond_score: Mapped[float] = mapped_column(default=0.0)
#     conversion_score: Mapped[float] = mapped_column(default=0.0)
#     ltv_score: Mapped[float] = mapped_column(default=0.0)

# class CampaignEligibility(Base):
#     # missing this?
#     __tablename__ = 'campaign_eligibilities'

#     visitor_key: Mapped[int] = mapped_column(ForeignKey('visitors.visitor_key'), primary_key=True)
#     perf_week: Mapped[date] = mapped_column(primary_key=True)
#     # channel_id: Mapped[str] = mapped_column(ForeignKey('channels.channel_id'), primary_key=True)
#     campaign_id: Mapped[str] = mapped_column(ForeignKey('campaigns.campaign_id'))
#     campaign_elig: Mapped[bool] = mapped_column()
#     respond_score: Mapped[float] = mapped_column(default=0.0)
#     conversion_score: Mapped[float] = mapped_column(default=0.0)
#     ltv_score: Mapped[float] = mapped_column(default=0.0)

# class Campaign(Base):

#     __tablename__ = 'campaigns'

#     campaign_id: Mapped[str] = mapped_column(primary_key=True)
#     channel_id: Mapped[str] = mapped_column(ForeignKey('channels.channel_id'))
#     start_dt: Mapped[date] = mapped_column()
#     end_dt: Mapped[date] = mapped_column()

# class Channel(Base):

#     __tablename__ = 'channels'

#     channel_id: Mapped[str] = mapped_column(primary_key=True)
#     channel_description: Mapped[str] = mapped_column()

# class Offer(Base):

#     __tablename__ = 'offers'

#     offer_id: Mapped[str] = mapped_column(primary_key=True)
#     channel_id: Mapped[str] = mapped_column(ForeignKey('channels.channel_id'))
#     headline_price_lb: Mapped[float] = mapped_column()
#     headline_price_ub: Mapped[float] = mapped_column()
#     start_dt: Mapped[date] = mapped_column()
#     end_dt: Mapped[date] = mapped_column()

# class UnsolicitedHistory(Base):

#     __tablename__ = 'unsolicited_history'

#     visitor_key: Mapped[int] = mapped_column(ForeignKey('visitors.visitor_key'), primary_key=True)
#     campaign_id: Mapped[str] = mapped_column(ForeignKey('campaigns.campaign_id'), primary_key=True)
#     event_dt: Mapped[date] = mapped_column(primary_key=True)
#     event_cd: Mapped[str] = mapped_column(primary_key=True)

#     region: Mapped[str] = mapped_column()
#     perf_month: Mapped[date] = mapped_column()
#     creative_id: Mapped[str] = mapped_column()

# class SolicitedHistory(Base):

#     __tablename__ = 'solicited_history'

#     cims_acct_key: Mapped[int] = mapped_column(ForeignKey('cardmembers.cims_acct_key'), primary_key=True)
#     # channel_id: Mapped[int] = mapped_column(ForeignKey('channels.channel_id'), primary_key=True)
#     offer_id: Mapped[str] = mapped_column(ForeignKey('offers.offer_id'), primary_key=True)
#     event_dt: Mapped[date] = mapped_column(primary_key=True)

#     # sent, retarget, click, converted
#     event_cd: Mapped[str] = mapped_column(primary_key=True)

#     # what level is this information (offer)?
#     region: Mapped[str] = mapped_column()

#     # what is this?
#     perf_month: Mapped[date] = mapped_column()
    
#     # should this be in the offer eligibility table instead?
#     creative_id: Mapped[str] = mapped_column()

#     # retargeting_ind: Mapped[bool] = mapped_column(nullable=True)

#     # are scores refreshed once per month?
#     # should this be in the eligibility table?
#     # respond_score: Mapped[float] = mapped_column(nullable=True)

#     # DM_MDL_SCR
#     # EM_CHANNEL_SCR (what is this?)
#     # EM_CLCK_SCR
    
# class ResponderHistory(Base):

#     __tablename__ = 'responder_history'
    
#     application_id: Mapped[str] = mapped_column(ForeignKey('applications.application_id'), primary_key=True)
#     updated_dt: Mapped[datetime] = mapped_column(primary_key=True)
#     status: Mapped[str] = mapped_column()

# class Application(Base):

#     __tablename__ = 'applications'

#     application_id: Mapped[str] = mapped_column(primary_key=True)
#     visitor_key: Mapped[int] = mapped_column(ForeignKey('visitors.visitor_key'))
#     campaign_id: Mapped[str] = mapped_column(ForeignKey('campaigns.campaign_id'))
#     offer_id: Mapped[str] = mapped_column(ForeignKey('offers.offer_id'))

# class MarketSpendHistory(Base):

#     __tablename__ = 'market_spend_history'

#     campaign_id: Mapped[str] = mapped_column(ForeignKey('campaigns.campaign_id'), primary_key=True)
#     perf_week: Mapped[date] = mapped_column(primary_key=True)
    
#     # how does channel spend come about at the campaign level?
#     channel_spend: Mapped[float] = mapped_column(default=0.0)
#     campaign_spend: Mapped[float] = mapped_column(default=0.0)