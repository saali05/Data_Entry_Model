import json
import random
from pathlib import Path


# ============================================================
# PATHS
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parent.parent

INPUT_PATH = (
    PROJECT_ROOT
    / "data"
    / "processed"
    / "combined_annotations_v10.json"
)

TRAIN_PATH = (
    PROJECT_ROOT
    / "data"
    / "train_v10.json"
)

VALIDATION_PATH = (
    PROJECT_ROOT
    / "data"
    / "validation_v10.json"
)

TEST_PATH = (
    PROJECT_ROOT
    / "data"
    / "test_v10.json"
)


# ============================================================
# SETTINGS
# ============================================================

RANDOM_SEED = 42

TRAIN_RATIO = 0.70
VALIDATION_RATIO = 0.15
TEST_RATIO = 0.15


# ============================================================
# LOAD DATA
# ============================================================

def load_data():

    print("Loading V10 combined dataset...")

    with open(
        INPUT_PATH,
        "r",
        encoding="utf-8"
    ) as f:

        data = json.load(f)

    print(f"Input examples: {len(data)}")

    return data


# ============================================================
# COUNT ENTITIES
# ============================================================

def count_entities(data):

    return sum(
        len(item.get("entities", []))
        for item in data
    )


# ============================================================
# SAVE DATA
# ============================================================

def save_data(path, data):

    with open(
        path,
        "w",
        encoding="utf-8"
    ) as f:

        json.dump(
            data,
            f,
            indent=2,
            ensure_ascii=False
        )


# ============================================================
# MAIN
# ============================================================

def main():

    print("=" * 70)
    print("V10 DATASET SPLIT")
    print("=" * 70)

    data = load_data()

    # --------------------------------------------------------
    # Shuffle
    # --------------------------------------------------------

    random.seed(RANDOM_SEED)

    random.shuffle(data)

    # --------------------------------------------------------
    # Calculate split sizes
    # --------------------------------------------------------

    total = len(data)

    train_size = int(
        total * TRAIN_RATIO
    )

    validation_size = int(
        total * VALIDATION_RATIO
    )

    # Remaining examples go to test
    test_size = (
        total
        - train_size
        - validation_size
    )

    # --------------------------------------------------------
    # Split
    # --------------------------------------------------------

    train_data = data[
        :train_size
    ]

    validation_data = data[
        train_size:
        train_size + validation_size
    ]

    test_data = data[
        train_size + validation_size:
    ]

    # --------------------------------------------------------
    # Count entities
    # --------------------------------------------------------

    train_entities = count_entities(
        train_data
    )

    validation_entities = count_entities(
        validation_data
    )

    test_entities = count_entities(
        test_data
    )

    # --------------------------------------------------------
    # Display
    # --------------------------------------------------------

    print()
    print("=" * 70)
    print("V10 DATASET SPLIT")
    print("=" * 70)

    print(
        f"TRAIN        Examples: {len(train_data):3d} "
        f"| Entities: {train_entities}"
    )

    print(
        f"VALIDATION   Examples: {len(validation_data):3d} "
        f"| Entities: {validation_entities}"
    )

    print(
        f"TEST         Examples: {len(test_data):3d} "
        f"| Entities: {test_entities}"
    )

    print(
        f"Total        Examples: {total:3d}"
    )

    print(
        f"Random seed: {RANDOM_SEED}"
    )

    # --------------------------------------------------------
    # Save
    # --------------------------------------------------------

    save_data(
        TRAIN_PATH,
        train_data
    )

    save_data(
        VALIDATION_PATH,
        validation_data
    )

    save_data(
        TEST_PATH,
        test_data
    )

    print()
    print("Files created:")

    print(TRAIN_PATH)
    print(VALIDATION_PATH)
    print(TEST_PATH)

    print()
    print("=" * 70)
    print("V9 DATASET SPLIT COMPLETE")
    print("=" * 70)


if __name__ == "__main__":
    main()