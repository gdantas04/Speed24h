import speedtest, time, json
from datetime import datetime
import matplotlib.pyplot as plt

st = speedtest.Speedtest()

def getDU():
    d = int(st.download() / 1000000)  # Mbps
    u = int(st.upload() / 1000000)    # Mbps
    return d, u


def generate_graph(file_path):
    with open(file_path) as f:
        data = json.load(f)
    
    times = list(data.keys())
    download_speeds = [data[time]["D"] for time in times]
    upload_speeds = [data[time]["U"] for time in times]

    plt.figure(figsize=(10, 5))
    plt.plot(times, download_speeds, label='Download Speed (Mbps)', color='blue')
    plt.plot(times, upload_speeds, label='Upload Speed (Mbps)', color='red')
    plt.xlabel('Time')
    plt.ylabel('Speed (Mbps)')
    plt.title('Internet Over 24 Hours')
    plt.legend()
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig('internet24h.png', dpi=300, bbox_inches='tight')  


def run_tests_for_24_hours():
	total_tests = 144  # 1 test every 10 minutes
	interval = 600     # 10 min

	for i in range(total_tests):
		start_time = time.time()  
		
		try:
			d, u = getDU()
		except Exception:
			d, u = -10,-10

		time_now = datetime.now().strftime("%H:%M")
		
		with open('speed24h.json') as f:
			data = json.load(f)
			
		data[time_now] = {"D":d, "U":u}
					
		with open('speed24h.json', 'w') as f:
			json.dump(data, f)


		elapsed_time = time.time() - start_time  
		time_to_wait = max(0, interval - elapsed_time)  
		time.sleep(time_to_wait)
	
	generate_graph('speed24h.json')

run_tests_for_24_hours()
