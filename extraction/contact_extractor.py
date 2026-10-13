import re
from typing import Dict, List, Optional

class ContactExtractor:

    # email: 1. username: [A-Za-z0-9._%+-]+ 2. @ 3. domain name: [A-Za-z0-9.-]+ 4. \. 5. top-level domain [A-Za-z]{2,}
    EMAIL_REGEX = r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b"
    #phone: 1.Optional country code: (?:\+?\d{1,3}[-.\s]?)? 2.Optional area code: \(?\d{3}\)?
    # 3. Optional separator: [-.\s]? 4. First 3 digits: \d{3} 5.Optional separator: [-.\s]?
    #6. Final 4 digits: \d{4}
    PHONE_REGEX = r"\b(?:\+?\d{1,3}[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}\b"
    #linkedin: 1. Optional protocol: (?:https?:\/\/)? 2. Optional www subdomain: (?:www\.)?
    #3. Mandatory LinkedIn profile base path: linkedin\.com\/in\/ 4. Profile username/slug: [A-Za-z0-9_-]+
    #5. Optional trailing slash: \/?
    LINKEDIN_REGEX = r"\b(?:https?:\/\/)?(?:www\.)?linkedin\.com\/in\/[A-Za-z0-9_-]+\/?\b"

    @classmethod
    def extract_contacts(cls, text: str) -> Dict[str, Optional[str]]:
        #extracts first email, phone and linkedin found
        emails = re.findall(cls.EMAIL_REGEX, text)
        phones = re.findall(cls.PHONE_REGEX, text)
        linkedin = re.findall(cls.LINKEDIN_REGEX, text)

        return {
            "extracted_email": emails[0] if emails else None,
            "extracted_phone": phones[0] if phones else None,
            "extracted_linkedin": linkedin[0] if linkedin else None,
        }