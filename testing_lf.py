import boto3
import json
import concurrent.futures

lambda_client = boto3.client('lambda')


def main(img_url,url):
    payload = {
        'url1': img_url,
        'url2': url['url']
    }
    response = lambda_client.invoke(
        FunctionName='test',
        InvocationType='RequestResponse',
        Payload=json.dumps(payload)
    )
    response_payload = json.loads(response['Payload'].read())
    print(response_payload)
    score = response_payload['similarity_score']
    url['score'] = score
    return url

def similarity_score(img_url, all_urls):
    results = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=200) as executor:
        futures = [executor.submit(main, img_url, url) for url in all_urls]
        for future in concurrent.futures.as_completed(futures):
            results.append(future.result())
    return results




img_url = 'https://gtsdashbucket.s3.eu-west-1.amazonaws.com/R.jpeg'
all_urls = json.load(open('res.json'))

if __name__ == '__main__':
    similarity_scores = similarity_score(img_url,all_urls)
    with open('out.json','w',encoding='utf=8') as j:
        json.dump(similarity_scores,j,indent=4,ensure_ascii=False)
    # url = {'url':'https://avatars.mds.yandex.net/i?id=0d6372dce336c04b1959787bb5c178511bfb4c07-4589529-images-thumbs&n=13'}
    # r = main(img_url,url)
    # print(r)
