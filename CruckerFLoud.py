import requests
import time
from concurrent.futures import ThreadPoolExecutor

def print_logo():
    logo = r"""
   _____                 _        ______ _                 _ 
  / ____|               | |      |  ____| |               | |
 | |     _ __ _   _  ___| | _____| |__  | | ___  _   _  __| |
 | |    | '__| | | |/ __| |/ / _ \  __| | |/ _ \| | | |/ _` |
 | |____| |  | |_| | (__|   <  __/ |    | | (_) | |_| | (_| |
  \_____|_|   \__,_|\___|_|\_\___|_|    |_|\___/ \__,_|\__,_|

               Advanced Web Testing Tool by CyberPhantom9288
    """
    print(logo)

def send_request(method, url):
    try:
        if method == 'GET':
            response = requests.get(url, timeout=5)
        elif method == 'POST':
            payload = {"sample": "data"}  # Customize POST data if needed
            response = requests.post(url, json=payload, timeout=5)
        else:
            return "Invalid Method"
        return response.status_code
    except Exception as e:
        return f"Error: {str(e)}"

def load_test(method, url, threads, duration):
    print(f"[+] Running Load Test on {url} ({method}) for {duration} seconds with {threads} threads")
    end_time = time.time() + duration
    with ThreadPoolExecutor(max_workers=threads) as executor:
        while time.time() < end_time:
            futures = [executor.submit(send_request, method, url) for _ in range(threads)]
            for future in futures:
                print(f"Status: {future.result()}")

def stress_test(method, url, max_threads, duration):
    print(f"[+] Running Stress Test on {url} ({method}) up to {max_threads} threads")
    for t in range(10, max_threads + 1, 10):
        print(f"[!] Stressing with {t} threads")
        load_test(method, url, t, duration)

def spike_test(method, url, threads, duration, spike_time):
    print(f"[+] Running Spike Test on {url} ({method})")
    load_test(method, url, threads, duration)
    print(f"[!!!] Spiking traffic with {threads * 5} threads for {spike_time} seconds")
    load_test(method, url, threads * 5, spike_time)
    print(f"[+] Returning to normal load")
    load_test(method, url, threads, duration)

def soak_test(method, url, threads, duration):
    print(f"[+] Running Soak Test on {url} ({method}) for {duration} seconds with {threads} threads")
    load_test(method, url, threads, duration)

def main():
    print_logo()
    while True:
        url = input("\nEnter target URL (or type 'exit' to quit): ").strip()
        if url.lower() == "exit":
            print("Exiting CruckerFloud. Goodbye!")
            break

        method = input("HTTP Method (GET/POST or 'exit' to quit): ").strip().upper()
        if method == "EXIT":
            print("Exiting CruckerFloud. Goodbye!")
            break
        if method not in ['GET', 'POST']:
            print("Invalid HTTP method. Please enter GET or POST.")
            continue

        print("\nSelect Test Type:")
        print("1. Load Test")
        print("2. Stress Test")
        print("3. Spike Test")
        print("4. Soak Test")
        print("Type 'exit' to quit.")
        choice = input("Enter choice: ").strip()
        if choice.lower() == "exit":
            print("Exiting CruckerFloud. Goodbye!")
            break

        if choice == '1':
            threads = int(input("Number of threads: "))
            duration = int(input("Test duration (seconds): "))
            load_test(method, url, threads, duration)
        elif choice == '2':
            max_threads = int(input("Max threads: "))
            duration = int(input("Each level duration (seconds): "))
            stress_test(method, url, max_threads, duration)
        elif choice == '3':
            threads = int(input("Base threads: "))
            duration = int(input("Base duration (seconds): "))
            spike_time = int(input("Spike duration (seconds): "))
            spike_test(method, url, threads, duration, spike_time)
        elif choice == '4':
            threads = int(input("Number of threads: "))
            duration = int(input("Test duration (seconds): "))
            soak_test(method, url, threads, duration)
        else:
            print("Invalid option!")

if __name__ == "__main__":
    main()
