from pathlib import Path
import spacy


# ============================================================
# PATHS
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parents[2]

MODEL_PATH = (
    PROJECT_ROOT
    / "models"
    / "whatsapp_ner_v10"
)


# ============================================================
# COMPLETELY UNSEEN WHATSAPP MESSAGES
# ============================================================

MESSAGES = [

    # 1. Normal complete message
    "Hey, please send Rs. 27,500 to Anoop Menon. "
    "A/C 778899001122, IFSC SBIN0004567.",

    # 2. INR suffix
    "Transfer 32000 INR to Farhan Ali. "
    "Account number 987654321098.",

    # 3. Multiple unrelated numbers
    "Please send ₹4,750 to Meera Nair. "
    "A/c 112233445566. My phone is 9876543210.",

    # 4. Hard context with phone and transaction ID
    "Beneficiary: Rahul Das. "
    "Phone: 9876543210. "
    "Reference: TXN829374. "
    "Amount: 18500 INR. "
    "A/C: 556677889900. "
    "IFSC: ICIC0007890.",

    # 5. Different field order
    "IFSC HDFC0004321, amount Rs 12500, "
    "account 667788990011, beneficiary Priyanka Sharma.",

    # 6. Informal WhatsApp wording
    "Bro send 8500 to Vishnu pls. "
    "A/c no 445566778899.",

    # 7. k notation
    "Please transfer 25k to Nikhil Raj. "
    "Account: 334455667788.",

    # 8. decimal k notation
    "Send 20.5k to Fathima. "
    "A/C 889900112233.",

    # 9. Amount context
    "Recipient name is Deepa Krishnan. "
    "Amount is 9200. "
    "Account number is 221133445566.",

    # 10. Currency symbol with comma
    "Can you transfer ₹18,750 to Suresh Babu? "
    "Bank account: 998877665544.",

    # 11. No IFSC
    "Pay Rs. 6,300 to Lakshmi Menon. "
    "A/C 123443211234.",

    # 12. No account number
    "Send ₹11,000 to Arjun Kumar. "
    "IFSC: SBIN0009876.",

    # 13. No amount
    "Beneficiary: Sneha Thomas. "
    "Account: 445566778811. "
    "IFSC: HDFC0008765.",

    # 14. Numbers that should NOT become entities
    "OTP is 482913. "
    "Transaction ID is TXN456782. "
    "Please call 9847012345.",

    # 15. Multiple financial numbers
    "Account 123456789012, amount 15000, "
    "reference 908765, phone 9876501234. "
    "Send to Mohammed Irfan.",

    # 16. Very informal
    "pls pay 7200 to Anjali. "
    "acc 778811223344, ifsc ICIC0001234",

    # 17. Different wording
    "Beneficiary account holder is Kiran Jose. "
    "Transfer amount: 14,500 INR. "
    "A/C No: 667700889911.",

    # 18. Amount before beneficiary
    "₹9,999 needs to be sent to Rajesh Kumar. "
    "Account 909090123456.",

    # 19. Mixed unrelated numbers
    "Send Rs 16,250 to Neha. "
    "OTP 654321, phone 9123456780, "
    "A/C 787878121212.",

    # 20. Complete difficult message
    "Hi, transfer 35k to Rahul Kumar today. "
    "Bank A/C: 345678901234. "
    "IFSC Code: AXIS0005678. "
    "My reference is REF98231 and contact is 9895012345.",
]


# ============================================================
# EXPECTED ENTITIES
# ============================================================

