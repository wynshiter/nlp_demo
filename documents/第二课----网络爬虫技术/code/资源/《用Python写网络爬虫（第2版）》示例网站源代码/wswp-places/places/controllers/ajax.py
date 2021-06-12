import re
import math


def search():
    """Results of AJAX search
    """
    records = []
    num_pages = 0
    error = ''
    search_term = request.vars.search_term
    if search_term:
        try:
            page = int(request.vars.page or 0)
            page_size = int(request.vars.page_size) or 10
        except (ValueError, TypeError):
            # passed arguments are invalid
            error = 'Invalid parameters'
        else:
            try:
                # 'like' not supported on GAE so manually compare strings
                records = [dict(country_or_district=record.country_or_district, id=record.id, pretty_link=record.pretty_link) for record in places.search() if re.compile(search_term, flags=re.IGNORECASE).search(record.country_or_district)]
            except re.error:
                error = 'Invalid search term'
            else:
                num_pages = int(math.ceil(len(records) / float(page_size)))
            records = records[page * page_size:(page + 1) * page_size]
    return dict(records=records, num_pages=num_pages, error=error)

