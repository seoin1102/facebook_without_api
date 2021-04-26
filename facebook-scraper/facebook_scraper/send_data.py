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
    while 1:
        sleep(10)
        response = requests.get(url+'?offset='+str(i), headers=headers)
        print(response)
        # facebook_id_list= []
        facebook_id_list = open("facebook_id_list.txt","w+")
        facebook_id_list2 = []
        facebook_pk_list = {}
        if response:
            try:
                data = response.json()
            except Exception as e:
                print('Invalid response data in influencer_pk')
                continue
            if data:
                # We should use .get when we have a dictionary for safety reason
                result = data.get('results', None)

                # Check result is in correct form
                if result:        
                    for i2 in range(len(result)):
                        # facebook_id_list.append(result[i2]['insta_pk'])
                        facebook_id_list.writelines(result[i2]['insta_pk'])
                        facebook_pk_list[result[i2]['insta_pk']] = result[i2]['pk']
                        i+=20
                        if data['next']==None and len(facebook_id_list)%20 == len(result):
                            # facebook_id_list.append(result[i2]['insta_pk'])
                            facebook_id_list.writelines(result[i2]['insta_pk'])
                            facebook_pk_list[result[i2]['insta_pk']] = result[i2]['pk']
                            break          
                    with open('dosiciety1.json','rt', encoding='UTF8') as json_file:
                        json_data = json.load(json_file)
                
                        for i in range(len(json_data)):
                            influencer = json_data[i]['username']
                            print(influencer)
                            influencer_id = json_data[i]['user_id']
                            print(influencer_id)
                            profile_pic  = 'https://scontent-gmp1-1.xx.fbcdn.net/v/t1.18169-1/c0.16.148.116a/p148x148/11817213_10155879004550352_2443853221089824039_n.png?_nc_cat=1&ccb=1-3&_nc_sid=0c64ff&_nc_ohc=NAwfBdBbEykAX-_6niJ&_nc_ht=scontent-gmp1-1.xx&tp=30&oh=981c25a67f68d2fbfefd1cf69bcf06d3&oe=609A61A3'
                            base64_bytes = base64.b64encode(requests.get(profile_pic).content)
                            image_url = base64_bytes.decode('utf-8')
                            
                            facebook_id_list2.append(facebook_id_list.readlines ())
                            if influencer_id not in facebook_id_list2:
                                sleep(10)
                                print(requests.post('http://test.dabi-api.com/api/influencer/', json={"insta_id": influencer, "insta_pk":influencer_id , "profile_image": image_url}, headers=headers))
                                # facebook_id_list.append(influencer_id)
                                facebook_id_list.writelines(result[i2]['insta_pk'])
                                sleep(1)
                                print('New influencer')
                                facebook_id_list.close()
                                return facebook_pk_list

facebook_pk_list = influencer_check()
print(facebook_pk_list)
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
                    post_list.append(result[i]['post_url'])
                return post_list

def post_pk(pk1, post_url):
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
                        if post_url == result[i2]['post_url']:
                            pk = result[i2]['pk']
                            return pk
                        else:
                            print('No post')
                            i+=20
                    if data['next']==None:
                        break
            break            

with open('dosiciety1.json','rt', encoding='UTF8') as json_file:
    json_data = json.load(json_file)
    url_list = []     
    u_list = [] 
    
    for i in range(len(json_data)):
        influencer_id = json_data[i]['user_id']
        print(facebook_pk_list)
        pk1 = facebook_pk_list[str(influencer_id)]
        url = json_data[i]['post_url']
        u_list = check_post(influencer_id)
        if u_list == None:
            u_list = []

        if url in u_list:
            i+=1
            print('Already on the list')

        elif url not in u_list:
            url_list.append(url)
            print(url_list)
            image_url = json_data[i]['image']
            
            base64_bytes = base64.b64encode(requests.get(image_url).content)
            image_url = base64_bytes.decode('utf-8')
            date_posted_human = json_data[i]['time']
            date_posted_human = datetime.fromtimestamp(date_posted_human).strftime("%Y-%m-%d")
            captions = json_data[i]['text']                   
            sleep(10)              

            print(requests.post(f'http://test.dabi-api.com/api/influencer/{pk1}/feedback/', json={"post_url": url, "post_thumb_image":image_url ,"post_taken_at_timestamp": date_posted_human,
                                    "post_description": captions}, headers=headers))   


            for k in json_data[i]['images']:
                
                k.replace(r'\u0026', "&")
                base64_bytes = base64.b64encode(requests.get(k).content)
                display_url = base64_bytes.decode('utf-8')
                sleep(1)
                pk2 = post_pk(pk1, url)
                sleep(10)
   
                print(requests.post(f'http://test.dabi-api.com/api/influencer/{pk1}/feedback/{pk2}/image', json={"source": display_url}, headers=headers))      
            
            li = [0]
            li[0] = url
            posts = list(get_posts(post_urls = li, options={'comments': True}, cookies="cookies.txt", timeout=15))
            sleep(10)

            if posts[0]['comments_full'] == None:
                i+=1

            if posts[0]['comments_full'] != None:
                for post in posts[0]['comments_full']:
                    comments = post['comment_text']  
                    sleep(10)
                    print(requests.post(f'http://test.dabi-api.com/api/influencer/posts/{pk2}/comments/', json={"text": comments}, headers=headers))      
               
                

