from flask import Flask, request, jsonify, render_template
import selectorlib
import requests
from dateutil import parser as dateparser
app = Flask(__name__)
extractor = selectorlib.Extractor.from_yaml_file('etsy_selectors.yml')

def getReviews(url):
    """
    Purpose: Returns the reviews page for a product on Amazon.  

    sample url:
    https://www.amazon.com/MONDAY-MOOSE-Decorative-Reversible-Included/dp/B08H4KJPV7/ref=cm_cr_arp_d_product_top?ie=UTF8
    input url = 'https://www.amazon.com/MONDAY-MOOSE-Decorative-Reversible-Included/dp/B08H4KJPV7/ref=cm_cr_arp_d_product_top?ie=UTF8'

    target url = 'https://www.amazon.com/MONDAY-MOOSE-Decorative-Reversible-Included/product-reviews/B08H4KJPV7/ref=cm_cr_dp_d_show_all_btm?ie=UTF8&reviewerType=all_reviews'
    """
    if 'pageNumber' in url:
        return url
    """
    page_num = None
    if p > 0:
        page_num = url[p+11]
    print(p) # -1 if no page, else page no.
    """
    i = url.find('/dp/')
    j = url[i+4:].find('/') 
    product_id = url[i+4: i+4+j]
    
    target_url = url[:i] + '/product-reviews/' + product_id + '/ref=cm_cr_dp_d_show_all_btm?ie=UTF8&reviewerType=all_reviews' 
    # need
    #https://www.amazon.com/MONDAY-MOOSE-Decorative-Reversible-Included/product-reviews/B08H4KJPV7/ref=cm_cr_dp_d_show_all_btm?ie=UTF8&reviewerType=all_reviews
    return target_url

def scrape(url):    
    headers = {
        'authority': 'www.amazon.com',
        'pragma': 'no-cache',
        'cache-control': 'no-cache',
        'dnt': '1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (X11; CrOS x86_64 8172.45.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.64 Safari/537.36',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'sec-fetch-site': 'none',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-dest': 'document',
        'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
    }

    # Download the page using requests
    print("Downloading %s"%url)
    
    # UNCOMMENT AS NEEDED:
    # url = getReviews(url) 
    
    r = requests.get(url, headers=headers)
    # Simple check to check if page was blocked (Usually 503)
    if r.status_code > 500:
        if "To discuss automated access to Amazon data please contact" in r.text:
            print("Page %s was blocked by Amazon. Please try using better proxies\n"%url)
        else:
            print("Page %s must have been blocked by Amazon as the status code was %d"%(url,r.status_code))
        return None

    # Pass the HTML of the page and create 
    data = extractor.extract(r.text,base_url=url)
    print(data)
    reviews = []
    """
    for r in data['reviews']:
        r["product"] = data["product_title"]
        r['url'] = url
        if 'verified' in r:
            if 'Verified Purchase' in r['verified']:
                r['verified'] = 'Yes'
            else:
                r['verified'] = 'Yes'
        r['rating'] = r['rating'].split(' out of')[0]
        date_posted = r['date'].split('on ')[-1]
        if r['images']:
            r['images'] = "\n".join(r['images'])
        r['date'] = dateparser.parse(date_posted).strftime('%d %b %Y')
        reviews.append(r)
    
        #Notes: If there are issues, try:
        #puppeteer / headless browsing : selenium
        

    histogram = {}
    for h in data['histogram']:
        histogram[h['key']] = h['value']
    data['histogram'] = histogram
    data['average_rating'] = float(data['average_rating'].split(' out')[0])
    data['reviews'] = reviews
    d = data['number_of_reviews'].split(' ')[0]
    d = d.replace(',', '')
    data['number_of_reviews'] = int(d)
    """
    return data 
    
@app.route('/')
def api():
    url = request.args.get('url',None)
    if url:
        data = scrape(url)
        return jsonify(data)
    else:
        return render_template('index.html')
    return jsonify({'error':'URL to scrape is not provided'}),400