import requests
from bs4 import BeautifulSoup 

# TO-DO: add readme file

def fetch_and_print_from_doc(doc_url):
    """
    Fetches coordinates from a Google Doc URL and prints the resulting ASCII art.
    
    Args:
        doc_url (str): URL of the published Google Doc containing coordinate data
    """
    try:
        # Extract document ID from URL
        if '/pub' not in doc_url:
            raise ValueError("URL must be a published Google Doc (ending in /pub)")
        
        # Add headers to request text format
        response = requests.get(
            doc_url, 
            headers={'Accept': 'text/plain'},
            timeout=10  # Add timeout for safety
        )
        response.raise_for_status()

        soup = BeautifulSoup(response.text, 'html.parser')
        table = soup.find('table')

        if not table:
            raise ValueError("No data table found in document")

        content = table.find_all('tr')

        # so we have x, y, char as opposed to x, char, y
        coordinates = [(int(cell[0].get_text().strip()),
                       int(cell[2].get_text().strip()),
                       cell[1].get_text().strip())
                    for cell in [row.find_all('td') for row in content[1:]]]

        print_coordinates(coordinates)

    except Exception as e:
        print(f"Error processing document: {str(e)}")


def print_coordinates(coordinates):
    """
    Prints ASCII art from a list of coordinates.
    
    Args:
        coordinates (list): List of tuples (x, y, char) representing points to plot
    """
    if not coordinates:
        print("No coordinates to display")
        return

    max_x = max(coord[0] for coord in coordinates) + 1
    max_y = max(coord[1] for coord in coordinates) + 1

    grid = [[' ' for _ in range(max_x)] for _ in range(max_y)]

    for x, y, char in coordinates:
        grid[y][x] = char
    
    grid.reverse()

    for row in grid:
        print("".join(row))

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