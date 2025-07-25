import requests
from bs4 import BeautifulSoup

urls = [
    "https://www.algerian-human.org",
    "https://www.algerian-human.org/about",
    "https://www.algerian-human.org/projects/Algeria/medical",
    "https://www.algerian-human.org/projects/Algeria/families",
    "https://www.algerian-human.org/projects/Algeria/students",
    "https://www.algerian-human.org/projects/Algeria/smile",
    "https://www.algerian-human.org/projects/Algeria/zakat",
    "https://www.algerian-human.org/projects/Algeria/debt",
    "https://www.algerian-human.org/projects/Algeria/equipment",
    "https://www.algerian-human.org/projects/Africa/water",
    "https://www.algerian-human.org/projects/Africa/mosques",
    "https://www.algerian-human.org/projects/Africa/food",
    "https://www.algerian-human.org/projects/Africa/seasonal",
    "https://www.algerian-human.org/projects/Africa/Aladhahi",
    "https://www.algerian-human.org/projects/ar/wells",
    "https://www.algerian-human.org/projects/ar/mosques",
    "https://www.algerian-human.org/projects/ar/relief"
    "https://www.algerian-human.org/donate",
    "https://www.algerian-human.org/contact",
]

for url in urls:
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    text = soup.get_text(separator="\n", strip=True)
    route = url.strip("/").split("/")[-1]
    fileName = "../dataset/association.txt"
    print(f"=== {url} ===")
    with open(fileName, "a", encoding="utf-8") as f:
        f.write(text)
    print(f"Saved {url} -> {fileName}")
    print("\n" + "=" * 50 + "\n")
