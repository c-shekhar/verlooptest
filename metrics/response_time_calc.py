import requests
def calculate_average_reponse_time(url, data={'org':'verloop'}):
	time  = []
	for i in range(10):
		response = requests.post(url, json=data, timeout=10)
		t = response.elapsed.total_seconds()
		# print(t)
		time.append(t)
	avg_time = float(sum(time))/len(time)
	return avg_time

if __name__ == '__main__':
	url = "http://3.84.219.59:80/repos"
	# avg_time = calculate_average_reponse_time(url)
	# print(f"Average response time is {avg_time}")
	org_avgs = []
	orgs = ['adobe','netflix','google','facebook']
	for org in orgs:
		avg_time = calculate_average_reponse_time(url,data={'org':org})
		org_avgs.append(avg_time)
		print(f"Average response time for {org} is {avg_time}")
	avg_time = float(sum(org_avgs))/len(org_avgs)
	print(f"Average response time is {avg_time}")