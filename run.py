from src.excel_tracker import (
    initialize_tracker
)

from src.resume_parser import (
    parse_resume
)


def main():

    initialize_tracker()

    profile = parse_resume(
        "resume/Parameshwari_New.pdf"
    )

    print(
        "\nResume Parsed Successfully"
    )

    print(profile)


if __name__ == "__main__":
    main()
