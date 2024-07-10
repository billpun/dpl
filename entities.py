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

    # ! need to know what the application is about
    campaign_id: Mapped[str] = mapped_column(ForeignKey('campaigns.campaign_id'))

    def __repr__(self):
        return f'ap_{self.application_id}_{self.status_dt.strftime(utils.DATETIME_FORMAT)}'

# eligibility table?
class TargetPopulation(Base):

    __tablename__ = 'target_population'

    campaign_id: Mapped[str] = mapped_column(ForeignKey('campaigns.campaign_id'), primary_key=True)
    visitor_id: Mapped[str] = mapped_column(ForeignKey('visitors.visitor_id'), primary_key=True)

    offer_id: Mapped[str] = mapped_column()

    resp_prob: Mapped[float] = mapped_column(default=0.0) # soft pull
    conv_prob: Mapped[float] = mapped_column(default=0.0) # hard pull
    cus_value: Mapped[float] = mapped_column(default=0.0) # null for prospect?

    # ! this is great for simulation (but could be huge)
    # this implies that even if the visitor is ineligible, statistics are still available
    eligibility_flag: Mapped[bool] = mapped_column(default=False)

    # what is this?
    expected_approval_rate: Mapped[float] = mapped_column(default=0.0)

    # ! this could just be a target dt depending on how often this is refreshed
    # period in which the target population and statistics are valid
    valid_from: Mapped[datetime] = mapped_column(nullable=True)
    valid_to: Mapped[datetime] = mapped_column(nullable=True)

    # offer id
    # solicitation attributes
    def __repr__(self):
        return f'tp_{self.visitor_id}_{self.campaign_id}'

# campaign?
class MarketingSpend(Base):

    __tablename__ = 'marketing_spend'

    # !!!!! depends on if campaign_id encodes channel
    campaign_id: Mapped[str] = mapped_column(ForeignKey('campaigns.campaign_id'), primary_key=True) # same ID across channels?
    # channel_id: Mapped[str] = mapped_column(ForeignKey('channels.channel_id'), primary_key=True)
    start_dt: Mapped[datetime] = mapped_column(primary_key=True) # what does it refer to?
    end_dt: Mapped[datetime] = mapped_column(primary_key=True) # what does it refer to?

    # how does channel spend come about at the campaign level?
    channel_spend: Mapped[float] = mapped_column(default=0.0)
    campaign_spend: Mapped[float] = mapped_column(default=0.0)

    def __repr__(self):
        return f'ms_{self.campaign_id}_' + \
            f'{self.start_dt.strftime(utils.DATETIME_FORMAT)}_' + \
            f'{self.end_dt.strftime(utils.DATETIME_FORMAT)}'

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

    # a campaign is created for a channel
    channel_id: Mapped[str] = mapped_column(ForeignKey('channels.channel_id'))

    # a campaign is about selling a product
    product_id: Mapped[str] = mapped_column(ForeignKey('products.product_id'))

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

    # ! would an indicator be enough or 
    # do they have their own customer id
    card_member_ind: Mapped[bool] = mapped_column()
    dpl_ind: Mapped[bool] = mapped_column()

    # ! need additional attribution for similarity
    def __repr__(self):
        return f'u_{self.customer_id}'

class Product(Base):

    __tablename__ = 'products'

    product_id: Mapped[str] = mapped_column(primary_key=True)
    product_name: Mapped[str] = mapped_column()

    headline_rate_lb: Mapped[float] = mapped_column(default=0)
    headline_rate_ub: Mapped[float] = mapped_column(default=0)

class CustomerProducts(Base):

    __tablename__ = 'customer_products'

    customer_id: Mapped[str] = mapped_column(ForeignKey('customers.customer_id'), primary_key=True)
    product_id: Mapped[str] = mapped_column(ForeignKey('products.product_id'), primary_key=True)

    # active, cancelled, paid off
    status: Mapped[str] = mapped_column()

    start_dt: Mapped[datetime] = mapped_column()
    end_dt: Mapped[datetime] = mapped_column()

    # ! what additional attributes do we need?

# class Offers(Base):

#     __tablename__ = 'offers'

#     offer_id: Mapped[str] = mapped_column(primary_key=True)
#     valid_from: Mapped[datetime] = mapped_column()
#     valid_to: Mapped[datetime] = mapped_column()


