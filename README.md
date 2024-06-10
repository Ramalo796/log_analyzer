# log_analyzer

This library has been created to parse the logs of a file with a given format.
In order to run this library follow the steps below:

1: clone the repository using the command --> git clone https://github.com/Ramalo796/log_analyzer.git

2: install the library using the command --> python setup.py install

3: Inside the log_analyzer/data/inputs folder, there is a file called access.log.gz with the logs information, you must unzip it

4: In order to run the library you will use the following command --> log-analyzer <input_file>  <output_file> --mfip --lfip --eps --bytes
  o --mfip: most frequent IP
  o --lfip: least frequent IP
  o --eps: events per second
  o --bytes: total amount of bytes exchanged
  
  Please note that the output will be in json format.
