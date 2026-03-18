class Interpreter:
    def __init__(self, parsed):
        self.song = parsed["song"]
        self.structure = parsed["structure"]
        self.sections = parsed["sections"]

    def run(self):
        if not self.song:
            raise RuntimeError("LyricScript Error: No song name defined")

        print(f"{self.song}\n")
        print("=" * 40)

        if self.structure:
            for section_name in self.structure:
                self.print_section(section_name)
        else:
            for section_name in self.sections:
                self.print_section(section_name)
        
        print("\n" + "=" * 40)

    def print_section(self, name):
        if name not in self.sections:
            raise RuntimeError(f"LyricScript Error: Section '{name}' used in structure but never defined")

        print(f"\n  [{name.upper()}]")
        for line in self.sections[name]["lines"]:
            print(f"    {line}")