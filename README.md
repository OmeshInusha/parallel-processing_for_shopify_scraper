# parallel-processing_for_shopify_scraper
This tool allows you to run multiple instances of a script (ssm.py) simultaneously, each with its own input parameter. It monitors each instance and automatically restarts any that terminate. It also supports scheduled restarts based on priority levels.

# Multi-Instance Script Manager

A Python utility for managing and maintaining multiple instances of a script running in parallel with automatic restart functionality.

## Overview

This tool allows you to run multiple instances of a script ( `ssm.py` , shopify scraper - 'https://github.com/OmeshInusha/shopify_products_scraper' ) simultaneously, each with its own input parameter. It monitors each instance and automatically restarts any that terminate. It also supports scheduled restarts based on priority levels.

## Features

- Run multiple script instances in parallel
- Each instance runs with a unique input parameter
- Automatic monitoring and restarting of terminated instances
- Configurable restart intervals based on priority levels
- Stdout and stderr output logging for each instance

## Requirements

- Python 3.x

## Usage

```bash
python mcssm.py input_file.txt priority
```

### Parameters

- `input_file.txt`: A text file containing input values (one per line) to be passed to each script instance
- `priority`: A value between 1-10 that determines the restart interval
  - Priority 1 = 12 days between restarts
  - Priority 10 = 2 days between restarts

## How It Works

1. The script reads input values from the specified file
2. For each input value, it starts an instance of `ssm.py`
3. Each instance is monitored in a separate thread
4. If an instance terminates, it is automatically restarted with the same input
5. All processes are restarted at intervals determined by the priority parameter

## Fair Data Usage

The script includes a fair data usage mechanism that maps priority levels to restart intervals:

| Priority | Restart Interval (Days) |
|----------|------------------------|
| 1        | 12                     |
| 2        | 11                     |
| 3        | 10                     |
| 4        | 9                      |
| 5        | 8                      |
| 6        | 7                      |
| 7        | 6                      |
| 8        | 5                      |
| 9        | 4                      |
| 10       | 3                      |

## Example

Create a file `inputs.txt` with the following content:
```
parameter1
parameter2
parameter3
```

Then run:
```bash
python mcssm.py inputs.txt 5
```

This will start 3 instances of `ssm.py`, each running with one of the parameters, and restart them every 8 days (priority 5).

## Notes

- Make sure `ssm.py` is in the same directory as `mcssm.py` or provide the full path
- The script will continue running indefinitely until manually terminated
- Each instance's output is prefixed with its instance ID for easy identification
