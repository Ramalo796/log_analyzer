import argparse
import json
import csv
from collections import Counter

def log_file_reader(file_path):
    logs = []
    if file_path.endswith('.log'):
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
    elif file_path.endswith('.csv'):
        with open(file_path, newline='', encoding='utf-8', errors='ignore') as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                if len(row) < 10:
                    continue
                try:
                    logs.append({
                        "timestamp": float(row[0]),
                        "response_header_size": int(row[1]),
                        "client_ip_address": row[2],
                        "http_response_code": row[3],
                        "response_size": int(row[4]),
                        "http_request_method": row[5],
                        "url": row[6],
                        "username": row[7],
                        "type_access_destination_ip": row[8],
                        "response_type": row[9]
                    })
                except ValueError as ve:
                    print(f"Warning: Skipping row with invalid data: {row} (Error: {ve})")
                    continue
    elif file_path.endswith('.json'):
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as jsonfile:
            logs = json.load(jsonfile)
    else:
        print(f"Error: Unsupported file format for {file_path}")
    return logs

def most_frequent_ip(logs):
    ip_counter = Counter(entry["client_ip_address"] for entry in logs)
    most_frequent_ip = ip_counter.most_common(1)[0][0]
    return most_frequent_ip

def least_frequent_ip(logs):
    ip_counter = Counter(entry["client_ip_address"] for entry in logs)
    least_frequent_ip = ip_counter.most_common()[-1][0]
    return least_frequent_ip

def events_per_second(logs):
    if not logs:
        return 0
    timestamps = [entry["timestamp"] for entry in logs]
    total_time = max(timestamps) - min(timestamps)
    return len(logs) / total_time if total_time > 0 else 0

def total_bytes_exchanged(logs):
    return sum(entry["response_size"] for entry in logs)

def save_output(output, output_file, output_format):
    if output_format == 'json':
        with open(output_file, 'w') as f:
            json.dump(output, f, indent=4)
    elif output_format == 'txt':
        with open(output_file, 'w') as f:
            for key, value in output.items():
                f.write(f"{key}: {value}\n")
    else:
        print(f"Error: Unsupported output format '{output_format}'")

def main():
    parser = argparse.ArgumentParser(description="Log Analyzer")
    parser.add_argument("input", nargs='+', help="Path to one or more input files")
    parser.add_argument("output", help="Path to a file to save output")
    parser.add_argument("--output-format", choices=['json', 'txt'], default='json', help="Format of the output file")
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

    save_output(output, args.output, args.output_format)

    print("The output is:")
    print(output)

if __name__ == "__main__":
    main()


