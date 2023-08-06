""" 
This file takes the output of the rules-script, transforms it to human readbale format and applies scoring on the severity of the found PII. 
"""

import pandas as pd
import warnings

def calculate_severity(
    resultdict: dict,
    scores: dict = {
        "bsn": 50,
        "iban": 20,
        "email": 1,
        "telnr": 10,
        "zip": 5,
        "address": 5,
        "cv": 30,
        "credentials": 5,
        "creditcard": 20,
        "passport": 50,
    },
) -> pd.DataFrame:
    """
    This is a function to calculate the severity of PII violations given the rules output. Each PII type is multiplied by a score. Score are summed at document level to reflect the severity of the violations found.

    Default scores are
    bsn: 50, discovery of Dutch Social Security Number
    iban: 20, international bank account number
    email: 1, email address
    telnr: 10, national or international phone number
    zip: 5, Dutch zipcode
    address: 5, address
    cv: 30, resume keywords detected
    credentials: 5, credential keywords detected
    passport: 50, Dutch password number

    Args:
        input (pd.DataFrame): it takes a Pandas dataframe as input containing boolean values in the columns for each PII type, the output of the function 'result_to_boolean_dataframe'
        scores (dict): the severtity scores for each PII type

    Returns:
        pd.DataFrame: when PII type has been detected a score is returned indicating the severity
    """
    resultdf = pd.DataFrame.from_dict(resultdict, orient="index")

    df_not_processed = resultdf[~resultdf.content_processed]
    resultdf = resultdf[resultdf.content_processed]

    # infer the datatypes of the columns where there are results
    resultdf = resultdf.infer_objects()

    if len(resultdf.index) > 0:
        for col in list(scores.keys()):
            if resultdf[col].dtype == "bool":
                resultdf[col + "_severity"] = resultdf[col] * scores[col]
            else:
                # assuming all others are lists
                resultdf[col + "_severity"] = resultdf[col].apply(len)
                resultdf[col + "_severity"].values[resultdf[col + "_severity"] > 1] = 1
                resultdf[col + "_severity"] = resultdf[col + "_severity"] * scores[col]

        score_cols = [col + "_severity" for col in scores.keys()]

        resultdf["total"] = resultdf[score_cols].sum(axis=1).astype(int)
        resultdf = resultdf.sort_values("total", ascending=False)
    else:
        warnings.warn("None of the files are processed, no risk score can be calculated")

    return resultdf, df_not_processed
