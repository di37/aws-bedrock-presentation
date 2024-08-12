# AWS Bedrock Presentation - Basic Examples + YouTube Notes Generator

This includes some basic text generation applications and youtube notes generator that was created using AWS Bedrock service.

## Setup Environment

1. Create environment
```bash
conda create -n aws_bedrock python=3.11
```

2. Activate environment
```bash
conda activate aws_bedrock
```

3. Install dependencies
```bash
pip install -r requirements.txt
```

## Run Applications

To run `invoke_app.py` and `converse_app.py` first navigate to the folder `basic-examples`:
```bash
cd basic-examples
```

For `invoke_app.py`:
```bash
streamlit run invoke_app.py
```

![Image](basic-examples/screenshots/1.png?raw=true)

For ``converse_app.py``:
```bash
streamlit run converse_app.py
```

![Image](basic-examples/screenshots/2.png?raw=true)

![Image](basic-examples/screenshots/3.png?raw=true)

Paragraph taken from: https://www.khaleejtimes.com/entertainment/shah-rukh-khan-and-sons-to-dub-mufasa-the-lion-king

To run `youtube_notes_generator.py` first navigate to the document `youtube-notes-generator` folder:
```bash
cd youtube-notes-generator
```

```bash
streamlit run youtube_notes_generator.py
```

![Image](youtube-notes-generator/screenshots/4.png?raw=true)

Link of the video: https://youtu.be/1bUy-1hGZpI

## Misc.

Please find the presentation of the talk - `Amazon Bedrock.pptx`. 