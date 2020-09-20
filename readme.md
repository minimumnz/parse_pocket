Fetch parse for entities, keywords, and summarise all the pages I've saved to Pocket.

You need to export all your getpocket.com pages. This is available on: https://getpocket.com/options.
The downloaded page will be called ril_export.html is stored in pocket_data/

Requirements:
pytorch 
transformers (https://github.com/huggingface/transformers)
spaCy (https://github.com/explosion/spaCy)
beautifulsoup4
newspaper3k

Download spaCy English model

python -m spacy download en_core_web_sm