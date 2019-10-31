import requests
import argparse

# app parameter configuration
parser = argparse.ArgumentParser()
parser.add_argument("-t", action="store", dest="api_token", help="your smash.gg API token")
parser.add_argument("-s", action="store", dest="slug", help="the tournament URL identifier")

args = parser.parse_args()


def getEventID( slug ) :
	"""
	Return the EventID for a particular event given a tournaments URL slug

	:param slug: the tournament URL slug
	:returns: the eventID as a string
	"""

	url = 'https://api.smash.gg/gql/alpha'
	json = { 'query' : 'query TournamentsBySlug($slug: String!) { tournament(slug:$slug){ id name countryCode slug events { id name videogame {id name}}}}', 'variables' : '{"slug":"%s"}' % slug }
	headers = {'Authorization': 'Bearer %s' % args.api_token}

	res = requests.post(url=url, json=json, headers=headers).json()

	# Search the results for the desired event (in this case, hardcoded to 'Ultimate Singles'
	for i in range (0, len (res['data']['tournament']['events'])):
		# TODO: logic to determine which event should be parsed out of the tournament events
		if res['data']['tournament']['events'][i]['name'] == 'Ultimate Singles':
			return (res['data']['tournament']['events'][i]['id'])



def getEventStandings( eventID ) :
	"""
	Return the participant standings for a particular event

	:param eventID: the ID for a particular event
	:returns: JSON data consisting of the participant standings
	"""

	url = 'https://api.smash.gg/gql/alpha'
	json = { 'query' : 'query EventStandings($eventId: ID!, $page: Int!, $perPage: Int!) { event(id: $eventId) { name standings(query: { perPage: $perPage, page: $page }){ nodes { standing entrant {name id}}}}}', 'variables' : '{"eventId": %s, "page": 1, "perPage": 30}' % eventID }
	headers = {'Authorization': 'Bearer %s' % args.api_token}
	
	res = requests.post(url=url, json=json, headers=headers).json()
	
	return res['data']['event']['standings']


eventID = getEventID(args.slug)
print (getEventStandings(eventID))
