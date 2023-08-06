import click
import click_log
import glom.core as gc
import logging
import pandas as pd
import yaml
from glom import glom, Assign
from linkml_runtime.utils.schemaview import SchemaView
from pprint import pformat

pd.set_option('display.max_columns', None)

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
            logger.info(f"slot_usage missing from {i['class']}")
            add_usage_path = f"classes.{i['class']}.slot_usage"
            add_usage_dict = {"placeholder": {"name": "placeholder"}}
            glom(schema_dict, Assign(add_usage_path, add_usage_dict))
            logger.info(pformat(schema_dict['classes'][i['class']]['slot_usage']))
        else:
            logger.info(f"slot_usage already present in {i['class']}")
            slot_usage = schema_dict['classes'][i['class']]['slot_usage']
            if len(slot_usage.keys()) > 1 and "placeholder" in slot_usage.keys():
                del slot_usage['placeholder']

        usage_query = f"classes.{i['class']}.slot_usage"
        usage_dict = glom(schema_dict, usage_query)
        if i['slot'] not in usage_dict:
            logger.info(f"Adding {i['slot']} to {i['class']}'s slot_usage")
            add_slot_path = f"classes.{i['class']}.slot_usage.{i['slot']}"
            add_slot_dict = {"name": f"{i['slot']}"}
            glom(schema_dict, Assign(add_slot_path, add_slot_dict))
            logger.info(pformat(schema_dict['classes'][i['class']]['slot_usage'][i['slot']]))
        else:
            logger.info(f"{i['slot']} already present in {i['class']}'s slot_usage")

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
                logger.info("overwrite_examples")
                cv_path = i['target']
                examples_list = i['value'].split("|")
                examples_list = [x.strip() for x in examples_list]
                assembled_list = []
                for example_item in examples_list:
                    assembled_list.append({'value': example_item})
                logger.info(f"assembled_list: {assembled_list}")
                target_already_present = cv_path in slot_usage_extract
                if target_already_present:
                    current_value = glom(slot_usage_extract, cv_path)
                    target_is_list = type(current_value) == list
                    if target_is_list:
                        logger.info(f"a list of examples is already present: {current_value}")
                        augmented_list = current_value + assembled_list
                        logger.info(f"augmented_list: {augmented_list}")

                    else:
                        logger.info(f"a scalar example is already present: {current_value}")
                        augmented_list = [current_value] + assembled_list
                        logger.info(f"augmented_list: {augmented_list}")

                else:
                    augmented_list = assembled_list
                glom(schema_dict, Assign(f"{base_path}.{i['target']}", augmented_list))

            elif i['action'] == "overwrite_examples" and i['target'] == "examples":
                logger.info("overwrite_examples")
                examples_list = i['value'].split("|")
                examples_list = [x.strip() for x in examples_list]
                assembled_list = []
                for example_item in examples_list:
                    assembled_list.append({'value': example_item})
                logger.info(f"assembled_list: {assembled_list}")
                glom(schema_dict, Assign(f"{base_path}.{i['target']}", assembled_list))

            elif i['action'] == "replace_annotation" and i['target'] != "" and i['target'] is not None:
                logger.info("replace_annotation")
                if "annotations" in slot_usage_extract:
                    logger.info("annotations already present")
                    update_path = f"annotations.{i['target']}"
                    logger.info(f"base_path: {base_path}")
                    logger.info(f"update_path: {update_path}")
                    logger.info(f"value: {i['value']}")
                    glom(schema_dict, Assign(f"{base_path}.annotations.{i['target']}", i['value']))
                else:
                    logger.info("annotations not present")
                    update_path = f"annotations"
                    logger.info(f"base_path: {base_path}")
                    logger.info(f"update_path: {update_path}")
                    logger.info(f"target: {i['target']}")
                    logger.info(f"value: {i['value']}")
                    glom(schema_dict, Assign(f"{base_path}.{i['target']}", {i['target']: i['value']}))

            elif i['action'] == "replace_attribute" and i['target'] != "" and i['target'] is not None:
                logger.info("replace_attribute")
                update_path = i['target']
                logger.info(f"update_path: {update_path}")
                fiddled_value = i['value']
                logger.info(f"fiddled_value: {fiddled_value}")
                from_meta = meta_view.get_slot(i['target'])
                fm_range = from_meta.range
                if fm_range == "boolean":
                    fiddled_value = bool(i['value'])
                glom(schema_dict, Assign(f"{base_path}.{i['target']}", fiddled_value))
            else:
                logger.info(f"no action for {i['action']}")

        # todo refactor

        except gc.PathAccessError as e:
            logger.warning(e)

    # ============== apply validation rules ============== #
    # ==================================================== #

    # fetch validation_converter sheet as pd df
    validation_rules_df = pd.read_csv(validation_config_tsv, sep="\t", header=0)

    # loop through all induced slots associated with all classes
    # from the schema_dict and modify slots in place

    logger.info(f"VALIDATION UPDATES")

    for class_name, class_defn in schema_dict["classes"].items():

        # check if the slot_usage key exists in each class definition
        if "slot_usage" in class_defn and len(class_defn["slot_usage"]) > 0:

            # loop over slot_usage items
            for slot_name, slot_defn in schema_dict["classes"][class_name][
                "slot_usage"
            ].items():
                if "range" in slot_defn:
                    replacement_ranges = validation_rules_df.loc[
                        (validation_rules_df['from_type'] == 'linkml range') &
                        (validation_rules_df['to_type'] == 'DH datatype') &
                        (validation_rules_df['from_val'] == slot_defn['range']), "to_val"
                    ]
                    if len(replacement_ranges) > 0:
                        logger.info(
                            f"class_name: {class_name}; slot_name: {slot_defn['name']}; range: {slot_defn['range']}")
                        logger.info(f"replacement_ranges #{len(replacement_ranges)}: {replacement_ranges.iloc[0]}")
                        slot_defn['range'] = replacement_ranges.iloc[0]
                    replacement_patterns = validation_rules_df.loc[
                        (validation_rules_df['from_type'] == 'linkml range') &
                        (validation_rules_df['to_type'] == 'DH pattern regex') &
                        (validation_rules_df['from_val'] == slot_defn['range']), "to_val"
                    ]
                    if len(replacement_patterns) > 0:
                        logger.info(
                            f"class_name: {class_name}; slot_name: {slot_defn['name']}; range: {slot_defn['range']}")
                        logger.info(
                            f"replacement_patterns #{len(replacement_patterns)}: {replacement_patterns.iloc[0]}")
                        slot_defn['pattern'] = replacement_patterns.iloc[0]

                if "string_serialization" in slot_defn:
                    logger.info(
                        f"class_name: {class_name}; slot_name: {slot_defn['name']}; string_serialization: {slot_defn['string_serialization']}"
                    )
                    replacement_ranges = validation_rules_df.loc[
                        (validation_rules_df['from_type'].isin(
                            ['linkml string_serialization', 'MIxS string serialization'])) &
                        (validation_rules_df['to_type'] == 'DH datatype') &
                        (validation_rules_df['from_val'] == slot_defn['string_serialization']), "to_val"
                    ]
                    if len(replacement_ranges) > 0:
                        logger.info(
                            f"class_name: {class_name}; slot_name: {slot_defn['name']}; string_serialization: {slot_defn['string_serialization']}")
                        logger.info(f"replacement_ranges #{len(replacement_ranges)}: {replacement_ranges.iloc[0]}")
                        slot_defn['range'] = replacement_ranges.iloc[0]
                    replacement_patterns = validation_rules_df.loc[
                        (validation_rules_df['from_type'].isin(
                            ['linkml string_serialization', 'MIxS string serialization'])) &
                        (validation_rules_df['to_type'] == 'DH pattern regex') &
                        (validation_rules_df['from_val'] == slot_defn['string_serialization']), "to_val"
                    ]
                    if len(replacement_patterns) > 0:
                        logger.info(
                            f"class_name: {class_name}; slot_name: {slot_defn['name']}; range: {slot_defn['range']}")
                        logger.info(
                            f"replacement_patterns #{len(replacement_patterns)}: {replacement_patterns.iloc[0]}")
                        slot_defn['pattern'] = replacement_patterns.iloc[0]

        else:
            logger.warning(f"no slot_usage for {class_name}")
    with open(yaml_output, 'w') as f:
        yaml.dump(schema_dict, f, default_flow_style=False, sort_keys=False)


if __name__ == '__main__':
    modifications_and_validation()
