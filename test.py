import requests
import json

try:
    response = requests.post(
        "http://127.0.0.1:8080/v1/monthlyreport",
        json={
            "title": "test",
            "message": "I was working on agile",
            "feedback": "No Feedback"
        },
        stream=True  # Crucial for handling streamed responses
    )

    if response.status_code == 200:
        for line in response.iter_lines():
            print(line)
            # The lines from the stream are bytes, so you need to decode them
            decoded_line = line.decode('utf-8')

            # SSE events typically start with "data: "
            if decoded_line.startswith("data: "):
                # Extract the JSON payload
                json_data = decoded_line[len("data: "):]
                try:
                    # Parse the JSON and print the results
                    result = json.loads(json_data)
                    print(result)
                except json.JSONDecodeError:
                    print(f"Error decoding JSON: {json_data}")
            else:
                # Optionally, print other event types or keep it silent
                # print(f"Received non-data line: {decoded_line}")
                pass
    else:
        print(f"Request failed with status code: {response.status_code}")
        print(response.text)

except requests.exceptions.RequestException as e:
    print(f"An error occurred: {e}")