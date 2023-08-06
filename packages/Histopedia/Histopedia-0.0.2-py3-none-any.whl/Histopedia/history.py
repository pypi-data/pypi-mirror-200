import datetime
import difflib
events = [("Signing of the Magna Carta", 1215),
          ("Columbus' voyage to America", 1492),
          ("The French Revolution", 1789),
          ("The American Revolution", 1775),
          ("The Battle of Waterloo", 1815),
          ("The invention of the telephone", 1876),
          ("The publication of 'On the Origin of Species'", 1859),
          ("The Wright Brothers' first flight", 1903),
          ("The sinking of the Titanic", 1912),
          ("The outbreak of World War I", 1914),
          ("The Russian Revolution", 1917),
          ("The Wall Street Crash", 1929),
          ("The bombing of Pearl Harbor", 1941),
          ("D-Day", 1944),
          ("The dropping of the atomic bomb on Hiroshima", 1945),
          ("The founding of the United Nations", 1945),
          ("The Indian Independence", 1947),
          ("The assassination of JFK", 1963),
          ("The first moon landing", 1969),
          ("The fall of the Berlin Wall", 1989),
          ("The Gulf War", 1990),
          ("The election of Nelson Mandela as President of South Africa", 1994),
          ("The September 11 attacks", 2001),
          ("The election of Barack Obama as President of the United States", 2008),
          ("The Arab Spring", 2011),
          ("The death of Nelson Mandela", 2013),
          ("The election of Donald Trump as President of the United States", 2016),
          ("The COVID-19 pandemic", 2020),
          ("The storming of the US Capitol", 2021),
          ("The inauguration of Joe Biden as President of the United States", 2021),
          ("Construction of the Great Wall of China", -700),
          ("Reign of Julius Caesar", -49),
          ("Eruption of Mount Vesuvius and destruction of Pompeii", 79)]


def proximate(year):
    # Check if year is within a valid range
    if year < -5000 or year > datetime.datetime.now().year:
        return "Unable to find any events for that year."

    # Calculate the absolute difference between the input year and each event year
    differences = []
    for event in events:
        event_year = event[1]
        difference = abs(year - event_year)
        differences.append(difference)

    # Find events within a 2 year range
    sorted_events = []
    for diff, event in sorted(zip(differences, events)):
        if diff <= 2:
            sorted_events.append(event)
        if len(sorted_events) == 5:
            break

    date_dict = {}
    for d, y in sorted_events:
        date_dict[y] = d

    return date_dict


def addEvent(dscrp, yr):
    events.append((dscrp, yr))
    return f"event ({dscrp}) added for year {yr}"


def exact(year):
    # Check if year is within a valid range
    if year < -5000 or year > datetime.datetime.now().year:
        return "Unable to find any events for that year."
    else:
        dscrp = []
        for a, b in events:
            if year == b:
                dscrp.append((a, b))
            else:
                continue
    if dscrp:
        return dscrp
    else:
        return "Unable to find any events for that year. Please try again with a different request"


inventions = [
    ("Wheel", -3500),
    ("Writing System", -3200),
    ("Plow", -3000),
    ("Sailing Ship", -3000),
    ("Bronze", -2800),
    ("Iron", -1200),
    ("Paper", 105),
    ("Compass", 206),
    ("Printing Press", 1440),
    ("Eyeglasses", 1286),
    ("Telescope", 1608),
    ("Microscope", 1595),
    ("Steam Engine", 1712),
    ("Lightning Rod", 1752),
    ("Electricity", 1752),
    ("Cotton Gin", 1793),
    ("Steamboat", 1807),
    ("Railroad", 1814),
    ("Reaper", 1831),
    ("Sewing Machine", 1846),
    ("Telegraph", 1837),
    ("Photography", 1839),
    ("Anesthesia", 1846),
    ("Typewriter", 1867),
    ("Telephone", 1876),
    ("Light Bulb", 1879),
    ("Automobile", 1885),
    ("Radio", 1895),
    ("X-Ray", 1895),
    ("Airplane", 1903),
    ("Assembly Line", 1913),
    ("Tank", 1915),
    ("Refrigerator", 1916),
    ("Television", 1925),
    ("Penicillin", 1928),
    ("Jet Engine", 1930),
    ("Photocopier", 1938),
    ("Nylon", 1938),
    ("Atomic Bomb", 1945),
    ("Transistor", 1947),
    ("Computer", 1948),
    ("Pacemaker", 1950),
    ("Color Television", 1951),
    ("Polio Vaccine", 1952),
    ("Credit Card", 1958),
    ("Laser", 1960),
    ("Bubble Wrap", 1960),
    ("Integrated Circuit", 1961),
    ("Video Cassette Recorder", 1963),
    ("Computer Mouse", 1964),
    ("ATM", 1967),
    ("Email", 1971),
    ("Floppy Disk", 1971),
    ("Ethernet", 1973),
    ("Cell Phone", 1973),
    ("Personal Computer", 1975),
    ("Apple Computer", 1976),
    ("Inkjet Printer", 1976),
    ("Post-It Notes", 1977),
    ("Walkman", 1979),
    ("Space Shuttle", 1981),
    ("Compact Disc", 1982),
    ("Apple Macintosh", 1984),
    ("Disposable Camera", 1986),
    ("World Wide Web", 1989),
    ("Digital Camera", 1990),
    ("Smartphone", 1992),
    ("DVD", 1995),
    ("MP3 Player", 1998),
    ("Google", 1998),
    ("USB Flash Drive", 1999),
    ("Bluetooth", 1999),
    ("iPod", 2001),
    ("Facebook", 2004),
    ("YouTube", 2005),
    ("Twitter", 2006),
    ("Kindle", 2007),
    ("Tesla Roadster", 2008),
    ("iPad", 2010),
    ("Bitcoin", 2009),
    ("Airbnb", 2008),
    ("Uber", 2009)
]


