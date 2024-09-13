# Calendar Event Extractor

The Calendar Event Extractor is a Python tool that automatically extracts event details from unstructured text, such as emails or messages, and generates Google Calendar links for easy event creation. This tool leverages the power of OpenAI's GPT-4 language model to understand and extract relevant event information.

## Features

- Extracts event details such as dates, start time, end time, event name, location, and notes from unstructured text
- Generates Google Calendar links for quick event creation
- Handles multiple event dates and missing event details gracefully
- Uses OpenAI's GPT-4 language model for accurate event information extraction

## Requirements

- Python 3.x
- `langchain_openai` package
- OpenAI API key

## Installation

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/calenderator.git
   ```

2. Navigate to the project directory:
   ```
   cd calenderator
   ```

3. Install the required packages:
   ```
   pip install -r requirements.txt
   ```

4. Create a `config.py` file in the project directory and add your OpenAI API key:
   ```python
   OPENAI_API_KEY = "your_api_key_here"
   ```

## Usage

1. Run the script:
   ```
   python generate.py
   ```

2. Paste the email content or unstructured text containing the event details.

3. Type 'END' on a new line when done.

4. The script will extract the event details and generate Google Calendar links.

5. Click on the generated links to create the events in your Google Calendar.

## Example

Here's an example of how to use the Calendar Event Extractor:

1. Run the script:
   ```
   python generate.py
   ```

2. Paste the email content:
   ```
   Hi everyone,

   We have an upcoming team meeting scheduled for next Monday, May 15th, at 10:30 AM. The meeting will take place in the main conference room on the 3rd floor.

   Please come prepared to discuss the project timeline and any roadblocks you're facing. The meeting is expected to last around 1 hour.

   Let me know if you have any questions!

   Best,
   John
   ```

3. Type 'END' on a new line.

4. The script will output the generated Google Calendar link:
   ```
   Google Calendar Links:
   Date 1: https://calendar.google.com/calendar/render?action=TEMPLATE&text=Team+Meeting&dates=20230515T103000/20230515T113000&details=Please+come+prepared+to+discuss+the+project+timeline+and+any+roadblocks+you're+facing.&location=Main+Conference+Room,+3rd+Floor
   ```

5. Click on the link to create the event in your Google Calendar.