This library has been created to parse the logs of a file with a given format. In order to run this library, follow the steps below:

1. **Clone the Repository:**
   - Option A: Using git:
     If you have git installed, run the following command:
     ```
     git clone https://github.com/Ramalo796/log_analyzer.git
     ```
   - Option B: Download the ZIP from GitHub:
   	If you don't have git, you can download the repository as a ZIP file:
		- Go to the repository page on GitHub: [https://github.com/Ramalo796/log_analyzer](https://github.com/Ramalo796/log_analyzer)
		- Click the "Code" button and then click "Download ZIP"
		- Extract the contents of the ZIP file on your machine


2. **Install the Library:**
   - Navigate to the cloned or extracted repository directory:
     ```
     cd log_analyzer
     ```
   - Install the library using Python:
     ```
     pip install .
     ```

3. **Unzip the Log File:**
   - Option A: Using gunzip:
     If you have gunzip installed, run the following command:
     ```
     gunzip log_analyzer/data/inputs/access.log.gz
     ```
   - Option B: Use a Decompression Tool:
     If you don't have gunzip, you can use a graphical or command-line decompression tool to unzip the `access.log.gz` file

4. **Run the Library:**
   To run the library, use the following command:
   ```
   log-analyzer <input_file> <output_file> [--mfip] [--lfip] [--eps] [--bytes]
   ```
   Where:
- `<input_file>` is the input file with the logs.
- `<output_file>` is the file where the output will be saved in JSON format.
- `--mfip`: Most frequent IP.
- `--lfip`: Least frequent IP.
- `--eps`: Events per second.
- `--bytes`: Total amount of bytes exchanged




