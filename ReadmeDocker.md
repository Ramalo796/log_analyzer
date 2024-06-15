This library has been created to parse the logs of a file with a given format. In order to run this library with DockerFile, follow the steps below:

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
     If you don't have gunzip, you can use a graphical or command-line decompression tool to unzip the `access.log.gz` file in log_analyzer/data/inputs/

4. **Build the Docker image:**
   Make sure you are on the 'log_analyzer' directory, then build the Docker image:
   ```
   docker build -t log_analyzer_image .
   ```
5. **Run the Docker container**
   Run the Docker container, mounting the local outputs directory:
   ```
   docker run -v "$(pwd)/outputs:/app/data/outputs" log_analyzer_image
   ```

6. **Atention**
The code is prepared to parse different input formats (.cvs, .json and .log), the repository only has an example of .log, if you want to try another type, the code can do it, but it is prepared for csv files with whitespace separations, json files with log data without headers and .log files with whitespace separations.
  
