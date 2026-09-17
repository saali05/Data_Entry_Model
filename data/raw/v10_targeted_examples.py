"""
V10 Targeted NER Examples
=========================

Purpose:
Improve the WhatsApp financial data extraction NER model based on V9 errors.

Targeted problems:
1. Transaction/reference/OTP numbers being incorrectly classified.
2. AMOUNT vs ACCOUNT_NUMBER confusion.
3. NAME boundary errors.
4. Names followed by punctuation.
5. Context-free names near financial information.
6. Natural WhatsApp wording.
7. Different field orders.

AMOUNT annotation policy:
Only the numeric monetary value is annotated.

Examples:
    ₹5000        -> AMOUNT = 5000
    Rs 5000      -> AMOUNT = 5000
    5000 INR     -> AMOUNT = 5000
    25k          -> AMOUNT = 25k

Currency indicators remain outside AMOUNT.
"""

import json


VALID_LABELS = {
    "NAME",
    "ACCOUNT_NUMBER",
    "IFSC_CODE",
    "AMOUNT",
}


# ---------------------------------------------------------------------------
# Helper
# ---------------------------------------------------------------------------

def build_examples():
    examples = []

    def add_example(text, entities):
        """
        entities format:

        [
            ("entity text", "LABEL"),
            ("entity text", "LABEL"),
        ]

        The function automatically calculates character offsets.
        """

        annotations = []
        search_start = 0

        for entity_text, label in entities:

            if label not in VALID_LABELS:
                raise ValueError(
                    f"Invalid label '{label}' in text:\n{text}"
                )

            start = text.find(entity_text, search_start)

            if start == -1:
                raise ValueError(
                    f"Could not find entity '{entity_text}' "
                    f"in text:\n{text}"
                )

            end = start + len(entity_text)

            annotations.append(
                (start, end, label)
            )

            search_start = end

        examples.append({
            "text": text,
            "entities": annotations
        })

    # =======================================================================
    # 1. TRANSACTION ID / REFERENCE NUMBER / OTP NEGATIVES
    # =======================================================================

    add_example(
        "Transaction ID 456789123. Please pay 8000 to Kumar.",
        [
            ("8000", "AMOUNT"),
            ("Kumar", "NAME"),
        ],
    )

    add_example(
        "Transaction ID 728391. Send 5000 to Arun Kumar.",
        [
            ("5000", "AMOUNT"),
            ("Arun Kumar", "NAME"),
        ],
    )

    add_example(
        "Transaction number 123456789. Transfer 7500 to Meera.",
        [
            ("7500", "AMOUNT"),
            ("Meera", "NAME"),
        ],
    )

    add_example(
        "Reference number 789456 was generated. Send 7000 to Priya.",
        [
            ("7000", "AMOUNT"),
            ("Priya", "NAME"),
        ],
    )

    add_example(
        "Reference number 908765. Please transfer 9500 to Rahul Das.",
        [
            ("9500", "AMOUNT"),
            ("Rahul Das", "NAME"),
        ],
    )

    add_example(
        "Payment reference number is 728391.",
        [],
    )

    add_example(
        "Reference number 789456.",
        [],
    )

    add_example(
        "Transaction ID is 456782.",
        [],
    )

    add_example(
        "Transaction ID TXN456782.",
        [],
    )

    add_example(
        "OTP: 391827. Please do not share it.",
        [],
    )

    add_example(
        "OTP is 391827. Please do not share it.",
        [],
    )

    add_example(
        "Use OTP 519263 to continue.",
        [],
    )

    add_example(
        "Please enter OTP 482913.",
        [],
    )

    add_example(
        "Verification code 728194 is required.",
        [],
    )

    add_example(
        "Security code 563829. Do not share this code.",
        [],
    )

    # =======================================================================
    # 2. AMOUNT WITH STRONG CONTEXT
    # =======================================================================

    add_example(
        "Payment amount is 18750.",
        [
            ("18750", "AMOUNT"),
        ],
    )

    add_example(
        "The payment amount is 12500.",
        [
            ("12500", "AMOUNT"),
        ],
    )

    add_example(
        "Amount to transfer is 9500.",
        [
            ("9500", "AMOUNT"),
        ],
    )

    add_example(
        "Transfer amount: 16000.",
        [
            ("16000", "AMOUNT"),
        ],
    )

    add_example(
        "Please send an amount of 8500.",
        [
            ("8500", "AMOUNT"),
        ],
    )

    add_example(
        "The amount is Rs 18750.",
        [
            ("18750", "AMOUNT"),
        ],
    )

    add_example(
        "Payment amount is Rs. 25000.",
        [
            ("25000", "AMOUNT"),
        ],
    )

    add_example(
        "Send amount 7500 INR.",
        [
            ("7500", "AMOUNT"),
        ],
    )

    add_example(
        "Please transfer ₹16000.",
        [
            ("16000", "AMOUNT"),
        ],
    )

    add_example(
        "Pay ₹4500 to Kiran Jose.",
        [
            ("4500", "AMOUNT"),
            ("Kiran Jose", "NAME"),
        ],
    )

    # =======================================================================
    # 3. AMOUNT VS ACCOUNT NUMBER
    # =======================================================================

    add_example(
        "Transfer to Suresh Babu. Bank account 998877665544. Payment amount is 18750.",
        [
            ("Suresh Babu", "NAME"),
            ("998877665544", "ACCOUNT_NUMBER"),
            ("18750", "AMOUNT"),
        ],
    )

    add_example(
        "Send 5000 to Arun Kumar. Account 123456789012.",
        [
            ("5000", "AMOUNT"),
            ("Arun Kumar", "NAME"),
            ("123456789012", "ACCOUNT_NUMBER"),
        ],
    )

    add_example(
        "12500 should be sent to Meera Nair. Account 987654321098.",
        [
            ("12500", "AMOUNT"),
            ("Meera Nair", "NAME"),
            ("987654321098", "ACCOUNT_NUMBER"),
        ],
    )

    add_example(
        "Please transfer 8500 to Rahul Das. Account 112233445566.",
        [
            ("8500", "AMOUNT"),
            ("Rahul Das", "NAME"),
            ("112233445566", "ACCOUNT_NUMBER"),
        ],
    )

    add_example(
        "9999 needs to be sent to Rajesh Kumar. Account 909090123456.",
        [
            ("9999", "AMOUNT"),
            ("Rajesh Kumar", "NAME"),
            ("909090123456", "ACCOUNT_NUMBER"),
        ],
    )

    add_example(
        "Transfer 15000 to Anjali Menon. Account 667788990011.",
        [
            ("15000", "AMOUNT"),
            ("Anjali Menon", "NAME"),
            ("667788990011", "ACCOUNT_NUMBER"),
        ],
    )

    add_example(
        "Pay 6300 to Lakshmi Menon. Account 123443211234.",
        [
            ("6300", "AMOUNT"),
            ("Lakshmi Menon", "NAME"),
            ("123443211234", "ACCOUNT_NUMBER"),
        ],
    )

    add_example(
        "Send 7200 to Suresh Babu. Account number 998877665544.",
        [
            ("7200", "AMOUNT"),
            ("Suresh Babu", "NAME"),
            ("998877665544", "ACCOUNT_NUMBER"),
        ],
    )

    add_example(
        "Transfer 18750 to Fathima. Bank account 889900112233.",
        [
            ("18750", "AMOUNT"),
            ("Fathima", "NAME"),
            ("889900112233", "ACCOUNT_NUMBER"),
        ],
    )

    add_example(
        "Please pay 4500 to Kiran Jose. Account no 667700889911.",
        [
            ("4500", "AMOUNT"),
            ("Kiran Jose", "NAME"),
            ("667700889911", "ACCOUNT_NUMBER"),
        ],
    )

    # =======================================================================
    # 4. NATURAL WHATSAPP MESSAGES
    # =======================================================================

    add_example(
        "bro send 9500 to Rahul Das. Account 556677889900",
        [
            ("9500", "AMOUNT"),
            ("Rahul Das", "NAME"),
            ("556677889900", "ACCOUNT_NUMBER"),
        ],
    )

    add_example(
        "pls send 8500 INR to Suresh. Account no 777788889999",
        [
            ("8500", "AMOUNT"),
            ("Suresh", "NAME"),
            ("777788889999", "ACCOUNT_NUMBER"),
        ],
    )

    add_example(
        "Can you send 11000 to Priya Sharma? Account 445566778899.",
        [
            ("11000", "AMOUNT"),
            ("Priya Sharma", "NAME"),
            ("445566778899", "ACCOUNT_NUMBER"),
        ],
    )

    add_example(
        "Need to pay 16000 to Mohammed Irfan. Account 121212343434.",
        [
            ("16000", "AMOUNT"),
            ("Mohammed Irfan", "NAME"),
            ("121212343434", "ACCOUNT_NUMBER"),
        ],
    )

    add_example(
        "send 9000 to Anu. account 343434343434",
        [
            ("9000", "AMOUNT"),
            ("Anu", "NAME"),
            ("343434343434", "ACCOUNT_NUMBER"),
        ],
    )

    add_example(
        "pls transfer 12000 to Joseph Thomas, acc 454545454545",
        [
            ("12000", "AMOUNT"),
            ("Joseph Thomas", "NAME"),
            ("454545454545", "ACCOUNT_NUMBER"),
        ],
    )

    # =======================================================================
    # 5. NAME BOUNDARY CASES
    # =======================================================================

    add_example(
        "Kiran needs ₹16000. A/c 454545454545. IFSC ICIC0009999.",
        [
            ("Kiran", "NAME"),
            ("16000", "AMOUNT"),
            ("454545454545", "ACCOUNT_NUMBER"),
            ("ICIC0009999", "IFSC_CODE"),
        ],
    )

    add_example(
        "Fathima. Please send 5000 to her account 123456789012.",
        [
            ("Fathima", "NAME"),
            ("5000", "AMOUNT"),
            ("123456789012", "ACCOUNT_NUMBER"),
        ],
    )

    add_example(
        "Rajesh Kumar. Send 9999 to this account 909090123456.",
        [
            ("Rajesh Kumar", "NAME"),
            ("9999", "AMOUNT"),
            ("909090123456", "ACCOUNT_NUMBER"),
        ],
    )

    add_example(
        "Priya Sharma, please receive 7500 in account 445566778899.",
        [
            ("Priya Sharma", "NAME"),
            ("7500", "AMOUNT"),
            ("445566778899", "ACCOUNT_NUMBER"),
        ],
    )

    add_example(
        "Rahul Das is the beneficiary. Send 9500. Account 556677889900.",
        [
            ("Rahul Das", "NAME"),
            ("9500", "AMOUNT"),
            ("556677889900", "ACCOUNT_NUMBER"),
        ],
    )

    add_example(
        "Meera Nair needs 12500. Bank account 987654321098.",
        [
            ("Meera Nair", "NAME"),
            ("12500", "AMOUNT"),
            ("987654321098", "ACCOUNT_NUMBER"),
        ],
    )

    # =======================================================================
    # 6. CONTEXT-FREE / MINIMAL NAME EXAMPLES
    # =======================================================================

    add_example(
        "sugunan, ₹4000, 898989898989, HDFC0001212.",
        [
            ("sugunan", "NAME"),
            ("4000", "AMOUNT"),
            ("898989898989", "ACCOUNT_NUMBER"),
            ("HDFC0001212", "IFSC_CODE"),
        ],
    )

    add_example(
        "Arun, 5000, 123456789012, SBIN0001234.",
        [
            ("Arun", "NAME"),
            ("5000", "AMOUNT"),
            ("123456789012", "ACCOUNT_NUMBER"),
            ("SBIN0001234", "IFSC_CODE"),
        ],
    )

    add_example(
        "Priya, ₹7500, 445566778899, ICIC0004321.",
        [
            ("Priya", "NAME"),
            ("7500", "AMOUNT"),
            ("445566778899", "ACCOUNT_NUMBER"),
            ("ICIC0004321", "IFSC_CODE"),
        ],
    )

    add_example(
        "Rahul Das, 9500, 556677889900, HDFC0005678.",
        [
            ("Rahul Das", "NAME"),
            ("9500", "AMOUNT"),
            ("556677889900", "ACCOUNT_NUMBER"),
            ("HDFC0005678", "IFSC_CODE"),
        ],
    )

    add_example(
        "Meera Nair, 12500, 987654321098, SBIN0009876.",
        [
            ("Meera Nair", "NAME"),
            ("12500", "AMOUNT"),
            ("987654321098", "ACCOUNT_NUMBER"),
            ("SBIN0009876", "IFSC_CODE"),
        ],
    )

    # =======================================================================
    # 7. ACCOUNT NUMBER AT END OF MESSAGE
    # =======================================================================

    add_example(
        "Send ₹5000 to Arun Kumar. Account 123456789012.",
        [
            ("5000", "AMOUNT"),
            ("Arun Kumar", "NAME"),
            ("123456789012", "ACCOUNT_NUMBER"),
        ],
    )

    add_example(
        "₹9999 needs to be sent to Rajesh Kumar. Account 909090123456.",
        [
            ("9999", "AMOUNT"),
            ("Rajesh Kumar", "NAME"),
            ("909090123456", "ACCOUNT_NUMBER"),
        ],
    )

    add_example(
        "Please transfer ₹8500 to Rahul Das. Bank account 112233445566.",
        [
            ("8500", "AMOUNT"),
            ("Rahul Das", "NAME"),
            ("112233445566", "ACCOUNT_NUMBER"),
        ],
    )

    add_example(
        "Pay ₹6300 to Lakshmi Menon. Account no 123443211234.",
        [
            ("6300", "AMOUNT"),
            ("Lakshmi Menon", "NAME"),
            ("123443211234", "ACCOUNT_NUMBER"),
        ],
    )

    # =======================================================================
    # 8. ACCOUNT / PHONE / OTP / REFERENCE HARD NEGATIVES
    # =======================================================================

    add_example(
        "Pay 15500 to Neha. Phone 9123456780. Account 787878121212.",
        [
            ("15500", "AMOUNT"),
            ("Neha", "NAME"),
            ("787878121212", "ACCOUNT_NUMBER"),
        ],
    )

    add_example(
        "Transfer 35000 to Rahul Kumar. Reference REF98231. Account 345678901234.",
        [
            ("35000", "AMOUNT"),
            ("Rahul Kumar", "NAME"),
            ("345678901234", "ACCOUNT_NUMBER"),
        ],
    )

    add_example(
        "Send 14000 to Deepa Krishnan. OTP 482913. Account 221133445566.",
        [
            ("14000", "AMOUNT"),
            ("Deepa Krishnan", "NAME"),
            ("221133445566", "ACCOUNT_NUMBER"),
        ],
    )

    add_example(
        "Pay 8000 to Kumar. Phone 9876543210. OTP 482913. Account 111122223333.",
        [
            ("8000", "AMOUNT"),
            ("Kumar", "NAME"),
            ("111122223333", "ACCOUNT_NUMBER"),
        ],
    )

    add_example(
        "Send 12000 to Anjali. Reference 789456. Phone 9876501234. Account 222233334444.",
        [
            ("12000", "AMOUNT"),
            ("Anjali", "NAME"),
            ("222233334444", "ACCOUNT_NUMBER"),
        ],
    )

    # =======================================================================
    # 9. IFSC WITH OTHER NUMBERS
    # =======================================================================

    add_example(
        "IFSC HDFC0004321, amount Rs 12500, account 667788990011, beneficiary Priyanka Sharma.",
        [
            ("HDFC0004321", "IFSC_CODE"),
            ("12500", "AMOUNT"),
            ("667788990011", "ACCOUNT_NUMBER"),
            ("Priyanka Sharma", "NAME"),
        ],
    )

    add_example(
        "Beneficiary name is Deepa Krishnan. Amount is 9200. Account number is 221133445566.",
        [
            ("Deepa Krishnan", "NAME"),
            ("9200", "AMOUNT"),
            ("221133445566", "ACCOUNT_NUMBER"),
        ],
    )

    add_example(
        "Name: Suresh Babu. Amount: 18750. Account: 998877665544. IFSC: SBIN0001234.",
        [
            ("Suresh Babu", "NAME"),
            ("18750", "AMOUNT"),
            ("998877665544", "ACCOUNT_NUMBER"),
            ("SBIN0001234", "IFSC_CODE"),
        ],
    )

    # =======================================================================
    # 10. MULTIPLE UNRELATED NUMBERS
    # =======================================================================

    add_example(
        "Transaction 728391, OTP 391827, phone 9876543210. Send 8500 to Rahul. Account 123456789012.",
        [
            ("8500", "AMOUNT"),
            ("Rahul", "NAME"),
            ("123456789012", "ACCOUNT_NUMBER"),
        ],
    )

    add_example(
        "Reference 908765 and phone 9876501234. Pay 6500 to Meera. Account 555566667777.",
        [
            ("6500", "AMOUNT"),
            ("Meera", "NAME"),
            ("555566667777", "ACCOUNT_NUMBER"),
        ],
    )

    add_example(
        "OTP 123456. Transaction ID 789012. Send 11000 to Priya Sharma. Account 444455556666.",
        [
            ("11000", "AMOUNT"),
            ("Priya Sharma", "NAME"),
            ("444455556666", "ACCOUNT_NUMBER"),
        ],
    )

    # =======================================================================
    # 11. COMPLETE NATURAL FINANCIAL MESSAGES
    # =======================================================================

    add_example(
        "Hi, please send ₹15000 to Mohammed Irfan. His bank account is 121212343434 and IFSC is ICIC0009876.",
        [
            ("15000", "AMOUNT"),
            ("Mohammed Irfan", "NAME"),
            ("121212343434", "ACCOUNT_NUMBER"),
            ("ICIC0009876", "IFSC_CODE"),
        ],
    )

    add_example(
        "Please transfer Rs 22000 to Anjali Menon. Account number 667788990011. IFSC HDFC0004321.",
        [
            ("22000", "AMOUNT"),
            ("Anjali Menon", "NAME"),
            ("667788990011", "ACCOUNT_NUMBER"),
            ("HDFC0004321", "IFSC_CODE"),
        ],
    )

    add_example(
        "Send 17500 INR to Fathima. A/C 889900112233. Bank code SBIN0001234.",
        [
            ("17500", "AMOUNT"),
            ("Fathima", "NAME"),
            ("889900112233", "ACCOUNT_NUMBER"),
            ("SBIN0001234", "IFSC_CODE"),
        ],
    )

    add_example(
        "Need to pay 9800 to Kiran Jose. Account 667700889911. IFSC ICIC0009999.",
        [
            ("9800", "AMOUNT"),
            ("Kiran Jose", "NAME"),
            ("667700889911", "ACCOUNT_NUMBER"),
            ("ICIC0009999", "IFSC_CODE"),
        ],
    )

    return examples


