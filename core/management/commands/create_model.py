from django.core.management.base import BaseCommand
import os
import json


class Command(BaseCommand):
    help = "Creates a new model directory and files"

    def add_arguments(self, parser):
        parser.add_argument("model_name", type=str, help="Name of the model to create")
        parser.add_argument("--fields", nargs="+", help="Fields for the model")

    def handle(self, *args, **options):
        model_name = options["model_name"]
        fields = options["fields"]
        model_dir = f"models/{model_name}"


        if os.path.exists(model_dir):
            print(f"Error: Model directory '{model_dir}' already exists.")
            return

        os.makedirs(model_dir)

        # Write model JSON file
        model_definition = {"fields": {}, "required_fields": []}
        if fields:
            for field in fields:
                if ":" in field:
                    field_name, field_type = field.split(":")
                    model_definition["fields"][field_name] = field_type
                else:
                    model_definition["fields"][field] = "TextField"  # Default field type
        with open(f"{model_dir}/{model_name}.json", "w") as f:
            json.dump(model_definition, f, indent=4)

        with open(f"{model_dir}/{model_name}.py", "w") as f:
            f.write(f"from core.models import Document\n\n")
            f.write(f"class {model_name.capitalize()}(Document):\n")
            f.write("    pass\n")

        print(f"Model '{model_name}' created successfully!")
