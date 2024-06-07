import json
import os

def convert_time(timestamp):
    import datetime

    # Convert the timestamp to seconds
    timestamp_in_seconds = timestamp / 1000

    # Convert the timestamp to a datetime object
    dt = datetime.datetime.fromtimestamp(timestamp_in_seconds)

    # Format the datetime object to a readable string
    readable_time = dt.strftime("%Y-%m-%d %H:%M:%S")
    
    return readable_time


folder_path = './data'
for filename in os.listdir(folder_path):
    f = open(folder_path + "/" + filename + "/message_1.json")
    
    data = json.load(f)

    
    final_data = []
    for mes in data['messages']:

        sender_name = mes['sender_name'].encode('latin1').decode('utf8')
        timestamp_ms = convert_time(mes['timestamp_ms'])
        is_geoblocked_for_viewer = mes['is_geoblocked_for_viewer']
        if 'share' in mes:
            if 'link' in mes['share']:
                share_link= mes['share']['link']
            else:
                share_link= ""
        else:
            share_link= ""
            mes['share'] = ""
            
        if 'reactions' in mes:
            if 'reaction' in mes['reactions'][0]:
                reactions_reaction= mes['reactions'][0]['reaction'].encode('latin1').decode('utf8')
            else:
                reactions_reaction= ""
                
            if 'actor' in mes['reactions'][0]:
                reactions_actor= mes['reactions'][0]['actor'].encode('latin1').decode('utf8')
            else:
                reactions_actor= ""
                
        else:
            reactions_reaction= ""
            reactions_actor= ""
            
        if 'photos' in mes:
                photos_url= mes['photos'][0]['uri']
        else:
            photos_url= ""
            
        if 'content' in mes:
            content = mes['content'].encode('latin1').decode('utf8')
        else:
            content= ""
        
        final_data.append({
            "sender_name": sender_name,
            "timestamp_ms": timestamp_ms,
            "is_geoblocked_for_viewer": is_geoblocked_for_viewer,
            "share_link": share_link,
            "reactions_reaction": reactions_reaction,
            "reactions_actor": reactions_actor,
            "photos_url": photos_url,
            "content": content
        })
    import pandas as pd
    df = pd.DataFrame(final_data)  # transpose to look just like the sheet above
    df.to_excel(f'data/{filename}.xlsx')