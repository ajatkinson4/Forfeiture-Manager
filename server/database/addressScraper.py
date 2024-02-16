import requests
from bs4 import BeautifulSoup

# URL of the Whitepages website
url = "https://www.whitepages.com/"

# Create a session to maintain cookies and sessions
session = requests.Session()

# Send an initial GET request to the website
response = session.get(url)

print(response)

# # Check if the initial request was successful
# if response.status_code == 200:
#     # Parse the HTML content of the page
#     soup = BeautifulSoup(response.text, "html.parser")
    
#     # Find the input elements for name and location
#     name_input = soup.find("input", id="search-name")
#     location_input = soup.find("input", id="search-location")
    
#     # Modify the input values (replace with the values you want)
#     name_input["value"] = "John Doe"
#     location_input["value"] = "New York"
    
#     # Find and trigger the submit action button
#     submit_button = soup.find("button", id="wp-search")
    
#     if submit_button:
#         # Send a POST request with the modified form data
#         response = session.post(url, data={"search-name": name_input["value"], "search-location": location_input["value"]})
        
#         if response.status_code == 200:
#             # Parse the search results page
#             search_results_soup = BeautifulSoup(response.text, "html.parser")
            
#             # Find the element with class 'name-wrap'
#             name_wrap = search_results_soup.find("div", class_="name-wrap")
            
#             if name_wrap:
#                 # Check if the name matches (you may need to parse the name from the element)
#                 if "John Doe" in name_wrap.get_text():
#                     # Find and trigger the link with class 'serp-card'
#                     link = search_results_soup.find("a", class_="serp-card")
                    
#                     if link:
#                         # Send a GET request to the link
#                         link_url = link["href"]
#                         response = session.get(link_url)
                        
#                         if response.status_code == 200:
#                             # Parse the page with the address information
#                             address_soup = BeautifulSoup(response.text, "html.parser")
                            
#                             # Find and store the address information (you may need to adapt this part based on HTML structure)
#                             address = address_soup.find("a", class_="mb-1 raven--text td-n").text
#                             print("Address:", address)
#                         else:
#                             print("Failed to retrieve link:", link_url)
#                     else:
#                         print("Link not found")
#                 else:
#                     print("Name does not match")
#             else:
#                 print("Name element not found")
#         else:
#             print("Failed to submit the form")
#     else:
#         print("Submit button not found")
# else:
#     print("Failed to access the website")

# Close the session
session.close()