# ---------------------------------------------------------------------------
# Validation
# ---------------------------------------------------------------------------

def validate_examples(examples):

    print("=" * 70)
    print("VALIDATING V10 TARGETED DATASET")
    print("=" * 70)

    total_entities = 0

    for index, example in enumerate(examples, start=1):

        text = example["text"]
        entities = example["entities"]

        if not isinstance(text, str):
            raise ValueError(
                f"Example {index}: text must be a string."
            )

        if not isinstance(entities, list):
            raise ValueError(
                f"Example {index}: entities must be a list."
            )

        spans = []

        for entity in entities:

            if not isinstance(entity, (list, tuple)):
                raise ValueError(
                    f"Example {index}: invalid entity format: {entity}"
                )

            if len(entity) != 3:
                raise ValueError(
                    f"Example {index}: entity must contain "
                    f"(start, end, label): {entity}"
                )

            start, end, label = entity

            if not isinstance(start, int) or not isinstance(end, int):
                raise ValueError(
                    f"Example {index}: start/end must be integers: {entity}"
                )

            if start < 0 or end > len(text) or start >= end:
                raise ValueError(
                    f"Example {index}: invalid span {entity}"
                )

            if label not in VALID_LABELS:
                raise ValueError(
                    f"Example {index}: invalid label {label}"
                )

            entity_text = text[start:end]

            if not entity_text:
                raise ValueError(
                    f"Example {index}: empty entity span."
                )

            spans.append(
                (start, end, label)
            )

            total_entities += 1

        # Check overlapping entities
        sorted_spans = sorted(
            spans,
            key=lambda x: (x[0], x[1])
        )

        for previous, current in zip(
            sorted_spans,
            sorted_spans[1:]
        ):

            previous_start, previous_end, _ = previous
            current_start, current_end, _ = current

            if current_start < previous_end:
                raise ValueError(
                    f"Example {index}: overlapping entities:\n"
                    f"  {previous}\n"
                    f"  {current}"
                )

    print()
    print(f"Examples : {len(examples)}")
    print(f"Entities : {total_entities}")
    print()
    print("All spans are valid.")
    print("No overlapping entities.")
    print("All labels are valid.")
    print()
    print("V10 dataset validation passed.")
    print("=" * 70)


# ---------------------------------------------------------------------------
# Save dataset
# ---------------------------------------------------------------------------

def save_examples(examples, output_path):

    with open(
        output_path,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            examples,
            file,
            indent=2,
            ensure_ascii=False
        )

    print()
    print("Saved dataset to:")
    print(output_path)


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

if __name__ == "__main__":

    examples = build_examples()

    validate_examples(examples)

    output_path = "data/raw/v10_targeted_examples.json"

    save_examples(
        examples,
        output_path
    )

    print()
    print("V10 TARGETED DATASET COMPLETE")
    print()
    print("Target areas:")
    print("  - Transaction/reference number negatives")
    print("  - OTP/verification code negatives")
    print("  - AMOUNT vs ACCOUNT_NUMBER")
    print("  - NAME boundary errors")
    print("  - Context-free names")
    print("  - Account number at end of message")
    print("  - Phone/OTP/reference hard negatives")
    print("  - Natural WhatsApp messages")
    print("  - IFSC + financial number combinations")