import smashgg_api  

def getEventID( slug, token ) :
    """
    Return the EventID for a particular event given a tournaments URL slug

    :param slug: the tournament URL slug
    :returns: the eventID as a string
    """
    query = '\
        query TournamentsBySlug($slug: String!) {\
            tournament(slug:$slug) {\
                id\
                name\
                countryCode\
                slug\
                events {\
                    id\
                    name\
                    videogame {\
                        id\
                        name\
                    }\
                }\
            }\
        }'

    variables = '\
        {\
            "slug":"%s"\
        }' % slug

    data = smashgg_api.executeApi(query, variables, token)
    res = 'null'

    if 'errorId' in data:
        raise ResourceWarning(data['message'])

    if data['data']['tournament'] == None:
        raise LookupError("Tournament doesn't exist with slug: %s" % slug)

    # Search the results for the desired event (in this case, hardcoded to 'Ultimate Singles'
    for i in range (0, len (data['data']['tournament']['events'])):
        # TODO: logic to determine which event should be parsed out of the tournament events
        if data['data']['tournament']['events'][i]['name'] == 'Ultimate Singles':
            res = data['data']['tournament']['events'][i]['id']

    return res


def getEventStandings( eventID, token ) :
    """
    Return the participant standings for a particular event

    :param eventID: the ID for a particular event
    :returns: JSON data consisting of the participant standings
    """
    query = '\
        query EventStandings($eventId: ID!, $page: Int!, $perPage: Int!) {\
            event(id: $eventId) {\
                name\
                standings(query: {\
                    perPage: $perPage,\
                    page: $page\
                }) {\
                    nodes {\
                        standing\
                        entrant {\
                            name\
                            id\
                        }\
                    }\
                }\
            }\
        }'

    variables = '\
        {\
            "eventId": %s,\
            "page": 1,\
            "perPage": 30\
        }' % eventID

    res = smashgg_api.executeApi(query, variables, token)
    
    return res['data']['event']['standings']