def traceIno(trace_year):
    inos = []
    for i, d in inventions:
        if d == trace_year:
            inos.append(i)
        else:
            continue
    if inos:
        return inos
    else:
        return "innovation not found in our database"


discoveries = [("Gravity", 1687), ("Cell Theory", 1839), ("Electromagnetism", 1820), ("Atomic Theory", 1803),
               ("Natural Selection", 1859), ("Periodic Table", 1869), ("DNA Structure", 1953),
               ("Special Relativity", 1905), ("General Relativity", 1915), ("Quantum Mechanics", 1925),
               ("Plate Tectonics", 1967), ("Big Bang Theory", 1927), ("Theory of Evolution", 1859),
               ("Theory of Plate Tectonics", 1960), ("Theory of Relativity", 1905),
               ("Theory of Quantum Mechanics", 1925), ("Theory of Gravitation", 1687),
               ("Theory of Electromagnetism", 1820), ("Theory of General Relativity", 1915),
               ("Theory of Special Relativity", 1905), ("Theory of Natural Selection", 1859),
               ("Theory of Atomic Structure", 1803), ("Structure of DNA", 1953), ("Discovery of Radioactivity", 1896),
               ("Discovery of X-rays", 1895), ("Discovery of Penicillin", 1928), ("Discovery of Neutrons", 1932),
               ("Discovery of Electrons", 1897), ("Discovery of the Nucleus", 1911),
               ("Discovery of Cosmic Microwave Background Radiation", 1964), ("Discovery of the Higgs Boson", 2012),
               ("Discovery of Dark Matter", 1933), ("Discovery of the Double Helix Structure of DNA", 1953),
               ("Discovery of the Structure of Benzene", 1865), ("Discovery of the Structure of Proteins", 1951),
               ("Discovery of the Structure of Viruses", 1935), ("Discovery of the Structure of Enzymes", 1926),
               ("Discovery of Neutron Stars", 1967), ("Discovery of Pulsars", 1967), ("Discovery of Quasars", 1963),
               ("Discovery of Black Holes", 1916), ("Discovery of the Hubble Constant", 1929),
               ("Discovery of the First Exoplanet", 1995),
               ("Discovery of the Cosmic Microwave Background Radiation", 1964), ("Discovery of Dark Energy", 1998),
               ("Discovery of the Human Genome", 2001), ("Discovery of the Structure of Ribosomes", 2000),
               ("Discovery of the Structure of the Zika Virus", 2016), ("Discovery of Gravitational Waves", 2015),
               ("Discovery of the CRISPR-Cas9 Gene Editing System", 2012), ("Discovery of the Ice Age", 1837),
               ("Discovery of the First Dinosaur Fossils", 1824), ("Discovery of the First Human Fossil", 1856)]


def discov(yr):
    discovs = []
    for d, y in discoveries:
        if y == yr:
            discovs.append(d)
        else:
            continue
    if discovs:
        return discovs
    else:
        closest = min(discoveries, key=lambda x: abs(x[1] - yr))
        closest_discovery = closest[0]
        closest_year = closest[1]
        return f"Discovery not found for {yr}. Did you mean {closest_year}: {closest_discovery}?"


