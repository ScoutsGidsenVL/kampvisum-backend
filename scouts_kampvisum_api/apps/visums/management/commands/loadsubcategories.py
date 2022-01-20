import logging, os, json
from pathlib import Path

from django.conf import settings
from django.core.management import call_command
from django.core.management.base import BaseCommand


logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = "Loads the categories from visum_categories.json"
    exception = False

    BASE_PATH = "apps/visums/fixtures"
    FIXTURE = "visum_sub_categories.json"
    TMP_FIXTURE = "{}_{}".format("adjusted", FIXTURE)

    def handle(self, *args, **kwargs):
        parent_path = Path(settings.BASE_DIR)

        data_path = "{}/{}".format(self.BASE_PATH, self.FIXTURE)
        path = os.path.join(parent_path, data_path)

        tmp_data_path = "{}/{}".format(self.BASE_PATH, self.TMP_FIXTURE)
        tmp_path = os.path.join(parent_path, tmp_data_path)

        logger.debug("Loading sub-categories from %s", path)

        previous_category = None
        previous_index = -1
        with open(path) as f:
            data = json.load(f)

            for model in data:
                category = model.get("fields")["category"]
                if previous_category is None:
                    previous_category = category

                if previous_category == category:
                    previous_index = previous_index + 1
                else:
                    previous_category = category
                    previous_index = 0
                model.get("fields")["index"] = previous_index

                logger.debug("MODEL DATA: %s", model)

            with open(tmp_path, "w") as o:
                json.dump(data, o)

        call_command("loaddata", tmp_path)

        os.remove(tmp_path)