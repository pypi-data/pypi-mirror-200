# Chat

Create a mattermost chat for discussing superevents.

## Usage

This current version uses a simple superevent_dictionary 
containing superevent_id to make mattermost channels.
It only works if the .netrc file has a "mattermost-bot" 
login with appropiate token as password. 

A `response` object gets the response form the mattermost api
If there is no response, the channel creation succeeded 
The new channel name will be `RRT {superevent_id}`
A post will be made in this channel with a corresponding 
grace_db playground url.

```
from ligo.rrt_chat import channel_creation
import json

res = channel_creation.rrt_channel_creation(superevent_dict)

if res is not None:
    print("channel creation failed {}".format(json.loads(res.text)))    
else:
    print("channel creation succeded")
```
