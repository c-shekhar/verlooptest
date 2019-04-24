from gevent import monkey
monkey.patch_all()

from flask import request, jsonify
from web import app, logger
import requests, grequests
from requests.exceptions import HTTPError, ConnectionError
from time import strftime
import traceback

@app.route('/repos', methods = ['GET','POST'])
def get_orgs_repos():
	'''
	RETURNS top three repositories of an organization(for valid organization-id).
	GIVES HTTP Error if organization doesn't exist.
	GIVES Connection Error in absence of internet.
	GIVES Invalid Request for Incorrect Request type or Payload.
	'''

	formatted_response = {'results' : []}
	## If request is a valid POST request
	if request.method == 'POST':
		try:
			## Fetching request payload
			payload = request.get_json()

			## If payload is None
			if not payload:
				return jsonify({'results' : [],
								'error' : "Invalid Request. Check request payload or content-type."})

			## If organization id is not present in payload
			if 'org' not in payload:
				return jsonify({'results' : [],
								'error' : "Organization-id not in payload"})
			
			## Getting organization-id from payload
			org_id = str(payload['org']).lower()
			try:
				## calling github api to fetch list of organization repos
				url = f"https://api.github.com/orgs/{org_id}/repos"
				response = requests.get(url)
				## checking response from github api for exception handling 
				response.raise_for_status()

			## In case we couldn't fetch from github
			except HTTPError as http_err:
				# print(f"HTTP error occurred: {http_err}")
				return jsonify({'results' : [],
								'error' : "HTTP error"})
			
			## In absence of network
			except ConnectionError as conn_err:
				# print(f"Connection error occurred: {conn_err}")
				return jsonify({'results' : [],
								'error' : "Connection error"})
			
			## In case there is any other error while fetching data from github
			except Exception as err:
				# print(f"Other error occurred: {err}")
				return jsonify({'results' : [],
								'error' : str(err)})
			
			response_headers = dict(response.headers)
			responses = response.json()

			## If response is paginated, check for 'Link' key in header
			if 'Link' in response_headers:
				link_info = response_headers['Link']
				## parse last page number
				num_pages = int(link_info.split(';')[1].split('page=')[-1].strip('>'))
				## make urls with query strings against each page
				urls = [f"{url}?page={page}" for page in range(2, num_pages + 1)]
				## asynchronously fetch from all urls
				rs = (grequests.get(u) for u in urls)
				rs = grequests.map(rs)
				## append each response to responses
				for r in rs:
					responses = responses + r.json() if r else []

			repos = []
			## Serializing data
			for repo_info in responses:
				repos.append(
							  {
								'name' : repo_info['name'],
								'stars' : repo_info['stargazers_count']
							  }
							)
			## Sorting by number of stars and picking the top 3
			formatted_response['results'] = sorted(repos,
												   key = lambda i: i['stars'],
												   reverse=True)[:3]

			## Returning the final serialized result
			return jsonify(formatted_response)
		
		## In case there is any other error while serving the request
		except Exception as e:
			return jsonify({'results' : [],
							'error':"Unknown error"})
	else:
		## Returning Invalid Request
		return jsonify({'results' : [],
						'error':"Invalid Request. Check if you are making a POST request."})

@app.after_request
def after_request(response):
	""" Logs after every request. """
	## This avoids the duplication of registry in the log,
	## since that 500 is already logged via @app.errorhandler.
	if response.status_code != 500:
		ts = strftime('[%Y-%b-%d %H:%M]')
		err = f"{ts} " \
			  f"{request.remote_addr} " \
			  f"{request.method} " \
			  f"{request.scheme} " \
			  f"{request.full_path} " \
			  f"{response.status} "
		logger.error(err)
	return response

@app.errorhandler(Exception)
def exceptions(error):
	""" Logs after every Exception. """
	ts = strftime('[%Y-%b-%d %H:%M]')
	tb = traceback.format_exc()
	err = f"{ts}" \
		  f"{request.remote_addr} " \
		  f"{request.method} " \
		  f"{request.scheme} " \
		  f"{request.full_path} " \
		  f"{tb} "
	logger.error(err)
	return "Internal Server Error", 500
