import json
import base64
import requests
from datetime import datetime
from time import sleep
from facebook_scraper import get_posts
from IPython.core.events import post_run_cell

token = '34ea8abce853ae9a90d4a826c52766aadfe591d9'
headers= {'Authorization': 'token ' + token,
    'Accept': 'application/json',
    'Content-Type': 'application/json;charset=UTF-8'
    }

def influencer_check():
    url ='http://test.dabi-api.com/api/influencer/'
    i=0
    facebook_id_list = []
    facebook_pk_list = {}
    t = True
    while t:
        sleep(10)
        print('influencer_check')
        response = requests.get(url+'?offset='+str(i), headers=headers)
        print(response)
        print(i)

        if response:
            try:
                data = response.json()
            except Exception as e:
                print('Invalid response data in influencer_pk')
                continue
            if data:
                # We should use .get when we have a dictionary for safety reason
                result = data.get('results', None)
                count = data.get('count')
                # Check result is in correct form
                if result:        
                    for i2 in range(len(result)):
                        
                        if result[i2]['pk'] != None:
                            facebook_pk_list[result[i2]['insta_pk']] = result[i2]['pk']
                            facebook_id_list.append(result[i2]['insta_pk'])
                        if data['next']==None and count == len(facebook_pk_list):
                            
                            if result[i2]['pk'] != None:
                                facebook_pk_list[result[i2]['insta_pk']] = result[i2]['pk']
                                facebook_id_list.append(result[i2]['insta_pk'])
                            with open('dosiciety.json','rt', encoding='UTF8') as json_file:
                                json_data = json.load(json_file)
                                id_li = []
                                for i in range(len(json_data)):
                                    influencer_id = json_data[i]['user_id']
                                    id_li.append(influencer_id)

                                for i in range(len(json_data)):
                                    influencer = json_data[i]['username']
                                    influencer_id = json_data[i]['user_id']
                                    
                                    profile_pic  = 'https://scontent-gmp1-1.xx.fbcdn.net/v/t1.18169-1/c0.16.148.116a/p148x148/11817213_10155879004550352_2443853221089824039_n.png?_nc_cat=1&ccb=1-3&_nc_sid=0c64ff&_nc_ohc=NAwfBdBbEykAX-_6niJ&_nc_ht=scontent-gmp1-1.xx&tp=30&oh=981c25a67f68d2fbfefd1cf69bcf06d3&oe=609A61A3'
                                    base64_bytes = base64.b64encode(requests.get(profile_pic).content)
                                    image_url = base64_bytes.decode('utf-8')

                                    if influencer_id not in facebook_id_list:
                                        print(influencer)
                                        k = len(facebook_pk_list)-1
                                        print('New influencer')
                                        print(requests.post('http://test.dabi-api.com/api/influencer/', json={"insta_id": influencer, "insta_pk":influencer_id , "profile_image": image_url}, headers=headers))
                                        sleep(13)
                                        response = requests.get(url+'?offset='+str(k), headers=headers)
                                        data = response.json()
                                        result = data.get('results', None)
                                        facebook_pk_list[result[-1]['insta_pk']] = result[-1]['pk']
                                        facebook_id_list.append(result[-1]['insta_pk'])

                                    A = set(facebook_id_list) & set(id_li)
                                    B = set(id_li)
                                    
                                    if A == B:
                                        return facebook_pk_list    
                            # t = False
                    i+=20
                             
    

facebook_pk_list = influencer_check()
def check_post(influencer_id):
    print('check post')
    post_list=[]
    pk = facebook_pk_list[str(influencer_id)]
    sleep(10)
    response = requests.get('http://test.dabi-api.com/api/influencer/'+str(pk)+'/feedback/?is-active=all', headers=headers)

    if response:
        try:
            data = response.json()
        except Exception as e:
            print('Invalid response data in check_post')
        if data:
            result = data.get('results')
            if result:
                for i in range(len(result)):
                    post_list.append(result[i]['post_id'])
                return post_list

def post_pk(pk1, post_id):
    print('find pk')
    url =f'http://test.dabi-api.com/api/influencer/{pk1}/feedback/?is-active=all'
    i=0
    while 1:
        sleep(10)
        response = requests.get(url+'&offset='+str(i), headers=headers)
        if response:
            try:
                data = response.json()
            except Exception as e:
                print('Invalid response data in post_pk')
                continue
            if data:
                result = data.get('results', None)
                sleep(1)
                if result:
                    for i2 in range(len(result)):
                        if post_id == result[i2]['post_id']:
                            pk = result[i2]['pk']
                            return pk
                        else:
                            print('No post')
                            i+=20

with open('dosiciety.json','rt', encoding='UTF8') as json_file:

    json_data_1 = json.load(json_file)
    id_list_1 = []     
    id_list = [] 
    json_data = []

    for i in range(len(json_data_1)):
        if json_data_1[i]['image'] != None:
            if "https://m.facebook.com/photo/" in json_data_1[i]['image']:
                continue
        if json_data_1[i]['image']== None and json_data_1[i]['video_thumbnail']==None:
            continue  
        if json_data_1[i]['post_id'] == None:
            continue 
        else: 
            json_data.append(json_data_1[i])

    for i in range(len(json_data)):

        influencer_id = json_data[i]['user_id']
        pk1 = facebook_pk_list[str(influencer_id)]
        url = json_data[i]['post_url']
        post_id = json_data[i]['post_id']
        id_list = check_post(influencer_id)
        if id_list == None:
            id_list = []

        if post_id in id_list:
            i+=1
            print('Already on the list')

        elif post_id not in id_list:
            id_list_1.append(post_id)
            print(id_list_1)
            if json_data[i]['image'] != None:
                image_url = json_data[i]['image']
            elif json_data[i]['image'] == None:
                image_url = json_data[i]['video_thumbnail']
                
            base64_bytes = base64.b64encode(requests.get(image_url).content)
            image_url = base64_bytes.decode('utf-8')

            date_posted_human = json_data[i]['time']
            date_posted_human = datetime.fromtimestamp(date_posted_human).strftime("%Y-%m-%d")
            captions = json_data[i]['text']                   
            sleep(10)              
            print('New post')
            print(requests.post(f'http://test.dabi-api.com/api/influencer/{pk1}/feedback/', json={"post_url": url, "post_id": post_id, "post_thumb_image":image_url ,"post_taken_at_timestamp": date_posted_human,
                                    "post_description": captions}, headers=headers))  
            

            if json_data[i]['images'] != None:
                
                for k in json_data[i]['images']:
                    
                    k.replace(r'\u0026', "&")
                    base64_bytes = base64.b64encode(requests.get(k).content)
                    display_url = base64_bytes.decode('utf-8')
                    sleep(1)
                    pk2 = post_pk(pk1, post_id)
                    sleep(10)
    
                    print(requests.post(f'http://test.dabi-api.com/api/influencer/{pk1}/feedback/{pk2}/image', json={"source": display_url}, headers=headers)) 
        
            if url != None:
                li = [0]
                li[0] = url
                print(li)
                
                posts = list(get_posts(post_urls = li, options={'comments': True}, cookies="cookies.txt", timeout=15))
                sleep(10)

                if posts[0]['comments_full'] == None:
                    i+=1

                if posts[0]['comments_full'] != None:
                    for post in posts[0]['comments_full']:
                        comments = post['comment_text']  
                        sleep(10)
                        print(requests.post(f'http://test.dabi-api.com/api/influencer/posts/{pk2}/comments/', json={"text": comments}, headers=headers))   
                        print("text", comments)   
                
                    

