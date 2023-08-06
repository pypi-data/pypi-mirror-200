from ligo.rrt_chat.mattermost_api import MMApi
from safe_netrc import netrc, NetrcParseError
from requests.exceptions import RequestException

from . import LIGO_ID, MATTERMOST_API, RRT_ID


def get_auth(host):
    try:
        auth = netrc().authenticators(host)
        if not auth:
            raise ValueError('No netrc entry found for {}'.format(host))
        else:
            _, _, TOKEN = auth
            return TOKEN
    except (NetrcParseError, OSError, ValueError):
        print('Could not load the mattermost bot'
              'token for {} from the netrc file'.format(host))


def rrt_channel_creation(superevent_id, gracedb_url='gracedb.ligo.org'):
    """
    Creates a channel in LIGO team in Mattermost based
    on the superevent_id. Also attaches a link for the
    corresponding gracedb entry.

    Parameters
    ----------
    superevent_id: string
        The superevent id
    gracedb_url: string
        The grace_db url corresponding to the superevnt

    Raises
    ------
    RequestException: If channel creation or login fails
    """

    # Mattermost credentials file needs to be changed according to user
    mm = MMApi(MATTERMOST_API)
    token = get_auth("mattermost-bot")
    login_response = mm.login(bearer=token)
    if login_response.status_code != 200:
        raise RequestException(login_response.json()['message'])
    channel_name = "rrt-" + superevent_id.lower()
    channel_display_name = "RRT " + superevent_id
    channel_response = mm.create_channel(LIGO_ID, channel_name,
                                         channel_display_name)
    if channel_response.status_code == 201:
        channel_id = channel_response.json()['id']
        grace_url = "https://" + gracedb_url + "/superevents/" + \
                    superevent_id + "/view/"
        mm.post_in_channel(channel_id, grace_url)
        post_msg = f"Channel created for {superevent_id}. Channel:~rrt-" + \
                   superevent_id.lower()
        mm.post_in_channel(RRT_ID, post_msg)
        mm.logout()
    else:
        mm.logout()
        raise RequestException(channel_response.json()['message'])
