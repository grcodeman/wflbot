import requests

ac_url = "https://docs.google.com/forms/d/e/1FAIpQLSeG9pnigqPSvsUDWKT9gFTCRjh2O4vgpsH41OihHh5QsmoLsQ/formResponse"

def submit_ac (user, player, disc):
    try:
        form_data = {'entry.1388311424':str(user),
                    'entry.1167180825':str(player),
                    'entry.796014550':str(disc),
                    'draftResponse':[],
                    'pageHistory':0}
        user_agent = {'Referer':'https://docs.google.com/forms/d/e/1FAIpQLSeG9pnigqPSvsUDWKT9gFTCRjh2O4vgpsH41OihHh5QsmoLsQ/viewform','User-Agent': "Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/28.0.1500.52 Safari/537.36"}
        r = requests.post(ac_url, data=form_data, headers=user_agent)
        if str(r.status_code) == '200':
            return "AC Submitted: `" + str(user) + "` `" + str(player) + "` `" + str(disc) + "`"
        else:
            return 'Failed to submit AC'
    except:
        return "Error"