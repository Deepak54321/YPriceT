# -*- coding:utf8 -*-
# !/usr/bin/env python
# Copyright 2017 Google Inc. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from __future__ import print_function
from future.standard_library import install_aliases
install_aliases()

from urllib.parse import urlparse, urlencode
from urllib.request import urlopen, Request
from urllib.error import HTTPError

import json
import os

from flask import Flask
from flask import request
from flask import make_response

# Flask app should start in global layout
app = Flask(__name__)


@app.route('/webhook', methods=['POST'])
def webhook():
    req = request.get_json(silent=True, force=True)

    print("Request:")
    print(json.dumps(req, indent=4))

    res = processRequest(req)
    res = json.dumps(res, indent=4)
    # print(res)
    r = make_response(res)
    r.headers['Content-Type'] = 'application/json'
    return r


def processRequest(req):
	if req.get("result").get("action") =="Priceapi":
		baseurl = "http://www.yamaha-motor-india.com/iym-web-api//51DCDFC2A2BC9/statewiseprice/getprice?product_profile_id=salutorxspcol&state_id=240"
		full_url = baseurl  
		result = urlopen(full_url).read()
		data = json.loads(result)
		responseData = data.get('responseData')
		product_price = responseData.get('product_price')
		price = product_price[0]['price']	
		speech = 'Price is ' + price		
		return {
        		"speech": speech,
        		"displayText": speech,
       			# "data": data,
        		# "contextOut": [],
        		"source": "apiai-weather-webhook-sample"
    			}
	if req.get("result").get("action") =="Dealerapi":
		result = req.get("result")
		parameters = result.get("parameters")
		state=parameters.get('State')
		city=parameters.get('geo-city')
		baseurl = "http://www.yamaha-motor-india.com/iym-web-api//51DCDFC2A2BC9/network/search?type=sales&profile_id=gujarat&city_profile_id=ahmedabad"
		full_url = baseurl  
		result = urlopen(full_url).read()
		data = json.loads(result)
		responseData = data.get('responseData')
		speech=""
		dealers = responseData.get('dealers')
		if dealers is None:
			speech="No Dealer Found in your city please check the city you entered"		
		for i in range(len(dealers)):
			dealername = dealers[i]['dealer_name']
			dealeraddress=dealers[i]['dealer_address']
			dealersalmgrmob=dealers[i]['sales_manager_mobile']
			speech+='Dealer name :' + dealername + '\n'  + 'Dealer Address :' + dealeraddress + '\n'  + 'Dealer Salese Manager Mobile No :' + dealersalmgrmob + '\n' + '\n' 
		return {
			"speech":speech,
			"displayText":speech,
			}
	if req.get("result").get("action") =="intro":
	    return {
		      'speech': 'When',
              'displayText': 'When',
              'messages': 
              [
               {'title': 'Please choose one of the following options',
                'replies': ['Product Enquiry',
                            'Test Drive',
                            'Complaints',
                            'Yamaha News'],
                'type': 2}
              ],
              'source': 'dimwei.com'
		}
	
if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))

    print("Starting app on port %d" % port)

    app.run(debug=False, port=port, host='0.0.0.0')
