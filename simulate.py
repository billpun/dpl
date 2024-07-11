from datetime import datetime, timedelta
import random

from database import SQLite
from entities import *
from utils import *

SUBMISSION_PROB = 0.05
APPROVE_REJECT_PROB = 0.5
CANCEL_PROB = 0.1

db = SQLite('demo.db', Base, create=True, renew=True, read_only=False)
db.connect()

NUM_VISITORS = 10
NUM_CUSTOMERS = 2
NUM_PRODUCTS = 3

# set random seeds
random.seed(0)

# simulate products
products = dict()
for i, name in enumerate(['DPL1', 'DPL2', 'DPL3']):
	p = Product()
	p.product_id = f'P{str(i).zfill(5)}'
	p.product_name = name
	p.headline_rate_lb = random.choice([j for j in range(10, 16)])
	p.headline_rate_ub = random.choice([j for j in range(16, 25)])
	products[p.product_id] = p

# simulate visitors
visitors = dict()
for v in range(NUM_VISITORS):
	v = Visitor()
	v.visitor_id = f'V{str(len(visitors)).zfill(8)}'
	visitors[v.visitor_id] = v

# simulate customers
customers = dict()
for c in range(NUM_CUSTOMERS):
	c = Customer()
	c.customer_id = f'C{str(len(visitors)).zfill(8)}'
	c.card_member_ind = (random.random() < 0.5)
	c.dpl_ind = not c.card_member_ind
	customers[c.customer_id] = c

# link customers and visitors
for v, c in zip(random.choices(list(visitors.values()), k=NUM_CUSTOMERS), customers.values()):
	v.customer_id = c.customer_id

# create channels
channels = dict()
for i, cname in enumerate(['direct_marketing', 'web', 'mobile']):
	c = Channel()
	c.channel_id = f'CH{str(i).zfill(3)}'
	c.channel_name = cname
	channels[c.channel_id] = c

# create campaigns
campaigns = dict()
for i, p in enumerate(products.values()):
	for h in channels.values():
		c = Campaign()
		c.campaign_id = f'CA{str(i).zfill(5)}'
		c.product_id = p.product_id
		# c.campaign_name = cname
		c.channel_id = h.channel_id
		campaigns[c.campaign_id] = c

# link channels and campaigns
marketing_spends = []
target_population = []
offer_id = 0
for c in campaigns.values():

	s = MarketingSpend()
	s.campaign_id = c.campaign_id
	s.campaign_spend = round(random.uniform(10, 100), DECIMAL)
	s.channel_spend = round(random.uniform(10, 100), DECIMAL)
	s.start_dt = datetime(2024, 1, 1)
	s.end_dt = datetime(2024, 12, 31, 23, 59, 59)
	marketing_spends.append(s)

	for v in visitors.values():
		e = TargetPopulation()
		e.visitor_id = v.visitor_id
		e.campaign_id = c.campaign_id
		e.offer_id = '' if random.random() < 0.5 else f'O{str(offer_id).zfill(3)}'
		offer_id += 1
		e.resp_prob = round(random.uniform(0, 0.2), DECIMAL)
		e.conv_prob = round(random.uniform(0, 0.05), DECIMAL)
		e.cus_value = round(random.uniform(100, 1000), DECIMAL)
		e.eligibility_flag = True
		e.expected_approval_rate = round(random.uniform(0.3, 0.7), DECIMAL)
		target_population.append(e)

		
activities = []
applications = []
for t in target_population:
	clicks = random.randint(0, 5)
	visitor = visitors[t.visitor_id]
	campaign = campaigns[t.campaign_id]
	channel = channels[campaign.channel_id]
	last_dt = datetime(2024, 1, 1)
	for i in range(clicks):
		a = Activity()
		a.activity_id = f'AC{str(len(activities)).zfill(8)}'
		a.visitor_id = visitor.visitor_id
		a.clicked_campaign = campaign.campaign_id
		a.clicked_channel = channel.channel_id
		a.clicked_dt = last_dt + timedelta(days=random.randint(1, 5))
		last_dt = a.clicked_dt
		activities.append(a)

		# simulate applications submission
		if random.random() <= SUBMISSION_PROB:
			# applied: visitor submitted application
			# decision: approved or rejected based on visitor soft-pull credit info
			# offered: customer prices offered if approved
			# accepted: custom prices accepted by customer
			# hard-pull: final verification
			# converted: successfully converted
			# cancelled: application cancelled
			for s in ['applied', 'decision', 'offered', 'accepted', 'hard-pull', 'converted']:
				if s == 'decision':
					if random.random() <= APPROVE_REJECT_PROB:
						s = 'approved'
					else:
						s = 'rejected'
				if s != 'applied' and random.random() <= CANCEL_PROB:
					s = 'cancelled'
				a = Application()
				a.application_id = f'AP{str(len(applications)).zfill(6)}'
				a.conversion_flag
				a.status = s
				a.status_dt = last_dt + timedelta(days=random.randint(1, 3))
				a.visitor_id = visitor.visitor_id
				a.channel_id = channel.channel_id
				a.campaign_id = campaign.campaign_id
				last_dt = a.status_dt
				applications.append(a)
				if s in {'cancelled', 'rejected'}:
					break

			if applications[-1].status == 'converted':
				# no more activity to simulate
				break

# save objects
def save(objects):
	if isinstance(objects, dict):
		objects = objects.values()
	for o in objects:
		db.session.add(o)
	db.session.commit()
save(products)
save(visitors)
save(customers)
save(channels)
save(campaigns)
save(marketing_spends)
save(target_population)
save(activities)
save(applications)

db.optimize()
db.close()