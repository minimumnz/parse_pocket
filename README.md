# parse_pocket

# Description
Fetches page then parses for entities, keywords, and summarise all the pages I've saved to Pocket in a format that can be uploaded to Roam.

You need to export all your getpocket.com pages. This is available on: https://getpocket.com/options.
The downloaded page will be called ril_export.html and is stored in pocket_data/


The generated json files will be saved in data/


*Warnings*
This will generate json files that you can then upload to Roam. You can only upload about 10 at a time to
Roam and sometimes the json the script generates will be incorrect so it'll fail.

** For many pages it will fail. I have a separate script to fetch Twitter links but this requires API access.
** Many times the summaries, and entities it generates are suboptimal :)

If you're still not discouraged:

*Requirements:*

1. pytorch 
2. transformers (https://github.com/huggingface/transformers)
3. spaCy (https://github.com/explosion/spaCy)*
4. beautifulsoup4
5. newspaper3k

*Installation:*

Download spaCy English model with python -m spacy download en_core_web_sm

python roam_pocket.py