EXPECTED = [

    {
        "NAME": ["Anoop Menon"],
        "ACCOUNT_NUMBER": ["778899001122"],
        "IFSC_CODE": ["SBIN0004567"],
        "AMOUNT": ["27,500"],
    },

    {
        "NAME": ["Farhan Ali"],
        "ACCOUNT_NUMBER": ["987654321098"],
        "IFSC_CODE": [],
        "AMOUNT": ["32000"],
    },

    {
        "NAME": ["Meera Nair"],
        "ACCOUNT_NUMBER": ["112233445566"],
        "IFSC_CODE": [],
        "AMOUNT": ["4,750"],
    },

    {
        "NAME": ["Rahul Das"],
        "ACCOUNT_NUMBER": ["556677889900"],
        "IFSC_CODE": ["ICIC0007890"],
        "AMOUNT": ["18500"],
    },

    {
        "NAME": ["Priyanka Sharma"],
        "ACCOUNT_NUMBER": ["667788990011"],
        "IFSC_CODE": ["HDFC0004321"],
        "AMOUNT": ["12500"],
    },

    {
        "NAME": ["Vishnu"],
        "ACCOUNT_NUMBER": ["445566778899"],
        "IFSC_CODE": [],
        "AMOUNT": ["8500"],
    },

    {
        "NAME": ["Nikhil Raj"],
        "ACCOUNT_NUMBER": ["334455667788"],
        "IFSC_CODE": [],
        "AMOUNT": ["25k"],
    },

    {
        "NAME": ["Fathima"],
        "ACCOUNT_NUMBER": ["889900112233"],
        "IFSC_CODE": [],
        "AMOUNT": ["20.5k"],
    },

    {
        "NAME": ["Deepa Krishnan"],
        "ACCOUNT_NUMBER": ["221133445566"],
        "IFSC_CODE": [],
        "AMOUNT": ["9200"],
    },

    {
        "NAME": ["Suresh Babu"],
        "ACCOUNT_NUMBER": ["998877665544"],
        "IFSC_CODE": [],
        "AMOUNT": ["18,750"],
    },

    {
        "NAME": ["Lakshmi Menon"],
        "ACCOUNT_NUMBER": ["123443211234"],
        "IFSC_CODE": [],
        "AMOUNT": ["6,300"],
    },

    {
        "NAME": ["Arjun Kumar"],
        "ACCOUNT_NUMBER": [],
        "IFSC_CODE": ["SBIN0009876"],
        "AMOUNT": ["11,000"],
    },

    {
        "NAME": ["Sneha Thomas"],
        "ACCOUNT_NUMBER": ["445566778811"],
        "IFSC_CODE": ["HDFC0008765"],
        "AMOUNT": [],
    },

    {
        "NAME": [],
        "ACCOUNT_NUMBER": [],
        "IFSC_CODE": [],
        "AMOUNT": [],
    },

    {
        "NAME": ["Mohammed Irfan"],
        "ACCOUNT_NUMBER": ["123456789012"],
        "IFSC_CODE": [],
        "AMOUNT": ["15000"],
    },

    {
        "NAME": ["Anjali"],
        "ACCOUNT_NUMBER": ["778811223344"],
        "IFSC_CODE": ["ICIC0001234"],
        "AMOUNT": ["7200"],
    },

    {
        "NAME": ["Kiran Jose"],
        "ACCOUNT_NUMBER": ["667700889911"],
        "IFSC_CODE": [],
        "AMOUNT": ["14,500"],
    },

    {
        "NAME": ["Rajesh Kumar"],
        "ACCOUNT_NUMBER": ["909090123456"],
        "IFSC_CODE": [],
        "AMOUNT": ["9,999"],
    },

    {
        "NAME": ["Neha"],
        "ACCOUNT_NUMBER": ["787878121212"],
        "IFSC_CODE": [],
        "AMOUNT": ["16,250"],
    },

    {
        "NAME": ["Rahul Kumar"],
        "ACCOUNT_NUMBER": ["345678901234"],
        "IFSC_CODE": ["AXIS0005678"],
        "AMOUNT": ["35k"],
    },
]


# ============================================================
# HELPERS
# ============================================================

LABELS = [
    "NAME",
    "ACCOUNT_NUMBER",
    "IFSC_CODE",
    "AMOUNT",
]


def extract_entities(doc):

    result = {
        label: []
        for label in LABELS
    }

    for ent in doc.ents:

        if ent.label_ in result:
            result[ent.label_].append(
                ent.text
            )

    return result


def compare(expected, predicted):

    errors = []

    for label in LABELS:

        if expected[label] != predicted[label]:

            errors.append(
                label
            )

    return errors


# ============================================================
# MAIN
# ============================================================

def main():

    print("Loading V4 model...")

    nlp = spacy.load(
        MODEL_PATH
    )

    print("Model loaded successfully.")

    print()
    print("=" * 70)
    print("PHASE 6 — UNSEEN MESSAGE TEST")
    print("=" * 70)

    total_messages = len(MESSAGES)
    correct_messages = 0
    total_entity_errors = 0

    for index, (text, expected) in enumerate(
        zip(MESSAGES, EXPECTED),
        start=1,
    ):

        doc = nlp(text)

        predicted = extract_entities(doc)

        errors = compare(
            expected,
            predicted,
        )

        print()
        print("-" * 70)
        print(f"MESSAGE #{index}")
        print("-" * 70)

        print("TEXT:")
        print(text)

        print()
        print("EXPECTED:")
        print(expected)

        print()
        print("PREDICTED:")
        print(predicted)

        if not errors:

            correct_messages += 1

            print()
            print("STATUS: ✅ CORRECT")

        else:

            total_entity_errors += len(errors)

            print()
            print(
                "STATUS: ❌ ERROR"
            )

            print(
                "Failed labels:",
                ", ".join(errors),
            )

    # --------------------------------------------------------
    # SUMMARY
    # --------------------------------------------------------

    accuracy = (
        correct_messages
        / total_messages
        * 100
    )

    print()
    print("=" * 70)
    print("UNSEEN TEST SUMMARY")
    print("=" * 70)

    print(
        f"Total messages     : {total_messages}"
    )

    print(
        f"Correct messages   : {correct_messages}"
    )

    print(
        f"Incorrect messages : "
        f"{total_messages - correct_messages}"
    )

    print(
        f"Message accuracy   : "
        f"{accuracy:.2f}%"
    )

    print(
        f"Entity-level error groups: "
        f"{total_entity_errors}"
    )

    print()

    if correct_messages == total_messages:

        print(
            "🎉 ALL UNSEEN MESSAGES PASSED"
        )

    else:

        print(
            "⚠️ Some unseen messages failed."
        )

        print(
            "Review the failed cases before "
            "adding new training data."
        )


if __name__ == "__main__":
    main()