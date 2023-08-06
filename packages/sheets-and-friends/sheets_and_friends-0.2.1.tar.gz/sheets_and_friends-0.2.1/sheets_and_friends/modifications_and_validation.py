import click
import click_log
import glom.core as gc
import logging
import pandas as pd
import yaml
from glom import glom, Assign
from linkml_runtime.dumpers import yaml_dumper
from linkml_runtime.linkml_model import SlotDefinition
from linkml_runtime.utils.schemaview import SchemaView
from pprint import pformat
from ruamel.yaml import YAML

# from typing import List, Optional, Dict, Any

logger = logging.getLogger(__name__)
click_log.basic_config(logger)


@click.command()
@click_log.simple_verbosity_option(logger)
@click.option("--yaml_input", type=click.Path(exists=True), required=True)
@click.option("--modifications_config_tsv", type=click.Path(exists=True), required=True)
@click.option("--validation_config_tsv", type=click.Path(exists=True), required=True)
@click.option("--yaml_output", type=click.Path(), required=True)
def modifications_and_validation(yaml_input: str, modifications_config_tsv: str, validation_config_tsv: str,
                                 yaml_output: str):
    """
    :param yaml_input:
    :param config_tsv:
    :param yaml_output:
    :return:
    """

    # todo be defensive
    # parameterize?

    meta_view = SchemaView("https://w3id.org/linkml/meta")

    # yaml = YAML()
    # with open('src/schema/nmdc.yaml') as f:
    #     schema_dict = yaml.load(f)

    with open(yaml_input, 'r') as stream:
        try:
            schema_dict = yaml.safe_load(stream)
        except yaml.YAMLError as e:
            logger.warning(e)

    mod_rule_frame = pd.read_csv(modifications_config_tsv, sep="\t")
    mod_rule_frame['class'] = mod_rule_frame['class'].str.split("|")
    mod_rule_frame = mod_rule_frame.explode('class')
    mod_rule_lod = mod_rule_frame.to_dict(orient='records')

    # todo break out overwrites first
    for i in mod_rule_lod:

        base_path = f"classes.{i['class']}.slot_usage.{i['slot']}"

        class_query = f"classes.{i['class']}"
        class_results_dict = glom(schema_dict, class_query)
        if "slot_usage" not in class_results_dict:
            logger.warning(f"slot_usage missing from {i['class']}")
            add_usage_path = f"classes.{i['class']}.slot_usage"
            # logger.warning(f"{add_usage_path = }")
            add_usage_dict = {"placeholder": {"name": "placeholder"}}
            # logger.warning(f"{add_usage_dict = }")
            glom(schema_dict, Assign(add_usage_path, add_usage_dict))
            logger.warning(pformat(schema_dict['classes'][i['class']]['slot_usage']))
        else:
            logger.warning(f"slot_usage already present in {i['class']}")
            slot_usage = schema_dict['classes'][i['class']]['slot_usage']
            if len(slot_usage.keys()) > 1 and "placeholder" in slot_usage.keys():
                del slot_usage['placeholder']

        usage_query = f"classes.{i['class']}.slot_usage"
        usage_dict = glom(schema_dict, usage_query)
        if i['slot'] not in usage_dict:
            logger.warning(f"Adding {i['slot']} to {i['class']}'s slot_usage")
            add_slot_path = f"classes.{i['class']}.slot_usage.{i['slot']}"
            # add_slot_dict = {"name": {i['slot']}}
            add_slot_dict = {"name": f"{i['slot']}"}
            glom(schema_dict, Assign(add_slot_path, add_slot_dict))
            logger.warning(pformat(schema_dict['classes'][i['class']]['slot_usage'][i['slot']]))
        else:
            logger.warning(f"{i['slot']} already present in {i['class']}'s slot_usage")

        try:
            logger.info(f"{i['slot']} {i['action']} {i['target']} {i['value']}")
            slot_usage_extract = glom(schema_dict, base_path)

            if i['action'] == "add_attribute" and i['target'] != "" and i['target'] is not None:
                # todo abort if slot is not multivalued
                #   alert use that value is being split on pipes
                cv_path = i['target']
                values_list = i['value'].split("|")
                values_list = [x.strip() for x in values_list]
                target_already_present = cv_path in slot_usage_extract

                if target_already_present:
                    current_value = glom(slot_usage_extract, cv_path)
                    target_is_list = type(current_value) == list
                    if target_is_list:
                        augmented_list = current_value + values_list
                    else:
                        augmented_list = [current_value] + values_list
                else:
                    augmented_list = values_list
                glom(schema_dict, Assign(f"{base_path}.{i['target']}", augmented_list))

            elif i['action'] == "add_example" and i['target'] == "examples":
                logger.warning("overwrite_examples")
                cv_path = i['target']
                examples_list = i['value'].split("|")
                examples_list = [x.strip() for x in examples_list]
                assembled_list = []
                for example_item in examples_list:
                    assembled_list.append({'value': example_item})
                logger.warning(f"assembled_list: {assembled_list}")
                target_already_present = cv_path in slot_usage_extract
                if target_already_present:
                    current_value = glom(slot_usage_extract, cv_path)
                    target_is_list = type(current_value) == list
                    if target_is_list:
                        logger.warning(f"a list of examples is already present: {current_value}")
                        augmented_list = current_value + assembled_list
                        logger.warning(f"augmented_list: {augmented_list}")

                    else:
                        logger.warning(f"a scalar example is already present: {current_value}")
                        augmented_list = [current_value] + assembled_list
                        logger.warning(f"augmented_list: {augmented_list}")

                else:
                    augmented_list = assembled_list
                glom(schema_dict, Assign(f"{base_path}.{i['target']}", augmented_list))

            elif i['action'] == "overwrite_examples" and i['target'] == "examples":
                logger.warning("overwrite_examples")
                examples_list = i['value'].split("|")
                examples_list = [x.strip() for x in examples_list]
                assembled_list = []
                for example_item in examples_list:
                    assembled_list.append({'value': example_item})
                logger.warning(f"assembled_list: {assembled_list}")
                glom(schema_dict, Assign(f"{base_path}.{i['target']}", assembled_list))

            elif i['action'] == "replace_annotation" and i['target'] != "" and i['target'] is not None:
                logger.warning("replace_annotation")
                if "annotations" in slot_usage_extract:
                    logger.warning("annotations already present")
                    update_path = f"annotations.{i['target']}"
                    logger.warning(f"base_path: {base_path}")
                    logger.warning(f"update_path: {update_path}")
                    logger.warning(f"value: {i['value']}")
                    glom(schema_dict, Assign(f"{base_path}.annotations.{i['target']}", i['value']))
                else:
                    logger.warning("annotations not present")
                    update_path = f"annotations"
                    logger.warning(f"base_path: {base_path}")
                    logger.warning(f"update_path: {update_path}")
                    logger.warning(f"target: {i['target']}")
                    logger.warning(f"value: {i['value']}")
                    glom(schema_dict, Assign(f"{base_path}.{i['target']}", {i['target']: i['value']}))

            elif i['action'] == "replace_attribute" and i['target'] != "" and i['target'] is not None:
                logger.warning("replace_attribute")
                update_path = i['target']
                logger.warning(f"update_path: {update_path}")
                fiddled_value = i['value']
                logger.warning(f"fiddled_value: {fiddled_value}")
                from_meta = meta_view.get_slot(i['target'])
                fm_range = from_meta.range
                if fm_range == "boolean":
                    fiddled_value = bool(i['value'])
                glom(schema_dict, Assign(f"{base_path}.{i['target']}", fiddled_value))
                # assign(obj=slot_usage_extract, path=update_path, val=fiddled_value)

            else:
                logger.warning(f"no action for {i['action']}")

        # todo refactor

        except gc.PathAccessError as e:
            logger.warning(e)

    # ============== apply validation rules ============== #
    # ==================================================== #

    # fetch validation_converter sheet as pd df
    validation_rules_df = pd.read_csv(validation_config_tsv, sep="\t", header=0)

    # logger.warning(f"validation_rules_df: {validation_rules_df}")

    # loop through all induced slots associated with all classes
    # from the schema_dict and modify slots in place

    for class_name, class_defn in schema_dict["classes"].items():

        # check if the slot_usage key exists in each class definition
        if "slot_usage" in class_defn and len(class_defn["slot_usage"]) > 0:

            # loop over slot_usage items from each of the classes
            for _, slot_defn in schema_dict["classes"][class_name][
                "slot_usage"
            ].items():

                # when slot range in filtered list from validation_converter
                if "range" in slot_defn and (
                        slot_defn["range"]
                        in validation_rules_df[
                            validation_rules_df["to_type"] == "DH pattern regex"
                        ]["from_val"].to_list()
                ):
                    slot_defn["pattern"] = validation_rules_df[
                        validation_rules_df["from_val"] == slot_defn["range"]
                        ]["to_val"].to_list()[0]

                # when slot string_serialization in filtered list
                # from validation_converter
                if "string_serialization" in slot_defn and (
                        slot_defn["string_serialization"]
                        in validation_rules_df[
                            validation_rules_df["to_type"] == "DH pattern regex"
                        ]["from_val"].to_list()
                ):
                    slot_defn["pattern"] = validation_rules_df[
                        validation_rules_df["from_val"]
                        == slot_defn["string_serialization"]
                        ]["to_val"].to_list()[0]

    with open(yaml_output, 'w') as f:
        yaml.dump(schema_dict, f, default_flow_style=False, sort_keys=False)


if __name__ == '__main__':
    modifications_and_validation()
