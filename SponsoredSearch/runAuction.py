from auctions import myBalance
from AuctionGenerator import generateAdvertisers,generateSlots
from bots import Bot1, Bot2, Bot3, Bot4, Bot5, Bot6, Bot7
from string import ascii_lowercase

# bots_types = [Bot1, Bot2,Bot3,Bot4,Bot5,Bot6,Bot7]

#In particular, for each auction format and for each bot adopted by the other advertiser
# you must run the auction for at least 500 different auction settings (slots’ click-through
# ratio, advertisers’ values and budgets) randomly generated.

queries = ["bread","bake","flour"]

################ PARAMETERS
# range of number of slots available to sell for each query
minSlots = 3
maxSlots = 4

#range of evaluation for each query
minValue = 0
maxValue = 10

#range of budgets for each bidder
minBudget = 50
maxBudget = 70

#number of random executions
nAuctions = 1
max_step = 100	

verbose = False

def printDelim():
	print("**********************************************************************")
	print("**********************************************************************")
	print("**********************************************************************")
	print("**********************************************************************")
	print("**********************************************************************")
	print("**********************************************************************")
	return

def printNewAuctionResult(history,bots,sbudgets,cbudgets,evals,slots):
	print("// SLOTS")
	print("ID\tClickthrough Rate")
	for slot in slots.keys():
		print(slot,"\t",slots[slot])
	print("// ADVERTISER'S RESULTS")
	print("Name\tValue\tSBudg.\tFBudg.\tSpent\tUtils\t\tBot")
	for adv in evals.keys():
		util = 0
		for step in range(len(history)):
			util = util + history[step]["adv_utilities"][adv]
		if adv == "a":
			c="*"
		else:
			c=""
		print(c,adv,"\t",evals[adv],"\t","%.2f"%sbudgets[adv],"\t","%.2f"%cbudgets[adv],"\t","%.2f"%(sbudgets[adv]-cbudgets[adv]),"\t","%.2f"%util,"\t\t",bots[adv])

	return

def printAuctionResult(nAuction,slots, adv_bots, adv_budgets, adv_values,adv_bids,assigned_slots,payments,step):
	print("**************************")
	print("Auction #",nAuction)
	print("\n//// INPUT")
	print("// SLOTS")
	print("ID\tClickthrough Rate")
	for slot in slots.keys():
		print(slot,"\t",slots[slot])
	print("// ADVERTISERS")
	print("Name\tValue\tBudget\tBid\tBot")
	for adv in adv_values.keys():
		if adv == "a":
			c="*"
		else:
			c=""
		print(c,adv,"\t",adv_values[adv],"\t","%.2f"%adv_budgets[adv],"\t","%.2f" % adv_bids[adv],"\t",adv_bots[adv])
	
	print("\n//// OUTPUT")
	print("// ASSIGNED SLOTS")
	print("ID\tAdv\tPayment\tUtility")
	for slot in assigned_slots.keys():
		paid = payments[assigned_slots[slot]]
		util = adv_values[assigned_slots[slot]] - paid
		print(slot,"\t",assigned_slots[slot],"\t","%.2f" % paid,"\t","%.2f" % util)
	print("// CLOSED IN")
	print(step,"steps")
	print("**************************")
	return

def printInput(slots,adv_values,adv_budgets,adv_bots):
	print("\n//// INPUT")
	print("// SLOTS")
	print("ID\tClickthrough Rate")
	for slot in slots.keys():
		print(slot,"\t",slots[slot])
	print("// ADVERTISERS")
	print("Name\tValue\tBudget\tBot")
	for adv in adv_values.keys():
		if adv == "a":
			c="*"
		else:
			c=""
		print(c,adv,"\t",adv_values[adv],"\t",adv_budgets[adv],"\t",adv_bots[adv])
	return

def printTableHeader(advs):
	print("____________________________________________________________")
	header = ""
	for adv in advs.keys():
		header += adv+"\t"
	print(header)
	return

def printTableRow(step,budgets,bids,slots,payments,utilities,evaluation):
	print("________________________________________________________________________")
	print("#",step,end="\t")
	for adv in budgets.keys():
		print(adv,end="\t")
	print("\n________________________________________________________________________")
	print("budget",end="\t")
	for adv in budgets.keys():
		print("%.1f" % budgets[adv],end="\t")
	print("\nevals",end="\t")
	for adv in budgets.keys():
		print("%.1f" % evaluation[adv],end="\t")
	print("\nbids",end="\t")
	for adv in budgets.keys():
		print("%.1f" % bids[adv],end="\t")
	print("\npaid",end="\t")
	for adv in budgets.keys():
		if adv in payments.keys():
			print("%.1f" % payments[adv],end="\t")
		else:
			print(end="\t")
	print("\nutils",end="\t")
	for adv in budgets.keys():
		print("%.1f" % utilities[adv],end="\t")
	print(end="\n")
	return



def printOutput():
	return	

def runAuctions(ourbot, otherbots):
	adv_bots = dict()
	adv_counter = 0

	#instantiate our Bot
	adv_bots[ascii_lowercase[adv_counter]] = ourbot()
	adv_counter += 1

	#instantiate all other bots
	while adv_counter < number_of_bots:
		adv_bots[ascii_lowercase[adv_counter]] = otherbots()
		adv_counter +=1 

	for i in range(nAuctions):
		

		slots = generateSlots(queries,minSlots,maxSlots)
		adv_values, adv_sbudgets = generateAdvertisers(queries,adv_bots.keys(),minValue,maxValue,minBudget,maxBudget)

		step = 0
		history = []
		adv_bids = dict()
		adv_utilities = dict()
		adv_budgets = dict(adv_sbudgets)
		done = False

		# printInput(slots,adv_values,adv_budgets,adv_bots)

		# printTableHeader(adv_bots)
		while not done and step < max_step:
			
			# done = True
			for adv_name in adv_bots.keys():
				adv_bids[adv_name] = adv_bots[adv_name].response(adv_name,adv_values[adv_name],history,slots,0,0)
				# if adv_bids[adv_name] > adv_values[adv_name]:
					# print("DIOPORCO perche' cazzo",adv_name,"ha puntato","%.1f" % adv_bids[adv_name],"se lo valutava","%.1f"%adv_values[adv_name],"ma bisogna essere degli stronzi pero'")
				# if step == 0 or adv_bids[adv_name] != history[step-1]["adv_bids"][adv_name]:
				# 	done = False


			# if done:
			# 	break
			assigned_slots, payments = myBalance(slots,adv_bids,adv_sbudgets,adv_budgets)


			adv_utilities = dict()
			for adv in adv_values:
				if adv in payments and payments[adv] > 0:
					adv_utilities[adv] = adv_values[adv]- payments[adv]
					adv_budgets[adv] = adv_budgets[adv] - payments[adv]
				else:
					adv_utilities[adv] = 0

			# printTableRow(step,adv_budgets,adv_bids,assigned_slots,payments,adv_utilities,adv_values)

			history.append(dict())
			history[step]["adv_bids"] = dict(adv_bids)
			history[step]["adv_slots"] = dict(assigned_slots)
			history[step]["adv_pays"] = dict(payments)
			history[step]["adv_utilities"] = dict(adv_utilities)
			history[step]["adv_budgets"] = dict(adv_budgets)
			print(step,adv_utilities)
			
			step += 1
		printNewAuctionResult(history,adv_bots,adv_sbudgets,adv_budgets,adv_values,slots)
		

# SETTINGS
ourbot = Bot1	
otherbots = Bot1
number_of_bots = 8

runAuctions(ourbot,otherbots)













