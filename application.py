#!/usr/bin/env python
# -*- coding: utf-8 -*-

from rankscience import application, mysql
from flask import Flask, jsonify, request, abort, render_template
from flask_mysqldb import MySQL

from rankscience.helpers import construct_query, label_json, paginate


@application.route('/')
def index():
    return render_template('index.html')


@application.route('/api/v1/shipments', methods=['GET'])
def get_company():
    params = request.args.to_dict()

    # company_id is required
    if 'company_id' not in params.keys():
        resp = jsonify({'errors': ['company_id is required']})
        resp.status_code = 422
        return resp

    cur = mysql.connection.cursor()
    query, parameterized = construct_query(**params)
    print query
    cur.execute(query, parameterized)

    # Gets all column names of query
    col_names = [x[0] for x in cur.description]
    data = cur.fetchall()
    print data
    serialized_data = label_json(data, col_names)
    pdata = paginate(serialized_data, **params)
    return jsonify(records=pdata)


if __name__ == "__main__":
    application.run()


