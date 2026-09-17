import json
import random
from pathlib import Path
from collections import defaultdict

import spacy
from spacy.training import Example


# ============================================================
# PATHS
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parent.parent

MODEL_PATH = PROJECT_ROOT / "models" / "whatsapp_ner_v10"

VALIDATION_PATH = PROJECT_ROOT / "data" / "validation_v10.json"
TEST_PATH = PROJECT_ROOT / "data" / "test_v10.json"


LABELS = [
    "NAME",
    "ACCOUNT_NUMBER",
    "IFSC_CODE",
    "AMOUNT",
]


# ============================================================
# LOAD DATASET
# ============================================================

def load_dataset(path):
    print(f"Loading dataset:")
    print(f"  {path}")

    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)

    print(f"Examples loaded: {len(data)}")

    return data


# ============================================================
# CONVERT ENTITIES TO SPACY FORMAT
# ============================================================

def convert_entities(entities):
    """
    Convert our JSON entity format into spaCy format.

    Input examples:

        {
            "start": 10,
            "end": 20,
            "label": "NAME"
        }

    OR:

        [10, 20, "NAME"]

    Output:

        [
            (10, 20, "NAME")
        ]
    """

    converted = []

    for entity in entities:

        # Dictionary format
        if isinstance(entity, dict):

            start = entity["start"]
            end = entity["end"]
            label = entity["label"]

        # List / tuple format
        elif isinstance(entity, (list, tuple)):

            if len(entity) != 3:
                raise ValueError(
                    f"Invalid entity format: {entity}"
                )

            start, end, label = entity

        else:
            raise TypeError(
                f"Unexpected entity type: {type(entity)}"
            )

        converted.append(
            (
                int(start),
                int(end),
                str(label)
            )
        )

    # spaCy expects entities ordered by start position
    converted.sort(key=lambda x: x[0])

    return converted


# ============================================================
# PREPARE SPACY EXAMPLE
# ============================================================

def create_spacy_example(nlp, item):

    text = item["text"]

    entities = item.get("entities", [])

    spacy_entities = convert_entities(entities)

    annotations = {
        "entities": spacy_entities
    }

    reference_doc = nlp.make_doc(text)

    example = Example.from_dict(
        reference_doc,
        annotations
    )

    return example


# ============================================================
# EVALUATE DATASET
# ============================================================

def evaluate_dataset(nlp, dataset, dataset_name):

    print()
    print("=" * 70)
    print(f"EVALUATING {dataset_name}")
    print("=" * 70)

    examples = []

    for item in dataset:

        example = create_spacy_example(
            nlp,
            item
        )

        examples.append(example)

    print(f"Examples evaluated: {len(examples)}")

    # --------------------------------------------------------
    # spaCy Scorer
    # --------------------------------------------------------

    scores = nlp.evaluate(examples)

    ents_p = scores.get("ents_p", 0.0)
    ents_r = scores.get("ents_r", 0.0)
    ents_f = scores.get("ents_f", 0.0)

    print()
    print("Overall Performance")
    print("-" * 70)

    print(f"Precision : {ents_p:.4f}")
    print(f"Recall    : {ents_r:.4f}")
    print(f"F1 Score  : {ents_f:.4f}")

    # --------------------------------------------------------
    # Per-label metrics
    # --------------------------------------------------------

    print()
    print("Per-Entity Performance")
    print("-" * 70)

    per_type = scores.get("ents_per_type", {})

    for label in LABELS:

        metrics = per_type.get(label, {})

        precision = metrics.get("p", 0.0)
        recall = metrics.get("r", 0.0)
        f1 = metrics.get("f", 0.0)

        print(
            f"{label:<18}"
            f"P: {precision:.4f}  "
            f"R: {recall:.4f}  "
            f"F1: {f1:.4f}"
        )

    return scores


# ============================================================
# MANUAL ERROR ANALYSIS
# ============================================================

