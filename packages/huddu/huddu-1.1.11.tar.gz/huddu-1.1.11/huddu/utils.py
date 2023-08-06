def get_headers_from_one_string_token(one_string_token):
    key_value_pairs = one_string_token.split(",")

    headers = {}
    for i in key_value_pairs:
        headers[i.split("=")[0]] = i.split("=")[1]

    return headers
