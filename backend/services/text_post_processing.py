def normalize_ocr_text(text: str) -> str:
    if not text:
        return ""

    lines = [l.strip() for l in text.split("\n") if l.strip()]

    merged = []
    buffer = ""

    for line in lines:
        if line.endswith((":", "–", "-", ",")):
            buffer += " " + line
        else:
            if buffer:
                merged.append(buffer + " " + line)
                buffer = ""
            else:
                merged.append(line)

    if buffer:
        merged.append(buffer)

    return "\n".join(merged)
