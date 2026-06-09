
import json

severity_keywords = {
    "outage": 5,
    "fraud": 5,
    "hacked": 5,
    "stolen": 5,
    "payment failed": 4,
    "unauthorized": 4,
    "error": 3,
    "failed": 3,
    "urgent": 2,
    "asap": 1,
    "login": 1,
    "password": 1
}


def extract_keywords(text):

    text = str(text).lower()

    found = []

    for word in severity_keywords:

        if word in text:
            found.append(word)

    return found


def confidence(row):

    delta = abs(row["Severity_Delta"])

    score = 70 + delta * 10

    if row["Keyword_Score"] >= 5:
        score += 5

    return min(score, 99)

def generate_analysis(row):

    keywords = ", ".join(
        row["Detected_Keywords"]
    )

    if row["Mismatch_Type"] == "Hidden Crisis":

        return (
            f"The presence of {keywords} together "
            f"with a semantic urgency score of "
            f"{row['Semantic_Score']:.2f} suggests "
            f"that this ticket deserves a higher "
            f"priority than the assigned "
            f"{row['Priority_Level']} level."
        )

    elif row["Mismatch_Type"] == "False Alarm":

        return (
            f"The ticket content and semantic "
            f"indicators do not strongly support "
            f"the assigned {row['Priority_Level']} "
            f"priority level."
        )

    else:

        return (
            "The inferred severity is consistent "
            "with the assigned priority."
        )

def generate_dossier(row, max_keyword_score=10):

    detected_keywords = extract_keywords(
        row["Combined_Text"]
    )

    dossier = {

        "ticket_id":
        row["Ticket_ID"],

        "assigned_priority":
        row["Priority_Level"],

        "inferred_severity":
        row["Inferred_Severity"],

        "mismatch_type":
        row["Mismatch_Type"],

        "severity_delta":
        int(row["Severity_Delta"]),

        "feature_evidence": [

            {
                "signal": "keyword",

                "value":
                detected_keywords,

                "weight":
                round(
                    row["Keyword_Score"] /
                    max_keyword_score,
                    2
                )
            },

            {
                "signal":
                "resolution_time",

                "value":
                int(
                    row[
                        "Resolution_Time_Hours"
                    ]
                ),

                "interpretation":

                (
                    "Fast resolution suggests operational urgency"

                    if row[
                        "Resolution_Time_Hours"
                    ] <= 12

                    else

                    "Normal resolution window"
                ),

                "weight":

                round(
                    (
                        3
                        if row["Resolution_Time_Hours"] <= 12
                        else 2
                        if row["Resolution_Time_Hours"] <= 48
                        else 1
                    ) / 3,
                    2
                )
            },

            {
                "signal":
                "semantic_score",

                "value":
                round(
                    row[
                        "Semantic_Score"
                    ],
                    3
                ),

                "weight":
                round(
                    row[
                        "Semantic_Score"
                    ],
                    2
                )
            }

        ],

        "constraint_analysis":
        "",

        "confidence":
        str(
            confidence(row)
        ) + "%"
    }

   
    row["Detected_Keywords"] = detected_keywords

    dossier["constraint_analysis"] = (
        generate_analysis(row)
    )

    return dossier

def save_dossiers(
    dossiers,
    output_path
):

    with open(
        output_path,
        "w"
    ) as f:

        json.dump(
            dossiers,
            f,
            indent=4
        )

# Example Usage

if __name__ == "__main__":

    print(
        "Evidence Dossier Generator Loaded Successfully."
    )