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
                except ValueError:
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
            reader = csv.reader(csvfile, delimiter=' ')
            for row in reader:
                if len(row) < 10:
                    continue

                try:
                    timestamp = float(row[0])
                    response_header_size = int(row[1])
                    client_ip_address = row[2]
                    http_response_code = row[3]
                    response_size = int(row[4])
                    http_request_method = row[5]
                    url = row[6]
                    username = row[7]
                    type_access_destination_ip = row[8]
                    response_type = row[9]
                except ValueError:
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
    elif file_path.endswith('.json'):
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as jsonfile:
            try:
                data = json.load(jsonfile)
                if isinstance(data, list):
                    if all(isinstance(entry, list) and len(entry) >= 10 for entry in data):
                        for entry in data:
                            try:
                                timestamp = float(entry[0])
                                response_header_size = int(entry[1])
                                client_ip_address = entry[2]
                                http_response_code = entry[3]
                                response_size = int(entry[4])
                                http_request_method = entry[5]
                                url = entry[6]
                                username = entry[7]
                                type_access_destination_ip = entry[8]
                                response_type = entry[9]
                            except (ValueError, IndexError):
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
                else:
                    print(f"Invalid JSON format in file: {file_path}")
            except json.JSONDecodeError:
                print(f"Error decoding JSON file: {file_path}")
    else:
        print(f"Error: Unsupported file format for {file_path}")

    return logs

def most_frequent_ip(logs):
    ip_counter = Counter(entry["client_ip_address"] for entry in logs)
    if not ip_counter:
        return None
    most_frequent_ip = ip_counter.most_common(1)[0][0]
    return most_frequent_ip

def least_frequent_ip(logs):
    ip_counter = Counter(entry["client_ip_address"] for entry in logs)
    if not ip_counter:
        return None
    least_frequent_ip = ip_counter.most_common()[-1][0]
    return least_frequent_ip

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

    output_file = args.output.lower()

    try:
        if output_file.endswith('.json'):
            with open(args.output, 'w') as output_file:
                json.dump(output, output_file, indent=4)
        elif output_file.endswith('.csv'):
            with open(args.output, 'w', newline='') as output_file:
                writer = csv.writer(output_file)
                for key, value in output.items():
                    writer.writerow([key, value])
        elif output_file.endswith('.log'):
            with open(args.output, 'w') as output_file:
                for key, value in output.items():
                    output_file.write(f"{value}\n")
        else:
            print(f"Unsupported output file format: {args.output}")
            return
    except Exception as e:
        print(f"Error writing to output file '{args.output}': {e}")
        return

    print("Analysis completed. Results saved to:", args.output)

if __name__ == "__main__":
    main()
