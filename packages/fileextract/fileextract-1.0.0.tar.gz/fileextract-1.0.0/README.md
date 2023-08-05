# Description

Extracts files from .raw/.dd images by using sleuthkit

# Installation

```
apt install sleuthkit
pip install fileextract
```

# Usage

Create a config file with the following schema:

```json
    {
    "logPath": "fileextract.log",                         // Path to log file
    "raws": [                                               // List of .raw images
        {
            "path": "path/to/raws/**",                      // Path to the .raw image 
            "offset": 0,                                    // Offset where the file system starts
            "files": [                                      // The files which shall be extracted
                "/data/app/user.db"
            ]
        }
    ]
}
```

# Example

`python -m fileextract -c config.json`

```
################################################################################

fileextract by 5f0
Extracts files from .raw images by using sleuthkit

Current working directory: /path/to/fileextract

Datetime: 01/01/1970 10:11:12

################################################################################

 --> Target: path/to/raws/action_one.raw
    ---
     Create: path/to/raws/action_one.raw_files
    Extract: /data/app/user.db
    ---

 --> Target: path/to/raws/action_two.raw
    ---
     Create: path/to/raws/action_two.raw_files
    Extract: /data/app/user.db
    ---

################################################################################

Execution Time: 0.139446 sec

```

# License

MIT