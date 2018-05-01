# Coursera Dump

Saves Coursera course info to xlsx file.

Since it's way too long to process all the courses,
the script takes the first 20 of them. (This can be changed using `-n` switch).

By default, the results are saved to `output.xlsx` file. (Change this with `-f` switch).

### Usage example
```
$ python3 coursera.py -n 5 -f test.xlsx
INFO:root:fetching course urls...
INFO:root:fetching https://www.coursera.org/learn/gamification...
INFO:root:fetching https://www.coursera.org/learn/missing-data...
INFO:root:fetching https://www.coursera.org/learn/vital-signs...
INFO:root:fetching https://www.coursera.org/learn/modern-art-ideas...
INFO:root:fetching https://www.coursera.org/learn/evolvinguniverse...
INFO:root:successfully saved to test.xlsx
```

### Installation

The script requires Python 3. Other dependencies are installed with
``` pip3 install -r requirements.txt ```

# Project Goals

The code is written for educational purposes. Training course for web-developers - [DEVMAN.org](https://devman.org)
