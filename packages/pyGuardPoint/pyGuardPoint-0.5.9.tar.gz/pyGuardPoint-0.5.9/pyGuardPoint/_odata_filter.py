from datetime import datetime

from DateTime import DateTime

from .guardpoint_dataclasses import Area


def _compose_filter(search_words=None,
                    areas=None,
                    cardholder_type_name=None,
                    filter_expired=False,
                    earliest_last_pass=None):
    filter_phrases = []

    if earliest_last_pass:
        if isinstance(earliest_last_pass, datetime):
            last_pass_date = earliest_last_pass.strftime('%Y-%m-%dT%H:%M:%SZ')
            filter_phrases.append(f'(lastPassDate%20ge%20{last_pass_date})')

    # Filter out expired cardholders
    if filter_expired:
        # end_of_day = datetime.utcnow().strftime('%Y-%m-%dT23:59:59Z')
        start_of_day = datetime.utcnow().strftime('%Y-%m-%dT00:00:00Z')
        filter_phrases.append(f'(fromDateValid%20ge%20{start_of_day})')

    # Filter by Cardholder Type Name
    if cardholder_type_name:
        filter_phrases.append(f"(cardholderType/typeName%20eq%20'{cardholder_type_name}')")

    # Filter by Areas
    if areas:
        if isinstance(areas, Area):
            filter_phrases.append(f"(insideAreaUID%20eq%20{areas.uid})")
        if isinstance(areas, list):
            if len(areas) > 0 :
                area_phrases = []
                for area in areas:
                    if isinstance(area, Area):
                        area_phrases.append(f"(insideAreaUID%20eq%20{area.uid})")
                filter_phrases.append(f"({'%20or%20'.join(area_phrases)})")

    # Search filter
    if search_words:
        if isinstance(search_words, str):
            # Split 'search_words' by spaces, remove empty elements, ignore > 5 elements
            words = list(filter(None, search_words.split(" ")))[:5]
            fields = ["firstName", "lastName", "CardholderPersonalDetail/company", "CardholderPersonalDetail/email"]
            search_phrases = []
            for f in fields:
                for v in words:
                    search_phrases.append(f"contains({f},'{v}')")
            filter_phrases.append(f"({'%20or%20'.join(search_phrases)})")

    # compose filter string
    filter_str = ""
    if len(filter_phrases) > 0:
        filter_str += "$filter="
        filter_str += f"({'%20and%20'.join(filter_phrases)})"
        filter_str += "&"

    return filter_str


if __name__ == "__main__":
    area_list = []
    area_list.append(Area({'uid': '00000000-0000-0000-0000-100000000001', 'area': "Offsite"}))
    print(_compose_filter(search_words="John Owen",
                          areas=area_list,
                          cardholder_type_name="Visitor", filter_expired=True))
