import requests
import pdfplumber
import os
import io
import logging
import json

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

URLS = {
    "ATF": "https://www.forfeiture.gov/pdf/ATF/OfficialNotification.pdf",
    "DEA": "https://www.forfeiture.gov/pdf/DEA/OfficialNotification.pdf",
    "FBI": "https://www.forfeiture.gov/pdf/FBI/OfficialNotification.pdf",
    "IRS": "https://www.forfeiture.gov/pdf/IRS/OfficialNotification.pdf"
}

STATES = [
    "ALABAMA", "ALASKA", "ARIZONA", "ARKANSAS", "CALIFORNIA", 
    "COLORADO", "CONNECTICUT", "DELAWARE", "FLORIDA", "GEORGIA", 
    "HAWAII", "IDAHO", "ILLINOIS", "INDIANA", "IOWA", 
    "KANSAS", "KENTUCKY", "LOUISIANA", "MAINE", "MARYLAND", 
    "MASSACHUSETTS", "MICHIGAN", "MINNESOTA", "MISSISSIPPI", "MISSOURI", 
    "MONTANA", "NEBRASKA", "NEVADA", "NEW HAMPSHIRE", "NEW JERSEY", 
    "NEW MEXICO", "NEW YORK", "NORTH CAROLINA", "NORTH DAKOTA", "OHIO", 
    "OKLAHOMA", "OREGON", "PENNSYLVANIA", "RHODE ISLAND", "SOUTH CAROLINA", 
    "SOUTH DAKOTA", "TENNESSEE", "TEXAS", "UTAH", "VERMONT", 
    "VIRGINIA", "WASHINGTON", "WEST VIRGINIA", "WISCONSIN", "WYOMING"
]


# Base directory for saving files
BASE_DIR = "agencyFiles"

# Flag to decide whether to keep PDF files
KEEP_PDF = False  # Set to True if you want to keep the PDFs


def checkDirectory(path):
    if not os.path.exists(path):
        os.makedirs(path)


def get_filename(agency, extension):
    return os.path.join(BASE_DIR, f"{agency}{extension}")


def updatePDF(agency, session):
    pdf_filename = get_filename(agency, ".pdf")
    txt_filename = get_filename(agency, ".txt")

    try:
        response = session.get(URLS[agency], verify=False)
        response.raise_for_status()

        with pdfplumber.open(io.BytesIO(response.content)) as pdf:
            new_text = ''.join(page.extract_text() for page in pdf.pages if page.extract_text())

        if os.path.exists(txt_filename):
            with open(txt_filename, "r") as f:
                old_text = f.read()

            if old_text != new_text:
                with open(txt_filename, "w") as f:
                    f.write(new_text)
                logging.info(f"{agency} DATA UPDATED")
            else:
                logging.info(f"{agency} DATA NOT CHANGED")
        else:
            with open(txt_filename, "w") as f:
                f.write(new_text)
            logging.info(f"{agency} DATA CREATED")

        if KEEP_PDF:
            with open(pdf_filename, "wb") as f:
                f.write(response.content)

    except requests.RequestException as e:
        logging.error(f"Error fetching data for {agency}: {e}")
    except Exception as e:
        logging.error(f"Unexpected error occurred: {e}")


def updateAllFiles():
    with requests.Session() as session:
        for agency in URLS.keys():
            updatePDF(agency, session)


def validate_and_sanitize_data(field, field_type):
    if field_type == "name" and len(field) > 100:  # Example length limit for name
        return ""
    if field_type == "location" and "," not in field:  # Location should contain a comma
        return ""
    if field_type == "date" and not field.isupper():  # Date should be uppercase
        return ""
    if field_type == "item":
        return ""
    if field_type == "value":
        return ""
        
    return field

def extractATFData(case):
    nameStart = case.find(" from ") + len(" from ")
    nameEnd = case.find(" in", nameStart)
    name = case[nameStart:nameEnd].strip()
    # name = validate_and_sanitize_data(case[nameStart:nameEnd].strip(), "name")

    locationStart = case.find(" in ") + len(" in ")
    locationEnd = case.find(" for", locationStart)
    location = case[locationStart:locationEnd].strip()

    search_str = "seized by the ATF on "
    dateStart = case.find(search_str) + len(search_str)
    dateEnd = case.find(" from", dateStart)
    date = case[dateStart:dateEnd].strip()


    if "U.S. Currency" in case:
        item = "U.S. Currency"
    else:
        item_start = case.find(":") + 2
        item_end = case.find(", valued at")
        item = case[item_start:item_end].strip()

    valueStart = case.find("$")
    valueEnd = valueStart
    value = ''

    if valueStart != -1:
        while valueEnd < len(case) - 2:
            if case[valueEnd] == '.' and case[valueEnd + 1].isdigit() and case[valueEnd + 2].isdigit():
                break
            valueEnd += 1

        valueEnd += 3
        value = case[valueStart:valueEnd]

    return name, location, date, item, value


