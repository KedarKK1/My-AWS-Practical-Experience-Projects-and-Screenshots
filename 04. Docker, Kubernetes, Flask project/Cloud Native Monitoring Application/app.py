# psutil (process and system utilities) - cross-platform library for retrieving information on running processes and system utilization (CPU, memory, disks, network, sensors) in Python.
# It is useful mainly for system monitoring, profiling and limiting process resources and management of running processes.
# It implements many functionalities offered by classic UNIX command line tools such as ps, top, iotop, lsof, netstat, ifconfig, free and others
import psutil
from flask import Flask

app = Flask(__name__)


@app.route('/')
def index():
    cpu_percentage_usage = psutil.cpu_percent()
    cpu_stats = psutil.cpu_stats()
    mem_percentage_usage = psutil.virtual_memory().percent

    Message = None

    if(mem_percentage_usage > 80 or cpu_percentage_usage > 80):
        Message = "High CPU or Memory utilization detected. Please scale UP!"

    return f'Number of cores in system {psutil.cpu_count()} <br> Number of physical cores in system <br> CPU Utilization: {cpu_percentage_usage} <br> CPU Stats: {cpu_stats} <br> Memory Utilization: {mem_percentage_usage}'


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
