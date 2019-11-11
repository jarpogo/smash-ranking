import requests
import argparse
import SmashggQueries

# app parameter configuration
parser = argparse.ArgumentParser()
parser.add_argument("-t", action="store", dest="api_token", help="your smash.gg API token")
parser.add_argument("-s", action="store", dest="slug", help="the tournament URL identifier")
parser.add_argument("-l", action="store", dest="slug_file", help="a file consisting of a list of slugs")

args = parser.parse_args()

if args.slug_file is not None:
    with open(args.slug_file) as slug_list:
        line = slug_list.readline().strip()
        cnt = 1
        while line:
            print("\nLine {}: {}".format(cnt, line))
            try:
                eventID = SmashggQueries.get_event_id(line, args.api_token)
                
                res = SmashggQueries.get_event_attendee_count(line, eventID, args.api_token)
                print ("Attendees: " + str(res))
                
                res = SmashggQueries.get_event_standings(eventID, args.api_token)
                print ("Event Standings: " + str(res))
                
            except (LookupError, ResourceWarning) as msg:
                print (msg)

            line = slug_list.readline().strip()
            cnt += 1
else:
    eventID = SmashggQueries.get_event_id(args.slug, args.api_token)
    res = SmashggQueries.get_event_standings(eventID, args.api_token)
    print (res)
