import json
import random
from pathlib import Path


INPUT_FILE = Path("data/processed/annotations.json")

TRAIN_FILE = Path("data/train.json")
VALIDATION_FILE = Path("data/validation.json")
TEST_FILE = Path("data/test.json")


TRAIN_RATIO = 0.70
VALIDATION_RATIO = 0.15
TEST_RATIO = 0.15


RANDOM_SEED = 42


def load_data():
    with open(
        INPUT_FILE,
        "r",
        encoding="utf-8",
    ) as file:
        return json.load(file)


def split_data(data):
    random.seed(RANDOM_SEED)

    data = data.copy()

    random.shuffle(data)

    total = len(data)

    train_end = int(total * TRAIN_RATIO)

    validation_end = train_end + int(
        total * VALIDATION_RATIO
    )

    train_data = data[:train_end]

    validation_data = data[
        train_end:validation_end
    ]

    test_data = data[
        validation_end:
    ]

    return (
        train_data,
        validation_data,
        test_data,
    )


def save_data(data, file_path):
    with open(
        file_path,
        "w",
        encoding="utf-8",
    ) as file:
        json.dump(
            data,
            file,
            indent=4,
            ensure_ascii=False,
        )


def main():
    print("Loading dataset...")

    data = load_data()

    print(f"Total examples: {len(data)}")

    train_data, validation_data, test_data = split_data(
        data
    )

    save_data(
        train_data,
        TRAIN_FILE,
    )

    save_data(
        validation_data,
        VALIDATION_FILE,
    )

    save_data(
        test_data,
        TEST_FILE,
    )

    print()
    print("Dataset split completed.")
    print()
    print(f"Training examples:   {len(train_data)}")
    print(f"Validation examples: {len(validation_data)}")
    print(f"Test examples:       {len(test_data)}")


if __name__ == "__main__":
    main()