def error_analysis(nlp, dataset, dataset_name):

    print()
    print("=" * 70)
    print(f"ERROR ANALYSIS - {dataset_name}")
    print("=" * 70)

    total_errors = 0

    for index, item in enumerate(dataset, start=1):

        text = item["text"]

        expected_entities = convert_entities(
            item.get("entities", [])
        )

        doc = nlp(text)

        expected = [
            {
                "text": text[start:end],
                "label": label,
                "start": start,
                "end": end,
            }
            for start, end, label in expected_entities
        ]

        predicted = [
            {
                "text": ent.text,
                "label": ent.label_,
                "start": ent.start_char,
                "end": ent.end_char,
            }
            for ent in doc.ents
        ]

        expected_set = {
            (
                entity["start"],
                entity["end"],
                entity["label"]
            )
            for entity in expected
        }

        predicted_set = {
            (
                entity["start"],
                entity["end"],
                entity["label"]
            )
            for entity in predicted
        }

        if expected_set != predicted_set:

            total_errors += 1

            print()
            print(f"Message #{index}")
            print("-" * 70)

            print(f"Text:")
            print(text)

            print()
            print("Expected:")

            if expected:
                for entity in expected:
                    print(
                        f"  {entity['label']:<18}"
                        f"→ {entity['text']}"
                    )
            else:
                print("  No entities")

            print()
            print("Predicted:")

            if predicted:
                for entity in predicted:
                    print(
                        f"  {entity['label']:<18}"
                        f"→ {entity['text']}"
                    )
            else:
                print("  No entities")

            # ------------------------------------------------
            # Missing entities
            # ------------------------------------------------

            missing = expected_set - predicted_set

            if missing:

                print()
                print("Missing:")

                for start, end, label in sorted(missing):

                    print(
                        f"  {label:<18}"
                        f"→ {text[start:end]}"
                    )

            # ------------------------------------------------
            # Extra predictions
            # ------------------------------------------------

            extra = predicted_set - expected_set

            if extra:

                print()
                print("Extra predictions:")

                for start, end, label in sorted(extra):

                    print(
                        f"  {label:<18}"
                        f"→ {text[start:end]}"
                    )

    print()
    print("=" * 70)
    print(f"{dataset_name} ERROR SUMMARY")
    print("=" * 70)

    print(f"Messages with errors: {total_errors}")
    print(f"Messages evaluated  : {len(dataset)}")

    if len(dataset) > 0:

        accuracy = (
            (len(dataset) - total_errors)
            / len(dataset)
        )

        print(
            f"Message-level accuracy: "
            f"{accuracy * 100:.2f}%"
        )


# ============================================================
# MAIN
# ============================================================

def main():

    print()
    print("=" * 70)
    print("WHATSAPP FINANCIAL DATA NER - V9 EVALUATION")
    print("=" * 70)

    # --------------------------------------------------------
    # Load model
    # --------------------------------------------------------

    print()
    print("Loading model...")
    print(MODEL_PATH)

    nlp = spacy.load(MODEL_PATH)

    print("Model loaded successfully.")

    # --------------------------------------------------------
    # Load datasets
    # --------------------------------------------------------

    validation_data = load_dataset(
        VALIDATION_PATH
    )

    test_data = load_dataset(
        TEST_PATH
    )

    # --------------------------------------------------------
    # Validate labels
    # --------------------------------------------------------

    print()
    print("Checking dataset labels...")

    for dataset_name, dataset in [
        ("VALIDATION", validation_data),
        ("TEST", test_data),
    ]:

        for item in dataset:

            for entity in item.get("entities", []):

                if isinstance(entity, dict):
                    label = entity["label"]

                else:
                    label = entity[2]

                if label not in LABELS:

                    raise ValueError(
                        f"Unknown label '{label}' "
                        f"in {dataset_name} dataset."
                    )

    print("Dataset labels are valid.")

    # --------------------------------------------------------
    # Evaluate validation
    # --------------------------------------------------------

    validation_scores = evaluate_dataset(
        nlp,
        validation_data,
        "VALIDATION"
    )

    # --------------------------------------------------------
    # Evaluate test
    # --------------------------------------------------------

    test_scores = evaluate_dataset(
        nlp,
        test_data,
        "TEST"
    )

    # --------------------------------------------------------
    # Error analysis
    # --------------------------------------------------------

    error_analysis(
        nlp,
        validation_data,
        "VALIDATION"
    )

    error_analysis(
        nlp,
        test_data,
        "TEST"
    )

    # --------------------------------------------------------
    # Final summary
    # --------------------------------------------------------

    print()
    print("=" * 70)
    print("V8 EVALUATION COMPLETE")
    print("=" * 70)

    print()
    print("VALIDATION")
    print(
        f"Precision : {validation_scores.get('ents_p', 0):.4f}"
    )
    print(
        f"Recall    : {validation_scores.get('ents_r', 0):.4f}"
    )
    print(
        f"F1        : {validation_scores.get('ents_f', 0):.4f}"
    )

    print()
    print("TEST")
    print(
        f"Precision : {test_scores.get('ents_p', 0):.4f}"
    )
    print(
        f"Recall    : {test_scores.get('ents_r', 0):.4f}"
    )
    print(
        f"F1        : {test_scores.get('ents_f', 0):.4f}"
    )

    print()
    print("Model:")
    print(MODEL_PATH)


if __name__ == "__main__":
    main()