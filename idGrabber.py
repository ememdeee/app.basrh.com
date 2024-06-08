def main_function(links, csv_file_input, useOptionSelected):
    import requests
    from bs4 import BeautifulSoup
    import csv
    import os
    from datetime import datetime
    from werkzeug.utils import secure_filename
    import validators

    def scrapUrl(url):
        response = requests.get(url)
        if response.status_code == 200:
            # Parse the HTML content using BeautifulSoup
            soup = BeautifulSoup(response.content, 'html.parser')

            # Find the <body> tag and get all the classes inside it
            body_tag = soup.body
            if body_tag:
                body_classes = body_tag.get('class', [])

                # Check if there is at least the third class
                if len(body_classes) >= 3:
                    if body_classes[2] != "single-post":
                        # Return only the third class
                        return body_classes[2]
                    else:
                        # Return only the fourth  class
                        return body_classes[3]
                else:
                    return "There are less than three classes inside <body>."
            else:
                return "No <body> tag found on the page."
        else:
            return "Url not valid"

    linkSubmitted = []
    results = []
    fileName = ""
    newFileName = ""
    respond = {
        "links": "",
        "csv_filename": "",
        "use_option": "",
        "output": "",
        "download_link": "",
        "status": ""
    }

    if (useOptionSelected == "url"):
        # execute using links
        urls = links.split()
        for url in urls:
            if validators.url(url):
                linkSubmitted.append(url)
                result = scrapUrl(url)
                results.append(result)
            else:
                linkSubmitted.append(url)
                results.append("not valid")
    elif (useOptionSelected == "csv"):
        # execute using csv
        fileName = secure_filename(csv_file_input.filename)
        timestamp_str = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        newFileName = f'{fileName.split(".")[0]}_{timestamp_str}.csv'
        save_directory = os.path.join('input_csv', newFileName)
        result_directory = os.path.join('output_csv', newFileName)
        csv_file_input.save(save_directory)
        # process the csv and return the value
        with open(save_directory, 'r') as file:
            # Assuming the CSV file has a header called url
            reader = csv.DictReader(file)
            if 'url' in reader.fieldnames:
                urls = [row['url'] for row in reader]
                links = urls
            else:
                respond["status"] = "URL column not found."
                return respond
        with open(result_directory, 'w', newline='') as output_file:
            # Create a CSV writer
            csv_writer = csv.writer(output_file)

            # Write the header to the CSV file
            csv_writer.writerow(['URL', 'Result'])
            # Iterate over the list of URLs
            for url in urls:
                result = scrapUrl(url)
                results.append(result)
                csv_writer.writerow([url, result])
        # make ready download file - not yet

    respond = {
        "links": linkSubmitted,
        "csv_filename": fileName,
        "use_option": useOptionSelected,
        "output": results,
        "download_link": newFileName,
        "status": "200"
    }
    return respond