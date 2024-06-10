import argparse
import json
from collections import Counter

def parse_log_file(file_path):
    """
    Función para analizar el archivo de registro y devolver una lista de entradas analizadas.
    """
    parsed_entries = []

    try:
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as file:
            for line in file:
                parts = line.split()
                if len(parts) < 10:
                    continue

                timestamp = float(parts[0])
                response_header_size = int(parts[1])
                client_ip = parts[2]
                http_response_code = parts[3]
                response_size = int(parts[4])
                http_request_method = parts[5]
                url = parts[6]
                username = parts[7]
                access_info = parts[8]
                response_type = parts[9]

                parsed_entries.append({
                    "timestamp": timestamp,
                    "response_header_size": response_header_size,
                    "client_ip": client_ip,
                    "http_response_code": http_response_code,
                    "response_size": response_size,
                    "http_request_method": http_request_method,
                    "url": url,
                    "username": username,
                    "access_info": access_info,
                    "response_type": response_type
                })
    except FileNotFoundError:
        print(f"Error: El archivo '{file_path}' no existe.")
    except Exception as e:
        print(f"Error al procesar el archivo '{file_path}': {e}")

    return parsed_entries

def analyze_most_frequent_ip(entries):
    """
    Función para analizar la IP más frecuente en las entradas analizadas.
    """
    ip_counter = Counter(entry["client_ip"] for entry in entries)
    most_frequent_ip = ip_counter.most_common(1)[0][0]
    return most_frequent_ip

def analyze_least_frequent_ip(entries):
    """
    Función para analizar la IP menos frecuente en las entradas analizadas.
    """
    ip_counter = Counter(entry["client_ip"] for entry in entries)
    least_frequent_ip = ip_counter.most_common()[-1][0]
    return least_frequent_ip

def analyze_events_per_second(entries):
    """
    Función para analizar los eventos por segundo en las entradas analizadas.
    """
    timestamps = [entry["timestamp"] for entry in entries]
    timestamps.sort()
    time_diff = timestamps[-1] - timestamps[0]
    events_per_second = len(entries) / time_diff if time_diff > 0 else 0
    return events_per_second

def analyze_total_bytes_exchanged(entries):
    """
    Función para analizar el total de bytes intercambiados en las entradas analizadas.
    """
    total_bytes = sum(entry["response_size"] for entry in entries)
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

    all_entries = []
    for input_file in args.input:
        all_entries.extend(parse_log_file(input_file))

    output_data = {}

    if args.mfip:
        output_data["most_frequent_ip"] = analyze_most_frequent_ip(all_entries)

    if args.lfip:
        output_data["least_frequent_ip"] = analyze_least_frequent_ip(all_entries)

    if args.eps:
        output_data["events_per_second"] = analyze_events_per_second(all_entries)

    if args.bytes:
        output_data["total_bytes"] = analyze_total_bytes_exchanged(all_entries)

    print(output_data)

    with open(args.output, 'w') as output_file:
        json.dump(output_data, output_file, indent=4)

if __name__ == "__main__":
    main()