def push(disc, yr):
    discoveries.append((disc, yr))
    return "Appended successfully"


def getDisc():
    return discoveries  # this is for user usage if they want to make something


def pushIno(ino, yr):
    inventions.append((ino, yr))


def getInos():
    return inventions


def getEvents():
    return events


people = {
    'Aristotle': ('384 BC', '322 BC'),
    'Leonardo da Vinci': ('1452', '1519'),
    'William Shakespeare': ('1564', '1616'),
    'Galileo Galilei': ('1564', '1642'),
    'Isaac Newton': ('1643', '1727'),
    'Charles Darwin': ('1809', '1882'),
    'Albert Einstein': ('1879', '1955'),
    'Mahatma Gandhi': ('1869', '1948'),
    'Winston Churchill': ('1874', '1965'),
    'Martin Luther King Jr.': ('1929', '1968'),
    'Nelson Mandela': ('1918', '2013'),
    'Mother Teresa': ('1910', '1997'),
    'Alexander the Great': ('356 BC', '323 BC'),
    'Julius Caesar': ('100 BC', '44 BC'),
    'Augustus': ('63 BC', '14 AD'),
    'Charlemagne': ('747 AD', '814 AD'),
    'Genghis Khan': ('1162', '1227'),
    'Christopher Columbus': ('1451', '1506'),
    'Leon Trotsky': ('1879', '1940'),
    'Vladimir Lenin': ('1870', '1924'),
    'Mao Zedong': ('1893', '1976'),
    'Joseph Stalin': ('1878', '1953'),
    'Wolfgang Amadeus Mozart': ('1756', '1791'),
    'Ludwig van Beethoven': ('1770', '1827'),
    'Johann Sebastian Bach': ('1685', '1750'),
    'Pablo Picasso': ('1881', '1973'),
    'Vincent van Gogh': ('1853', '1890'),
    'Rembrandt van Rijn': ('1606', '1669'),
    'Michelangelo': ('1475', '1564'),
    'Leonardo Fibonacci': ('1175', '1250'),
    'Archimedes': ('287 BC', '212 BC'),
    'Euclid': ('325 BC', '265 BC'),
    'Pythagoras': ('570 BC', '495 BC'),
    'Plato': ('427 BC', '347 BC'),
    'Socrates': ('469 BC', '399 BC'),
    'Confucius': ('551 BC', '479 BC'),
    'Buddha': ('563 BC', '483 BC'),
    'Jesus Christ': ('4 BC', '30 AD'),
    'Muhammad': ('570 AD', '632 AD'),
    'William the Conqueror': ('1028', '1087'),
    'Queen Elizabeth I': ('1533', '1603'),
    'Catherine the Great': ('1729', '1796'),
    'Marie Curie': ('1867', '1934'),
    'Florence Nightingale': ('1820', '1910'),
    'Jane Austen': ('1775', '1817'),
    'Emily Dickinson': ('1830', '1886'),
    'Ralph Waldo Emerson': ('1803', '1882'),
    'F. Scott Fitzgerald': ('1896', '1940'),
    'Ernest Hemingway': ('1899', '1961'),
    'Henry David Thoreau': ('1817', '1862'),
    'Bhagat Singh': ('1907', '1931'),
    'George Washington': ('1732', '1799'),
    'Benjamin Franklin': ('1706', '1790'),
    'Alexander Hamilton': ('1755', '1804'),
    'James Madison': ('1751', '1836'),
    'George Clymer': ('1739', '1813'),
    'Benjamin Rush': ('1746', '1813'),
    'George Read': ('1733', '1798'),
    'Robert Morris': ('1734', '1806'),
    'William Blount': ('1749', '1800'),
    'Gouverneur Morris': ('1752', '1816'),
    'John Dickinson': ('1732', '1808'),
    'Daniel Carroll': ('1730', '1796'),
    'William Livingston': ('1723', '1790'),
    'William Paterson': ('1745', '1806'),
    'Hugh Williamson': ('1735', '1819'),
    'Thomas Fitzsimons': ('1741', '1811'),
    'Richard Bassett': ('1745', '1815'),
    'Jacob Broom': ('1752', '1810'),
    'Abraham Baldwin': ('1754', '1807'),
    'William Few': ('1748', '1828'),
    'Jonathan Dayton': ('1760', '1824'),
    'Nicholas Gilman': ('1755', '1814'),
    'William Houstoun': ('1755', '1813'),
    'Alexander Martin': ('1740', '1807'),
    'Pierce Butler': ('1744', '1822'),
    'John Blair': ('1732', '1800'),
    'John Rutledge': ('1739', '1800'),
    'Charles Pinckney': ('1757', '1824'),
    'Charles Cotesworth Pinckney': ('1746', '1825'),
    'William Richardson Davie': ('1756', '1820'),
    'Oliver Ellsworth': ('1745', '1807'),
    'Elbridge Gerry': ('1744', '1814'),
    'Nathaniel Gorham': ('1738', '1796'),
    'Roger Sherman': ('1721', '1793'),
    'Robert Yates': ('1738', '1801'),
    'John Lansing': ('1754', '1829'),
    'Luther Martin': ('1748', '1826'),
    'John Francis Mercer': ('1759', '1821'),
    'James McHenry': ('1753', '1816'),
    'William Paca': ('1740', '1799'),
    'George Wythe': ('1726', '1806'),
    'Richard Henry Lee': ('1732', '1794'),
    'Thomas Jefferson': ('1743', '1826'),
    'Benjamin Harrison V': ('1726', '1791'),
    'Edmund Randolph': ('1753', '1813'),
    'George Mason': ('1725', '1792'),
    'James Wilson': ('1742', '1798'),
    'John Blair Jr.': ('1732', '1800')
}


