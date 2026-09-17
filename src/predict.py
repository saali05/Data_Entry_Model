import json
import spacy

from validate import normalize_data
from database import create_table, insert_transaction


MODEL_PATH = "models/whatsapp_ner_v10"


def extract_financial_data(text):
    """
    Run the trained NER model and extract financial entities.
    """

    nlp = spacy.load(MODEL_PATH)

    doc = nlp(text)

    result = {
        "NAME": [],
        "ACCOUNT_NUMBER": [],
        "IFSC_CODE": [],
        "AMOUNT": []
    }

    for ent in doc.ents:
        if ent.label_ in result:
            result[ent.label_].append(ent.text)

    return result


def process_message(text):
    """
    Complete processing pipeline:

    Message
       ↓
    ML extraction
       ↓
    Validation
       ↓
    Normalization
       ↓
    Database
    """

    extracted_data = extract_financial_data(text)

    normalized_data = normalize_data(extracted_data)

    if normalized_data["is_valid"]:

        transaction_id = insert_transaction(
            normalized_data,
            text
        )

        normalized_data["transaction_id"] = transaction_id

    return extracted_data, normalized_data


def main():

    # Make sure the database/table exists.
    create_table()

    print("=" * 60)
    print("WhatsApp Financial Data Extraction Pipeline")
    print("=" * 60)

    text = input("\nEnter WhatsApp message:\n> ")

    # ---------------------------------------------------------
    # STEP 1: ML EXTRACTION
    # ---------------------------------------------------------

    extracted_data, normalized_data = process_message(text)

    print("\nRaw ML Output")
    print("-" * 60)

    print(json.dumps(extracted_data, indent=4))

    # ---------------------------------------------------------
    # STEP 2: VALIDATION + NORMALIZATION
    # ---------------------------------------------------------

    print("\nValidated & Normalized Data")
    print("-" * 60)

    print(json.dumps(normalized_data, indent=4))

    # ---------------------------------------------------------
    # STEP 3: DATABASE
    # ---------------------------------------------------------

    print("\nPipeline Status")
    print("-" * 60)

    if normalized_data["is_valid"]:

        print("STATUS: VALID")
        print(
            f"Transaction saved to database "
            f"with ID: {normalized_data['transaction_id']}"
        )

    else:

        print("STATUS: INVALID")
        print("Transaction was NOT saved.")

        print("\nValidation Errors:")

        for field, status in normalized_data["validation"].items():

            if not status:
                print(f"- {field}")


if __name__ == "__main__":
    main()