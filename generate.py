import os
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.output_parsers import ResponseSchema, StructuredOutputParser
import logging
from datetime import datetime, timedelta
import requests
from config import OPENAI_API_KEY

# Set up logging
logging.basicConfig(level=logging.INFO)

# Define the output schema
output_parser = StructuredOutputParser.from_response_schemas([
    ResponseSchema(name="Dates", description="The dates of the event in format YYYY-MM-DD, separated by commas if "
                                             "multiple"),
    ResponseSchema(name="StartTime", description="The start time of the event in format HH:MM"),
    ResponseSchema(name="EndTime", description="The end time of the event in format HH:MM"),
    ResponseSchema(name="EventName", description="The name of the event"),
    ResponseSchema(name="Location", description="The location of the event"),
    ResponseSchema(name="Notes", description="Any additional notes about the event")
])

# Define the prompt template
prompt_template = ChatPromptTemplate.from_template(
    """
    Extract the following event details from this email content:

    Email Content:
    {email_content}

    {format_instructions}

    If a piece of information is not provided or cannot be determined, use null for its value. 
    For multiple dates, list them separated by commas.
    """
)

# Set up the language model
model = ChatOpenAI(temperature=0, model="gpt-4", openai_api_key=OPENAI_API_KEY)


def extract_event_details(email_content):
    try:
        # Generate the prompt
        prompt = prompt_template.format_messages(
            email_content=email_content,
            format_instructions=output_parser.get_format_instructions()
        )

        # Get the response from the model
        response = model.invoke(prompt)

        # Parse the response
        event_details = output_parser.parse(response.content)
        logging.info(f"Extracted event details: {event_details}")
        return event_details
    except Exception as e:
        logging.error(f"Error extracting event details: {e}")
        return None


def generate_calendar_link(event_details):
    try:
        # Parse the dates and times
        dates = [date.strip() for date in event_details['Dates'].split(',')]
        start_time = event_details['StartTime']
        end_time = event_details['EndTime']

        # Create calendar links for each date
        calendar_links = []
        for date in dates:
            start_datetime = datetime.strptime(f"{date}T{start_time}", "%Y-%m-%dT%H:%M")

            if end_time:
                end_datetime = datetime.strptime(f"{date}T{end_time}", "%Y-%m-%dT%H:%M")
            else:
                # If no end time is provided, set the event duration to 1 hour
                end_datetime = start_datetime + timedelta(hours=1)

            # Format dates for Google Calendar
            start_formatted = start_datetime.strftime("%Y%m%dT%H%M%S")
            end_formatted = end_datetime.strftime("%Y%m%dT%H%M%S")

            # Construct the link
            base_url = "https://calendar.google.com/calendar/render"
            params = {
                "action": "TEMPLATE",
                "text": event_details['EventName'],
                "dates": f"{start_formatted}/{end_formatted}",
                "details": event_details['Notes'] or "",
                "location": event_details['Location'] or ""
            }

            calendar_link = f"{base_url}?{requests.compat.urlencode(params)}"
            calendar_links.append(calendar_link)

        logging.info(f"Generated calendar links: {calendar_links}")
        return calendar_links
    except Exception as e:
        logging.error(f"Error generating calendar link: {e}")
        return None


def main():
    print("Paste the email content here. Type 'END' on a new line when done:")

    email_content = []
    while True:
        line = input()
        if line.strip().upper() == "END":
            break
        email_content.append(line)

    email_content = "\n".join(email_content).strip()

    if not email_content:
        logging.error("No email content provided. Please try again.")
        print("No email content provided. Please try again.")
        return

    # Step 1: Extract event details
    event_details = extract_event_details(email_content)

    if event_details:
        # Step 2: Generate Google Calendar links
        calendar_links = generate_calendar_link(event_details)

        if calendar_links:
            print("\nGoogle Calendar Links:")
            for i, link in enumerate(calendar_links, 1):
                print(f"Date {i}: {link}")
        else:
            print("Failed to generate Google Calendar links.")
    else:
        print("Failed to extract event details.")


if __name__ == "__main__":
    main()