def born(name):
    if name in people:
        return people[name][0]
    else:
        matches = difflib.get_close_matches(name, people.keys())
        if matches:
            return f"No matching name for '{name}', did you mean '{matches[0]}'"
        else:
            return f"No matching name for {name}"


def died(name):
    if name in people:
        return people[name][1]
    else:
        matches = difflib.get_close_matches(name, people.keys())
        if matches:
            return f"No matching name for '{name}', did you mean '{matches[0]}'"
        else:
            return f"No matching name for {name}"


prehistoric_animals = {
    "trilobite": "Cambrian",
    "ammonite": "Devonian to Cretaceous",
    "eurypterid": "Ordovician to Permian",
    "dimetrodon": "Permian",
    "plesiosaur": "Jurassic to Cretaceous",
    "ichthyosaur": "Triassic to Cretaceous",
    "stegosaurus": "Jurassic",
    "brachiosaurus": "Jurassic to Cretaceous",
    "tyrannosaurus": "Cretaceous",
    "velociraptor": "Cretaceous",
    "diplodocus": "Jurassic",
    "triceratops": "Cretaceous",
    "ankylosaurus": "Cretaceous",
    "parasaurolophus": "Cretaceous",
    "apatosaurus": "Jurassic",
    "archaeopteryx": "Jurassic",
    "spinosaurus": "Cretaceous",
    "pteranodon": "Cretaceous",
    "deinonychus": "Cretaceous",
    "allosaurus": "Jurassic",
    "iguanodon": "Jurassic to Cretaceous",
    "styracosaurus": "Cretaceous",
    "edmontosaurus": "Cretaceous",
    "gallimimus": "Cretaceous",
    "ornithomimus": "Cretaceous",
    "therizinosaurus": "Cretaceous",
    "troodon": "Cretaceous",
    "dromaeosaurus": "Cretaceous",
    "ceratosaurus": "Jurassic to Cretaceous",
    "oviraptor": "Cretaceous",
    "sinosauropteryx": "Jurassic",
    "microraptor": "Jurassic to Cretaceous",
    "muttaburrasaurus": "Cretaceous",
    "paralititan": "Cretaceous",
    "saurolophus": "Cretaceous",
    "theropoda": "Triassic to Cretaceous",
    "sauropoda": "Jurassic to Cretaceous",
    "ornithischia": "Triassic to Cretaceous",
    "ankylosauria": "Jurassic to Cretaceous",
    "stegosauria": "Jurassic",
    "ceratopsia": "Cretaceous",
    "hadrosauridae": "Cretaceous",
    "tyrannosauridae": "Cretaceous",
    "dromaeosauridae": "Cretaceous",
    "megalodon": "Miocene to Pliocene",
    "dunkleosteus": "Devonian",
    "liopleurodon": "Jurassic",
    "xiphactinus": "Cretaceous",
    "ichthyosaurus": "Triassic to Jurassic",
    "dolichorhynchops": "Cretaceous",
    "leedsichthys": "Jurassic",
    "megalosaurus": "Jurassic",
    "helicoprion": "Permian to Triassic",
    "shonisaurus": "Triassic",
    "temnodontosaurus": "Jurassic",
    "elasmosaurus": "Cretaceous",
    "tylosaurus": "Cretaceous",
}


def period(anml):
    return prehistoric_animals.get(anml.lower(), f"'{anml.lower()}' not found")
