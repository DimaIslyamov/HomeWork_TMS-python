import csv
import io

from rest_framework.renderers import BaseRenderer


class CSVRenderer(BaseRenderer):
    media_type = "text/csv"
    format = "csv"

    def render(self, data, accepted_media_type=None, renderer_context=None):
        output = io.StringIO()
        writer = csv.writer(output)

        writer.writerow(["id", "title", "starts_at"])

        for event in data:
            writer.writerow(
                [
                    event["id"],
                    event["title"],
                    event["starts_at"],
                ]
            )

        return output.getvalue()