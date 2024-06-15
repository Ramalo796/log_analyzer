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
            reader = csv.reader(csvfile)
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
            logs = json.load(jsonfile)
    else:
        print(f"Error: Unsupported file format for {file_path}")
    return logs

# Resto del código y funciones de análisis aquí...




