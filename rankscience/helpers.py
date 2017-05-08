from collections import OrderedDict

def paginate(data, page=1, per=4, **extras):
    '''
    Slices list using multiple of the page limit. Additional
    keys from request are collected in extras

    Parameters:
    ----------
    data : List of OrderDict from query
    page : int with a default value of 1
    limit : length of the returned list

    Returns:
    -------
    page_list : list of OrderDict
    '''
    page = int(page)
    per = int (per)
    if page <= 0 or per < 0:
        abort(404, 'Use a valid page and limit')

    count = len(data)
    # Page limit exceeds number of returned objects
    if count < per:
        return data
    starting_index = per * (page - 1)
    ending_index = (page * per) - 1

    # End of page limit
    if ending_index >= (count - 1):
        return data[-(count % per):]
    return data[starting_index:ending_index + 1]


def construct_query(**kwargs):
    '''
    Constructs a SQL statement based on request

    Parameters:
    ----------
    request.args.to_dict() object

    Returns:
    -------
    SQL statement to be executed with cursor object
    '''

    base_query = """
                SELECT a.id, a.name, b.quantity, b.product_id as id, c.sku,
                c.description, b.id as active_shipment_count,
                a.international_transportation_mode,
                a.international_departure_date
                FROM shipments a
                INNER JOIN shipment_products b on b.shipment_id = a.id
                INNER JOIN products c on c.id = b.product_id
                """
    # Modify SQL statement as more items are passed
    parameterize = []
    # Construct WHERE statement
    where_statement = []
    where_statement.append("a.company_id=%s")
    parameterize.append(kwargs['company_id'])

    if 'international_transportation_mode' in kwargs.keys():
        where_statement.append("international_transportation_mode=%s")
        parameterize.append(kwargs['international_transportation_mode'])
    where_statement = "WHERE " + " AND ".join(where_statement)

    # Construct ORDER BY statement
    if {'sort','direction'} <= set(kwargs.keys()):
        # Without parametrize
        sort_statement = " ORDER BY " + kwargs['sort'] + \
            " " + kwargs['direction']
    else:
        sort_statement = ''
    return base_query + where_statement + sort_statement, tuple(parameterize)


def label_json(data, labels):
    '''
    Check if a record has a product and add additional products if
    id already exists.

    Parameters:
    ----------
    data : list of tuples from query
    labels : query column names

    Returns:
    -------
    List of records to be returned by jsonify
    '''
    objects = []

    # OrderedDictionary for debugging purposes
    for row in data:
        not_added = True
        d = OrderedDict(zip(labels[:2],row[:2]))
        # Check if id/name already exists
        # Iterate through object and append there otherwise add new
        for record in objects:
            if record['name'] == d['name']:
                record['products'].append(_product_json(row, labels))
                not_added = False
        # Create new product key
        if not_added:
            d['products'] = []
            d['products'].append(_product_json(row, labels))
            objects.append(d)

    return objects


def _product_json(row, labels):
    '''
    Assuming labels are in correct order, creates dict with quantity, id,
    sku, description, active_shipment_count as keys.

    Parameters:
    ----------
    row : a tuple in tuple of tuples from cur.fetchall()
    labels : set of defined labels from cur.description

    Returns:
    -------
    product : dict of product data
    '''
    return OrderedDict(zip(labels[2:7],row[2:7]))


