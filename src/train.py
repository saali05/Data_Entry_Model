"""
Train WhatsApp Financial Data NER - V10
"""

import json
import random
from pathlib import Path

import numpy as np
import spacy
from spacy.training import Example
from spacy.util import minibatch, compounding


# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parent.parent

TRAIN_PATH = PROJECT_ROOT / "data" / "train_v10.json"
VALIDATION_PATH = PROJECT_ROOT / "data" / "validation_v10.json"

MODEL_PATH = PROJECT_ROOT / "models" / "whatsapp_ner_v10"


# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

SEED = 42

ITERATIONS = 30
DROPOUT = 0.2

LABELS = [
    "NAME",
    "ACCOUNT_NUMBER",
    "IFSC_CODE",
    "AMOUNT",
]


# ---------------------------------------------------------------------------
# Random seed
# ---------------------------------------------------------------------------

random.seed(SEED)
np.random.seed(SEED)


# ---------------------------------------------------------------------------
# Load JSON
# ---------------------------------------------------------------------------

def load_json(path):

    with open(
        path,
        "r",
        encoding="utf-8"
    ) as file:

        return json.load(file)


# ---------------------------------------------------------------------------
# Normalize entity
# ---------------------------------------------------------------------------

def normalize_entity(entity):

    # Dictionary format:
    # {"start": 0, "end": 5, "label": "NAME"}

    if isinstance(entity, dict):

        return (
            entity["start"],
            entity["end"],
            entity["label"],
        )

    # List / tuple format:
    # [0, 5, "NAME"]
    # (0, 5, "NAME")

    if isinstance(entity, (list, tuple)):

        return (
            entity[0],
            entity[1],
            entity[2],
        )

    raise ValueError(
        f"Invalid entity format: {entity}"
    )


# ---------------------------------------------------------------------------
# Validate dataset
# ---------------------------------------------------------------------------

def validate_dataset(data, name):

    total_entities = 0

    for index, item in enumerate(
        data,
        start=1
    ):

        text = item["text"]
        entities = item["entities"]

        spans = []

        for entity in entities:

            start, end, label = normalize_entity(
                entity
            )

            if start < 0 or end > len(text):
                raise ValueError(
                    f"{name} example {index}: "
                    f"invalid span {entity}"
                )

            if start >= end:
                raise ValueError(
                    f"{name} example {index}: "
                    f"invalid span {entity}"
                )

            if label not in LABELS:
                raise ValueError(
                    f"{name} example {index}: "
                    f"invalid label {label}"
                )

            spans.append(
                (start, end, label)
            )

            total_entities += 1

        # Check overlap

        sorted_spans = sorted(
            spans,
            key=lambda x: (x[0], x[1])
        )

        for previous, current in zip(
            sorted_spans,
            sorted_spans[1:]
        ):

            if current[0] < previous[1]:

                raise ValueError(
                    f"{name} example {index}: "
                    f"overlapping entities:\n"
                    f"{previous}\n"
                    f"{current}"
                )

    print(
        f"{name}: "
        f"{len(data)} examples | "
        f"{total_entities} entities"
    )

    print(
        "Dataset validation passed."
    )


# ---------------------------------------------------------------------------
# Convert to spaCy Examples
# ---------------------------------------------------------------------------

def convert_to_spacy(data, nlp):

    examples = []

    for item in data:

        text = item["text"]

        entities = []

        for entity in item["entities"]:

            start, end, label = normalize_entity(
                entity
            )

            entities.append(
                (start, end, label)
            )

        doc = nlp.make_doc(text)

        example = Example.from_dict(
            doc,
            {
                "entities": entities
            }
        )

        examples.append(example)

    return examples


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():

    print("=" * 70)
    print("TRAINING WHATSAPP NER V10")
    print("=" * 70)

    print()
    print(f"Random seed: {SEED}")

    # ------------------------------------------------------------------
    # Load datasets
    # ------------------------------------------------------------------

    print()
    print("Loading training data...")

    train_data = load_json(
        TRAIN_PATH
    )

    print(
        f"Training examples: {len(train_data)}"
    )

    print()
    print("Loading validation data...")

    validation_data = load_json(
        VALIDATION_PATH
    )

    print(
        f"Validation examples: "
        f"{len(validation_data)}"
    )

    # ------------------------------------------------------------------
    # Validate
    # ------------------------------------------------------------------

    print()
    print("Validating TRAIN dataset...")

    validate_dataset(
        train_data,
        "TRAIN"
    )

    print()
    print("Validating VALIDATION dataset...")

    validate_dataset(
        validation_data,
        "VALIDATION"
    )

    # ------------------------------------------------------------------
    # Create spaCy pipeline
    # ------------------------------------------------------------------

    print()
    print("Creating spaCy NLP pipeline...")

    nlp = spacy.blank("en")

    # ------------------------------------------------------------------
    # Add NER
    # ------------------------------------------------------------------

    ner = nlp.add_pipe("ner")

    print()
    print("Registering NER labels...")

    for label in LABELS:

        ner.add_label(label)

        print(
            f"  Added label: {label}"
        )

    # ------------------------------------------------------------------
    # Convert datasets
    # ------------------------------------------------------------------

    print()
    print("Converting training data to spaCy format...")

    train_examples = convert_to_spacy(
        train_data,
        nlp
    )

    print(
        f"spaCy training examples: "
        f"{len(train_examples)}"
    )

    print()
    print("Converting validation data to spaCy format...")

    validation_examples = convert_to_spacy(
        validation_data,
        nlp
    )

    print(
        f"spaCy validation examples: "
        f"{len(validation_examples)}"
    )

    # ------------------------------------------------------------------
    # Initialize model
    # ------------------------------------------------------------------

    print()
    print("Initializing model...")

    optimizer = nlp.begin_training()

    # ------------------------------------------------------------------
    # Training
    # ------------------------------------------------------------------

    print()
    print("=" * 70)
    print("STARTING V10 TRAINING")
    print("=" * 70)

    for iteration in range(
        ITERATIONS
    ):

        random.shuffle(
            train_examples
        )

        losses = {}

        batches = minibatch(
            train_examples,
            size=compounding(
                4.0,
                8.0,
                1.001
            )
        )

        for batch in batches:

            nlp.update(
                batch,
                drop=DROPOUT,
                sgd=optimizer,
                losses=losses
            )

        loss = losses.get(
            "ner",
            0.0
        )

        print(
            f"Iteration "
            f"{iteration + 1:02d}/{ITERATIONS} "
            f"- Loss: {loss:.4f}"
        )

    # ------------------------------------------------------------------
    # Save model
    # ------------------------------------------------------------------

    print()
    print("=" * 70)
    print("SAVING V10 MODEL")
    print("=" * 70)

    MODEL_PATH.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    nlp.to_disk(
        MODEL_PATH
    )

    print()
    print("Model saved successfully:")
    print(
        MODEL_PATH
    )

    # ------------------------------------------------------------------
    # Complete
    # ------------------------------------------------------------------

    print()
    print("=" * 70)
    print("V10 TRAINING COMPLETE")
    print("=" * 70)

    print()
    print("Model:")
    print(
        f"  {MODEL_PATH}"
    )

    print()
    print("Training examples:")
    print(
        f"  {len(train_data)}"
    )

    print()
    print("Validation examples:")
    print(
        f"  {len(validation_data)}"
    )

    print()
    print("Labels:")

    for label in LABELS:

        print(
            f"  - {label}"
        )


if __name__ == "__main__":
    main()