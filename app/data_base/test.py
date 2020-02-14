from app.data_base.DB import DB
from app.data_base import bilibilier
from app.data_base import video

# bilibilier.write(2)

# x = bilibilier.read(2)

# DB.reset()
av1 = '78884756'
av2 = '79907068'
# video.write(av2)
r = video.read(av2)
for reply in r['replies']:
    if len(reply['sub_replies']) > 0:
        print(reply['rpid'])
        for sub in reply['sub_replies']:
            print(sub)




