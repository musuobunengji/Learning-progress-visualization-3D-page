import json


def read_lines(path):
    with open(path, "r", encoding="utf-8") as f:
        return f.readlines()


def load_content_to_data(chapter_path, section_path, book_name):
    """turn path source text to data structure"""
    chapters = []
    chapter_lines = read_lines(chapter_path)
    section_lines = read_lines(section_path)

    for line in chapter_lines:
        line = line.strip()
        if not line:
            continue

        tokens = line.split()

        if tokens[0].isdigit():
            chapter = {
                "id": f"{book_name}::ch{tokens[0]}",
                "order": int(tokens[0]),
                "title": " ".join(tokens[1:-1]),
                "sections": [],
                "signals": {"bullets": [], "raw_text": ""},
            }
            chapters.append(chapter)
    current_chapter = None
    current_bullet = ""  # bullet 缓冲区在「行循环外」-> bullet 是可能跨行的
    for line in section_lines:
        line = line.strip()
        if not line:
            continue

        tokens = line.split()

        # Situation 1: A Chapter Row
        if tokens[0].isdigit():
            ch_order = int(tokens[0])

            for chapter in chapters:
                if chapter["order"] == ch_order:
                    current_chapter = chapter
                    break
        # Situation 2: A Section Row
        elif "." in tokens[0] and current_chapter is not None:
            section_title = " ".join(tokens[1:-1])
            current_chapter["sections"].append(section_title)
        # Stiuation 3: Bullet Row
        elif current_chapter is not None:
            for token in tokens:
                if token.isdigit():
                    if current_bullet.strip():
                        current_chapter["signals"]["bullets"].append(
                            current_bullet.strip()
                        )
                    current_bullet = ""
                    break
                else:
                    current_bullet += token + " "

    # print(chapters)
    return chapters


def load_data_to_json(book_name, chapters):
    data = {"book_id": book_name, "chapters": chapters}
    with open(f"{book_name}.json", "w", encoding="utf-8") as f:
        json.dump(chapters, fp=f, indent=4, ensure_ascii=False)


def convert_content_to_json(book_name, chapter_path, section_path):
    chapters = load_content_to_data(
        chapter_path=chapter_path, section_path=section_path, book_name=book_name
    )
    load_data_to_json(book_name=book_name, chapters=chapters)


# -------test---------
convert_content_to_json(
    book_name="spring-in-action",
    chapter_path=r"book_content/spring_in_action_brief_content.txt",
    section_path=r"book_content/spring_in_action_content.txt",
)
