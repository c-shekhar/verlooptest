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
	url = "http://18.205.114.19:80/repos"
	avg_time = calculate_average_reponse_time(url)
	print(f"Average response time is {avg_time}")
