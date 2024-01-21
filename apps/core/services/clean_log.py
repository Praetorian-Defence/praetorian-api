from apps.core.models import Log


class CleanLogService:
    def __init__(self, log: Log) -> None:
        self._log = log
        self._data = log.base_log['log']

        self._recorded_data = []

    @classmethod
    def create_from_request(cls, log: Log) -> 'CleanLogService':
        return CleanLogService(log)

    def clean(self):
        next_item = False

        to_change_next_item = False
        consider_next_item = 'input'

        accumulated_data = ""
        last_type = None
        prompt = None
        timestamp = None
        for i in range(len(self._data) - 1):
            if next_item:
                next_item = False
                continue

            # set every iteration
            if to_change_next_item:
                self._data[i]['type'] = consider_next_item

            next_item = self._skip_next_item(self._data, i)
            to_change_next_item, consider_next_item = self._change_next_item(self._data, i)

            # because we check only \t at the moment
            if to_change_next_item:
                continue

            item = self._data[i]
            sanitized_data = self._sanitize_string(item['data'])  # Sanitize the data here

            # Initialize the last_type if it's the first iteration
            if last_type is None:
                last_type = item['type']
                timestamp = item['timestamp']

            if last_type == item['type']:
                accumulated_data = self._check_data(sanitized_data, accumulated_data)
                prompt = item.get('prompt', "Input: " if last_type == 'input' else 'Output: ').replace('[?2004h', '')
            else:
                self._print_data(accumulated_data, last_type, prompt, timestamp)
                accumulated_data = self._check_data(sanitized_data)
                last_type = item['type']
                timestamp = item['timestamp']

            # If this is the last item, print it
            if i == len(self._data) - 1:
                self._print_data(accumulated_data, last_type, prompt, timestamp)

        self._log.cleaned_log = {'log': self._recorded_data}
        self._log.base_log = None  # can not store ascii values like /u0000
        self._log.save()

    @staticmethod
    def _check_data(sanitized_data, accumulated_data=''):
        if bytes(sanitized_data, 'utf-8') == b'\x7f':
            accumulated_data = accumulated_data[:-1]
        else:
            sanitized_data = sanitized_data.replace('[?2004l', '')
            sanitized_data = sanitized_data.replace('[?2004h', '')
            sanitized_data = sanitized_data.replace('\b', '\r')

            sanitized_data = sanitized_data.replace('\u001b[A', '<KeyUp>')
            sanitized_data = sanitized_data.replace('\u001bOA', '<KeyUp>')

            sanitized_data = sanitized_data.replace('\u001bOB', '<KeyDown>')
            sanitized_data = sanitized_data.replace('\u001b[B', '<KeyDown>')

            sanitized_data = sanitized_data.replace('\u001bOC', '<KeyRight>')
            sanitized_data = sanitized_data.replace('\u001b[C', '<KeyRight>')

            sanitized_data = sanitized_data.replace('\u001bOD', '<KeyLeft>')
            sanitized_data = sanitized_data.replace('\u001b[D', '<KeyLeft>')

            sanitized_data = sanitized_data.replace('\u001b[K', '<ESC>')
            sanitized_data = sanitized_data.replace('\u001b', '<ESC>')

            sanitized_data = sanitized_data.replace('\u001B[K', '<RemovedBeforeThis>')
            sanitized_data = sanitized_data.replace('\x1B[K', '<RemovedBeforeThis>')
            sanitized_data = sanitized_data.replace('\u0007', '<RemovedBeforeThis>')

            accumulated_data += sanitized_data

    # "\x1B[K" '\u0007' overwrites last character in full-width line https://github.com/ninja-build/ninja/issues/2209

        return accumulated_data

    @staticmethod
    def _remove_before_and_substring(main_string, to_find):
        """
        Remove everything before and including the substring
        """

        output = []
        i = 0
        n = len(main_string)
        m = len(to_find)

        while i < n:
            if main_string[i:i + m] == to_find:
                output.clear()
                i += m  # Skip the length of to_find
            else:
                output.append(main_string[i])
                i += 1

        return ''.join(output)

    @staticmethod
    def _remove_prefix_and_substring(main_string, to_find):
        """
        Remove the character immediately before the substring
        """
        output = []
        i = 0
        n = len(main_string)
        m = len(to_find)

        while i < n:
            if i > 0 and main_string[i:i + m] == to_find:
                output.pop()
                i += m  # Skip the length of to_find
            else:
                output.append(main_string[i])
                i += 1

        return ''.join(output)

    @staticmethod
    def _replace_with_prefix(main_string, to_find, prefix_char):
        output = []
        i = 0
        n = len(main_string)
        m = len(to_find)

        while i < n:
            # If the next m characters match "to_find"
            if main_string[i:i + m] == to_find:
                output.append(prefix_char + to_find)
                i += m  # Skip the length of to_find
            else:
                output.append(main_string[i])
                i += 1

        return ''.join(output)

    def _print_data(self, data, data_type, prompt, timestamp):
        if '@' in prompt:
            self._recorded_data.append(
                {
                    'timestamp': timestamp,
                    'data': data,
                    'type': data_type,
                    'prompt': prompt
                }
            )
        else:
            self._recorded_data.append(
                {
                    'timestamp': timestamp,
                    'data': data,
                    'type': data_type,
                    'prompt': prompt
                }
            )

    def _skip_next_item(self, data: dict, i: int) -> bool:
        result = False
        if self._sanitize_string(data[i]['data']) == self._sanitize_string(data[i + 1]['data']):
            result = True
        elif bytes(self._sanitize_string(data[i]['data']), 'utf-8') == b'\x7f':
            result = True
        return result

    def _change_next_item(self, data: dict, i: int):
        result = False
        kind = 'output'
        if self._sanitize_string(data[i]['data']) == '\t':
            result = True
            kind = data[i]['type']

        return result, kind

    @staticmethod
    def _sanitize_string(s):
        """Remove null characters from a string."""
        """Removes null bytes and other characters that might cause issues with curses"""
        return s.replace('\x00', '')
