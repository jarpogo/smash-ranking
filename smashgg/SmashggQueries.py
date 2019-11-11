import SmashggAPI

def get_event_id ( slug, token ) :
    """
    Return the eventId for a particular event given a tournaments URL slug

    :param slug: the tournament URL slug
    :returns: the eventId as a string
    """
    query = '\
        query TournamentsBySlug($slug: String!) {\
            tournament(slug:$slug) {\
                id\
                name\
                countryCode\
                addrState\
                city\
                venueAddress\
                venueName\
                startAt\
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

    data = SmashggAPI.execute_api(query, variables, token)
    res = 'null'

    if 'errorId' in data:
        raise ResourceWarning(data['message'])

    if data['data']['tournament'] == None:
        raise LookupError("Tournament doesn't exist with slug: %s" % slug)

    if data['data']['tournament']['events'] == None:
        raise LookupError("Event doesn't exist with slug: %s" % slug)

    # Search the results for the desired event (in this case, hardcoded to 'Ultimate Singles'
    for i in range (0, len (data['data']['tournament']['events'])):
        # TODO: logic to determine which event should be parsed out of the tournament events
        if data['data']['tournament']['events'][i]['name'] == 'Ultimate Singles':
            res = data['data']['tournament']['events'][i]['id']

    return res


def get_event_attendee_count ( slug, eventId, token ) :

    query = '\
        query AttendeeCount($tourneySlug: String!, $eventIds: [ID]) {\
            tournament(slug: $tourneySlug) {\
                name\
                participants(query: {\
                    filter: {\
                        eventIds:$eventIds\
                    }\
                }) {\
                    pageInfo {\
                        total\
                    }\
                }\
            }\
        }'

    variables = '\
        {\
            "tourneySlug": "%s",\
            "eventId": [%s]\
        }' % ( slug, eventId )

    res = SmashggAPI.execute_api(query, variables, token)

    return res['data']['tournament']['participants']['pageInfo']['total']


def get_event_standings ( eventId, token ) :
    """
    Return the participant standings for a particular event

    :param eventId: the ID for a particular event
    :returns: JSON data consisting of the participant standings
    """
    query = '\
        query EventStandings($eventId: ID!, $page: Int!, $perPage: Int!) {\
            event(id: $eventId) {\
                name\
                startAt\
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
        }' % eventId

    res = SmashggAPI.execute_api(query, variables, token)
    
    return res['data']['event']['standings']