def extractDEAData(case):
    nameStart = case.find(" from ") + len(" from ")
    nameEnd = case.find(" in", nameStart)
    name = case[nameStart:nameEnd].strip()

    locationStart = case.find(" in ") + len(" in ")
    locationEnd = case.find(" for", locationStart)
    location = case[locationStart:locationEnd].strip()

    search_str = "seized by the DEA on "
    dateStart = case.find(search_str) + len(search_str)
    dateEnd = case.find(" from", dateStart)
    date = case[dateStart:dateEnd].strip()

    if "U.S. Currency" in case:
        item = "U.S. Currency"
    else:
        item_start = case.find(":") + 2
        item_end = case.find(", valued at")
        item = case[item_start:item_end].strip()
        # continue

    valueStart = case.find("$")
    valueEnd = valueStart

    if valueStart != -1:
        while valueEnd < len(case) - 2:
            if case[valueEnd] == '.' and case[valueEnd + 1].isdigit() and case[valueEnd + 2].isdigit():
                break
            valueEnd += 1

        valueEnd += 3
        value = case[valueStart:valueEnd]

    return name, location, date, item, value


def extractFBIData(case):
    nameStart = case.find(" from ") + len(" from ")
    nameEnd = case.find(" in", nameStart)
    name = case[nameStart:nameEnd].strip()

    locationStart = case.find(" in ") + len(" in ")
    locationEnd = case.find(" for", locationStart)
    location = case[locationStart:locationEnd].strip()

    search_str = "seized by the FBI on "
    dateStart = case.find(search_str) + len(search_str)
    dateEnd = case.find(" for", dateStart)
    date = case[dateStart:dateEnd].strip()

    if "U.S. Currency" in case:
        item = "U.S. Currency"
    else:
        item_start = case.find(":") + 2
        item_end = case.find(", valued at")
        item = case[item_start:item_end].strip()
        # continue

    valueStart = case.find("$")
    valueEnd = valueStart

    if valueStart != -1:
        while valueEnd < len(case) - 2:
            if case[valueEnd] == '.' and case[valueEnd + 1].isdigit() and case[valueEnd + 2].isdigit():
                break
            valueEnd += 1

        valueEnd += 3
        value = case[valueStart:valueEnd]

    return name, location, date, item, value


def extractIRSData(case):
    nameStart = case.find(" from ") + len(" from ")
    nameEnd = case.find(" in", nameStart)
    name = case[nameStart:nameEnd].strip()

    locationStart = case.find(" in ") + len(" in ")
    locationEnd = case.find(" for", locationStart)
    location = case[locationStart:locationEnd].strip()

    search_str = "seized by the FBI on "
    dateStart = case.find(search_str) + len(search_str)
    dateEnd = case.find(" for", dateStart)
    date = case[dateStart:dateEnd].strip()

    if "U.S. Currency" in case:
        item = "U.S. Currency"
    else:
        item_start = case.find(":") + 2
        item_end = case.find(", valued at")
        item = case[item_start:item_end].strip()
        # continue

    valueStart = case.find("$")
    valueEnd = valueStart

    if valueStart != -1:
        while valueEnd < len(case) - 2:
            if case[valueEnd] == '.' and case[valueEnd + 1].isdigit() and case[valueEnd + 2].isdigit():
                break
            valueEnd += 1

        valueEnd += 3
        value = case[valueStart:valueEnd]

    return name, location, date, item, value


def getCasesByState(state, agency):
    txt_filename = get_filename(agency, ".txt")
    
    with open(txt_filename, 'r') as file:
        lines = file.read().splitlines()

    # districtMap = {state: []}
    all_cases = []
    curr_case = []
    capture = False

    for line in lines:
        if "DISTRICT OF" in line:
            if state in line:
                capture = True
            else:
                capture = False

        elif capture and line.startswith("23-" + agency + "-"):  # Dynamic start pattern
            curr_case.append(line)

        elif capture and curr_case:
            curr_case[-1] += ' ' + line

            if "U.S.C." in line and any(char.isdigit() for char in line):
                caseID = curr_case[-1].split(':', 1)[0]

                if len(caseID) > 13:
                    continue

                extract_function_name = f'extract{agency}Data'
                if extract_function_name in globals():
                    extract_function = globals()[extract_function_name]
                    name, location, date, item, value = extract_function(curr_case[-1])
                else:
                    raise ValueError(f"No data extraction function found for agency: {agency}")

                case_entry = {
                    caseID: {
                        "name": name,
                        "location": location,
                        "date": date,
                        "items": item,
                        "value": value,
                        # "description": curr_case[-1],
                    }
                }
                # districtMap[state].append(case_entry)
                all_cases.append(case_entry)
                curr_case = []

    # return districtMap
    return all_cases


def updateDatabases():
    checkDirectory(BASE_DIR)
    
    for agency in URLS.keys():
        all_district_maps = {}

        for state in STATES:
            try:
                cases_for_state = getCasesByState(state, agency)
                all_district_maps[state] = cases_for_state
            except Exception as e:
                print(f"Error processing {state} for {agency}: {e}")

        # district_map = getCasesByState(state, agency)
        json_filename = os.path.join(BASE_DIR, f"{agency}.json")
        with open(json_filename, 'w') as json_file:
            json.dump(all_district_maps, json_file, indent=4)


if __name__ == '__main__':
    # updateAllFiles()
    updateDatabases()