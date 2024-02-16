# Forfeiture Manager

## Overview
Forfeiture-Manager is a sophisticated data scraping and management tool designed to streamline the process of identifying and acting on forfeiture cases listed on forfeiture.gov. By automating the extraction and parsing of case information from agency-specific PDFs, this application serves as an invaluable resource for legal professionals. It not only simplifies the search for relevant cases by state, city, person, and case ID but also integrates with WhitePages for person lookup and PostGrid for direct mail sending capabilities, offering a comprehensive solution for legal outreach.


## Features
**Automated Data Scraping:** Utilizes a Python script to scrape and parse forfeiture case data from government PDFs, storing this information in an accessible format.

**Advanced Search Functionality:** Offers an express.js web interface that allows users to search for cases based on various criteria including agency, case ID, name, and location.

**Direct Outreach Tools:** Integrates with WhitePages for accurate person lookup and PostGrid for the automated sending of letters to individuals involved in specific cases, facilitating direct legal assistance.

**Comprehensive Case Management:** Enables lawyers to efficiently manage case information, upload letters, and streamline the process of offering their services to potential clients.


## Usage
**Searching for Cases:** Access the web interface to search for forfeiture cases by various criteria. The search functionality is accessible through specific routes like /search.

**Uploading Letters:** Once a case of interest is found, legal professionals can upload a letter directly through the web interface, which can then be sent to the case's associated individual via PostGrid.

**Person Lookup:** Utilize the integrated WhitePages API for detailed lookups on individuals associated with specific cases.
