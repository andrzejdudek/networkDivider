import re


def parse_port_line(line: str, max_ports: int) -> list[int]:
    """Parses a single string line (1-based user input) into a list of 0-based port indices.

    Supports ranges (e.g., '1-4') and lists (e.g., '1, 2, 5').
    """
    ports = []
    tokens = line.split(",")

    for token in tokens:
        token = token.strip()
        if not token:
            continue

        range_match = re.match(r"^(\d+)\s*-\s*(\d+)$", token)
        if range_match:
            start_p = int(range_match.group(1))
            end_p = int(range_match.group(2))

            if start_p > end_p:
                raise ValueError(f"Invalid range definition: '{token}'")

            ports.extend(range(start_p, end_p + 1))
        elif token.isdigit():
            ports.append(int(token))
        else:
            raise ValueError(f"Invalid port entry: '{token}'")

    if not ports:
        return []

    # Convert 1-based (user input) to 0-based (scikit-rf internal)
    zero_based_ports = []
    for p in ports:
        if p < 1 or p > max_ports:
            raise ValueError(
                f"Port {p} is out of valid range (1..{max_ports})"
            )
        zero_based_ports.append(p - 1)

    return zero_based_ports