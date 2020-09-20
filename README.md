# Pocket Roam

**Description**

Fetches saved Pocket pages then parses for entities, keywords, and summarises all the pages in a format that can be uploaded to Roam

You need to export all your getpocket.com pages. This is available on: https://getpocket.com/options.
The downloaded page will be called ril_export.html and is stored in pocket_data/


The generated json files will be saved in data/


*Warning:*
1. It is slow.
2. For many pages it will fail. I have a separate script to fetch Twitter links but this requires API access.
3. Many times the summaries, and entities it generates are suboptimal :)
4. The generated JSON will somtimes be incorrect and not upload to Roam.


If you're still not discouraged:

**Requirements:**

1. pytorch 
2. transformers (https://github.com/huggingface/transformers)
3. spaCy (https://github.com/explosion/spaCy)*
4. beautifulsoup4
5. newspaper3k
6. requests

**Installation:**

Download spaCy English model with python -m spacy download en_core_web_sm

python roam_pocket.py
