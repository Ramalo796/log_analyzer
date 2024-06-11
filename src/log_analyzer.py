import argparse
import json
from collections import Counter

"""
Function to analyze the log file with predefined structure
"""
def log_file_reader(file_path):
    logs = []
    with open(file_path, 'r', encoding='utf-8', errors='ignore') as file:
        for row in file:
            parts = row.split()
            if len(parts) < 10:
                continue

            try:
                timestamp = float(parts[0])
                response_header_size = int(parts[1])
                client_ip_address = parts[2]
                http_response_code = parts[3]
                response_size = int(parts[4])
                http_request_method = parts[5]
                url = parts[6]
                username = parts[7]
                type_access_destination_ip = parts[8]
                response_type = parts[9]
            except ValueError as ve:
                print(f"Warning: Skipping row with invalid data: {row.strip()} (Error: {ve})")
                continue

            logs.append({
                "timestamp": timestamp,
                "response_header_size": response_header_size,
                "client_ip_address": client_ip_address,
                "http_response_code": http_response_code,
                "response_size": response_size,
                "http_request_method": http_request_method,
                "url": url,
                "username": username,
                "type_access_destination_ip": type_access_destination_ip,
                "response_type": response_type
            })
    return logs

"""
Function for analyzing the most frequent IP address among the input file
"""
def most_frequent_ip(logs):
    ip_counter = Counter(entry["client_ip_address"] for entry in logs)
    most_frequent_ip = ip_counter.most_common(1)[0][0]
    return most_frequent_ip

"""
Function for analyzing the least frequent IP address among the input file
"""
def least_frequent_ip(logs):
    ip_counter = Counter(entry["client_ip_address"] for entry in logs)
    least_frequent_ip = ip_counter.most_common()[-1][0]
    return least_frequent_ip

"""
Function for analyzing the events per second of the input file
"""
def events_per_second(logs):
    if not logs:
        return 0
    timestamps = [entry["timestamp"] for entry in logs]
    timestamps.sort()
    total_time = timestamps[-1] - timestamps[0]
    if total_time > 0:
        events_per_second = len(logs) / total_time
    else:
        events_per_second = 0
    return events_per_second

"""
Function for analyzing the total number of bytes exchanged among the input file
"""
def total_bytes_exchanged(logs):
    total_bytes = sum(entry["response_size"] for entry in logs)
    return total_bytes

def main():
    parser = argparse.ArgumentParser(description="Log Analyzer")
    parser.add_argument("input", nargs='+', help="Path to one or more input files")
    parser.add_argument("output", help="Path to a file to save output in JSON format")
    parser.add_argument("--mfip", action='store_true', help="Most frequent IP")
    parser.add_argument("--lfip", action='store_true', help="Least frequent IP")
    parser.add_argument("--eps", action='store_true', help="Events per second")
    parser.add_argument("--bytes", action='store_true', help="Total amount of bytes exchanged")
    args = parser.parse_args()

    if not (args.mfip or args.lfip or args.eps or args.bytes):
        print("Error: At least one analysis option (--mfip, --lfip, --eps, --bytes) must be specified")
        return

    logs = []
    for input_file in args.input:
        try:
            logs.extend(log_file_reader(input_file))
        except FileNotFoundError:
            print(f"Error: The file '{input_file}' does not exist")
            return
        except Exception as e:
            print(f"Error during processing of '{input_file}': {e}")
            return

    output = {}

    if args.mfip:
        output["most_frequent_ip"] = most_frequent_ip(logs)

    if args.lfip:
        output["least_frequent_ip"] = least_frequent_ip(logs)

    if args.eps:
        output["events_per_second"] = events_per_second(logs)

    if args.bytes:
        output["total_bytes"] = total_bytes_exchanged(logs)

    with open(args.output, 'w') as output_file:
        json.dump(output, output_file, indent=4)

if __name__ == "__main__":
    main()
