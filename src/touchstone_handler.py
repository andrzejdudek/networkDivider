import os
import skrf as rf
from src.parser import parse_port_line


class TouchstoneManager:

    def __init__(self):
        self.network = None
        self.file_path = ""

    def load_file(self, file_path: str) -> dict:
        """Loads a Touchstone file and returns basic metadata."""
        self.network = rf.Network(file_path)
        self.file_path = file_path

        return {
            "filename": os.path.basename(file_path),
            "ports": self.network.number_of_ports,
            "freq_start_mhz": self.network.frequency.start / 1e6,
            "freq_stop_mhz": self.network.frequency.stop / 1e6,
        }

    def process_batch_extraction(self, lines: list[str], output_dir: str) -> int:
        """Processes multiple port configurations and exports sub-network files."""
        if not self.network:
            raise RuntimeError("No Touchstone network loaded.")

        base_name, _ = os.path.splitext(os.path.basename(self.file_path))
        saved_count = 0

        for line in lines:
            zero_based_ports = parse_port_line(
                line, self.network.number_of_ports
            )
            if not zero_based_ports:
                continue

            sub_net = self.network.subnetwork(zero_based_ports)

            # Generate output filename (e.g. MyNetwork_ports_1_2.s2p)
            ports_str = "_".join(str(p + 1) for p in zero_based_ports)
            ext = f".s{len(zero_based_ports)}p"
            out_name = f"{base_name}_ports_{ports_str}{ext}"
            out_path = os.path.join(output_dir, out_name)

            sub_net.write_touchstone(out_path)
            saved_count += 1

        return saved_count