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

For ``converse_app.py``:
```bash
streamlit run converse_app.py
```

To run `youtube_notes_generator.py` first navigate to the document `youtube-notes-generator` folder:
```bash
cd youtube-notes-generator
```

```bash
streamlit run youtube_notes_generator.py
```