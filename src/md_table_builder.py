class MarkdownTableBuilder:
    def __init__(self):
        self.headers = ['❌Removed❌', '🦠IntroducedBy🦠']
        self.rows = []

    def add_row(self, row):
        self.rows.append(row)

    def __str__(self):
        num_columns = len(self.headers)
        column_widths = [max(len(str(row[i])) for row in self.rows + [self.headers]) for i in range(num_columns)]
        header_separator = '|'.join(['-' * width for width in column_widths])
        header = '|'.join([str(header).ljust(column_widths[i]) for i, header in enumerate(self.headers)])
        rows = '\n'.join(['|'.join([str(row[i]).ljust(column_widths[i]) for i in range(num_columns)]) for row in self.rows])
        return f'{header}\n{header_separator}\n{rows}'