class ArgParser:
    """Get input argument and validate that it exists"""

    def __init__(self) -> None:
        parser = argparse.ArgumentParser(description="Connect Z")
        parser.add_argument(
            "inputfilename", type=str, nargs="*", help="Enter file name"
        )
        self.args = parser.parse_args()

    def get_file(self) -> Path:
        """
        Get file from inputfilename argument.
        It makes sure that the file also exists.
        """
        input_file = self._validate_inputfilename()
        return Path(input_file)

    def _validate_inputfilename(self) -> None:
        """
        Validate that one inputfilename argument is specified.
        It stops the program otherwise.
        """
        input_file, *bad_params = self.args.inputfilename
        if input_file is None or bad_params:
            sys.exit("connectz.py: Provide one input file")
        else:
            return input_file

def sliding_window(iterable: Optional[int], size: int) -> Optional[int]:
    """
    Applies a sliding window of a given size to an iterable
    and returns (every) smaller list that can fit into an iterable"""
    iters = tee(iterable, size)
    for i in range(1, size):
        for each in iters[i:]:
            next(each)
    return zip(*iters)