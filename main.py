import requests
from bs4 import BeautifulSoup 

def fetch_and_print_from_doc(doc_url):
    try:
        # Extract document ID from URL
        if '/pub' not in doc_url:
            print("Please provide a public document")
            return
        
        # Add headers to request text format
        headers = {
            'Accept': 'text/plain'
        }
        
        response = requests.get(doc_url, headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')
        content = soup.find('table').find_all('tr')

        coordinates = [(cell[0].get_text().strip(),
                       cell[1].get_text().strip(),
                       cell[2].get_text().strip())
                    for cell in [row.find_all('td') for row in content[1:]]]

        print(f"coordinates: ${coordinates}")

    except Exception as e:
        print(f"Error processing document: {str(e)}")

# Example usage with coordinates that form the letter 'F'
example_coords = [
    (0, 0, '█'), (1, 0, '█'), (2, 0, '█'),
    (0, 1, '█'),
    (0, 2, '█'), (1, 2, '█'),
    (0, 3, '█'),
    (0, 4, '█')
]

fetch_and_print_from_doc("https://docs.google.com/document/d/e/2PACX-1vQGUck9HIFCyezsrBSnmENk5ieJuYwpt7YHYEzeNJkIb9OSDdx-ov2nRNReKQyey-cwJOoEKUhLmN9z/pub")
# fetch_and_print_from_doc("https://docs.google.com/document/d/e/2PACX-1vRMx5YQlZNa3ra8dYYxmv-QIQ3YJe8tbI3kqcuC7lQiZm-CSEznKfN_HYNSpoXcZIV3Y_O3YoUB1ecq/pub")