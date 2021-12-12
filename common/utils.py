import json


def parse_req(req_body):
    return json.loads(req_body)



def pagination(limit, page, resource_count, page_count, skip_val):
    if page:
        if not limit:
            limit = 10
        if resource_count > limit:
            page_count = int(resource_count / limit)
            if resource_count % limit:
                page_count += 1
        if page > page_count:
            raise Exception("Invalid page number")
        skip_val = ( page - 1 ) * limit
        if page_count == page:
            limit = resource_count - ( page - 1 ) * limit
            if limit == 0:
                limit = 1
    return skip_val, limit, page_count