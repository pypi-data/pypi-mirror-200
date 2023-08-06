# -*- coding: utf-8 -*-
# Copyright © 2023 Contrast Security, Inc.
# See https://www.contrastsecurity.com/enduser-terms-0317a for more details.
import contrast

import xml.etree.ElementTree
from contrast.utils.loggers.logger import security_log_msg
from contrast.utils.string_utils import ensure_string

from contrast.api.user_input import DocumentType, InputType
from contrast.agent.settings import Settings
from contrast.agent import agent_lib
from contrast.extern import structlog as logging
from contrast.utils.exceptions.security_exception import SecurityException

logger = logging.getLogger("contrast")


def _get_enabled_rules(rules_list=None):
    """
    This converts our list of enabled rules to an integer value as the bitmask that the Agent Library expects.
    """
    rules = 0
    settings = Settings()
    if rules_list is None:
        rules_list = settings.protect_rules.items()

    for rule_tuple in rules_list:
        if (
            rule_tuple
            and rule_tuple[1]
            and rule_tuple[1].enabled
            and rule_tuple[1].RULE_NAME in agent_lib.modules.CONSTANTS.RuleType
        ):
            rules |= agent_lib.modules.CONSTANTS.RuleType[rule_tuple[1].RULE_NAME]
    return rules


def get_input_analysis(rules_list=None):

    request_ctx = contrast.CS__CONTEXT_TRACKER.current()

    if request_ctx is None:
        return

    exclusions = Settings().exclusions

    rules = _get_enabled_rules(rules_list)

    # Prefer worth watching is set to True at the start of a request and False at request end.
    # Worth watching means to stop analysis when we hit the worth watching threshold, meaning we end early during the
    # request for performance and run the full analysis for attack detection after the request for accuracy.
    worth_watching = request_ctx.response is None

    # Input analysis for all the input_tracing.InputType enum values
    _evaluate_headers(request_ctx, rules, worth_watching, exclusions)
    _evaluate_cookies(request_ctx, rules, worth_watching, exclusions)
    _evaluate_body(request_ctx, rules, worth_watching, exclusions)
    _call_check_method_tampering(request_ctx, worth_watching)
    _evaluate_query_string_params(request_ctx, rules, worth_watching, exclusions)
    _call_agent_lib_evaluate_input(
        agent_lib.modules.CONSTANTS.InputType.get("UriPath"),
        request_ctx.request.path,
        rules,
        worth_watching,
        request_ctx,
    )
    _evaluate_path_params(request_ctx, rules, worth_watching, exclusions)
    _evaluate_multipart_request(request_ctx, rules, worth_watching)


def _evaluate_headers(request_ctx, rules, worth_watching, exclusions):
    for header_name, header_value in request_ctx.request.headers.items():
        if "cookie" in header_name.lower() or check_param_input_exclusions(
            exclusions, "HEADER", header_name
        ):
            continue

        input_analysis = agent_lib.evaluate_header_input(
            header_name, header_value, rules, worth_watching
        )

        if input_analysis:
            request_ctx.user_input_analysis.extend(input_analysis)
            # Report and block attack if necessary
            _report_and_block_by_rule_list(
                input_analysis,
                ["bot-blocker", "reflected-xss", "unsafe-file-upload"],
                request_ctx,
            )


def _evaluate_cookies(request_ctx, rules, worth_watching, exclusions):
    for cookie_name, cookie_value in request_ctx.request.cookies.items():
        if check_param_input_exclusions(exclusions, "COOKIE", cookie_name):
            continue

        _call_agent_lib_evaluate_input(
            agent_lib.modules.CONSTANTS.InputType.get("CookieName"),
            cookie_name,
            rules,
            worth_watching,
            request_ctx,
        )
        _call_agent_lib_evaluate_input(
            agent_lib.modules.CONSTANTS.InputType.get("CookieValue"),
            cookie_value,
            rules,
            worth_watching,
            request_ctx,
        )


def _evaluate_body(request_ctx, rules, worth_watching, exclusions):
    if check_url_input_exclusion(exclusions, "BODY", request_ctx.request.url):
        return

    body_type = request_ctx.request._get_document_type()
    if body_type == DocumentType.JSON:
        _evaluate_body_json(
            request_ctx, rules, worth_watching, request_ctx.request.json
        )
    elif body_type == DocumentType.XML:
        data = xml.etree.ElementTree.fromstring(request_ctx.request.body)
        text_list = [element.text for element in data]

        for text in text_list:
            if not str(text).startswith("\n"):
                _call_agent_lib_evaluate_input(
                    agent_lib.modules.CONSTANTS.InputType.get("XmlValue"),
                    str(text),
                    rules,
                    worth_watching,
                    request_ctx,
                )


def _evaluate_body_json(request_ctx, rules, worth_watching, body):
    # Using recursion for now to get all the json values and keys and pass them
    # through agent_lib until agent_lib implements parsing of the body for python
    if isinstance(body, dict):
        for key, value in body.items():
            _call_agent_lib_evaluate_input(
                agent_lib.modules.CONSTANTS.InputType.get("JsonKey"),
                key,
                rules,
                worth_watching,
                request_ctx,
            )
            # This check is to skip a level in the recursion, just a minor optimization
            if isinstance(value, (dict, list)):
                _evaluate_body_json(request_ctx, rules, worth_watching, value)
            else:
                _call_agent_lib_evaluate_input(
                    agent_lib.modules.CONSTANTS.InputType.get("JsonValue"),
                    value,
                    rules,
                    worth_watching,
                    request_ctx,
                )
    elif isinstance(body, list):
        for item in body:
            if isinstance(item, (dict, list)):
                _evaluate_body_json(request_ctx, rules, worth_watching, item)
            else:
                _call_agent_lib_evaluate_input(
                    agent_lib.modules.CONSTANTS.InputType.get("JsonValue"),
                    item,
                    rules,
                    worth_watching,
                    request_ctx,
                )
    else:
        # In theory we shouldn't enter this block but I would like to have it
        # just in case we get a value instead of dict
        _call_agent_lib_evaluate_input(
            agent_lib.modules.CONSTANTS.InputType.get("JsonValue"),
            body,
            rules,
            worth_watching,
            request_ctx,
        )


def _evaluate_query_string_params(request_ctx, rules, worth_watching, exclusions):
    """
    Calling agent_lib evaluate_input for all query_string_params for example:
    https://test.com/users?userId=1234&userName=testUser keys: userId, userName values: 1234, testUser
    """
    for param_key, param_value in request_ctx.request.params.items():
        if not isinstance(param_value, str) or check_url_input_exclusion(
            exclusions, "QUERYSTRING", request_ctx.request.url
        ):
            continue

        _call_agent_lib_evaluate_input(
            agent_lib.modules.CONSTANTS.InputType.get("ParameterKey"),
            param_key,
            rules,
            worth_watching,
            request_ctx,
            True,
        )
        _call_agent_lib_evaluate_input(
            agent_lib.modules.CONSTANTS.InputType.get("ParameterValue"),
            param_value,
            rules,
            worth_watching,
            request_ctx,
            True,
        )


def _evaluate_path_params(request_ctx, rules, worth_watching, exclusions):
    """
    Calling agent_lib evaluate_input for all path params for example:
    https://test.com/users/1234 the url parameter is 1234
    """
    for param in request_ctx.request.get_url_parameters():
        if check_param_input_exclusions(exclusions, "PARAMETER", param):
            continue

        _call_agent_lib_evaluate_input(
            agent_lib.modules.CONSTANTS.InputType.get("UrlParameter"),
            param,
            rules,
            worth_watching,
            request_ctx,
        )


def _evaluate_multipart_request(request_ctx, rules, worth_watching):
    """
    This is refering to Content-Type: multipart/form-data and checking the file_name for every
    multipart request if there is none it checks the name
    """
    for key, value in request_ctx.request.get_multipart_headers().items():
        if value is None and key is None:
            continue

        multipart_name = value if value is not None else key
        _call_agent_lib_evaluate_input(
            agent_lib.modules.CONSTANTS.InputType.get("MultipartName"),
            multipart_name,
            rules,
            worth_watching,
            request_ctx,
        )


def _call_check_method_tampering(request_ctx, worth_watching):
    input_analysis_value = agent_lib.check_method_tampering(
        request_ctx.request.method, worth_watching
    )

    if input_analysis_value:
        request_ctx.user_input_analysis.extend(input_analysis_value)
        _report_and_block_by_rule_list(
            input_analysis_value, ["reflected-xss", "unsafe-file-upload"], request_ctx
        )


def _call_agent_lib_evaluate_input(
    input_type, input_value, rule_set, worth_watching, request_ctx, is_querystring=False
):
    input_analysis_value = agent_lib.evaluate_input_by_type(
        input_type, input_value, rule_set, worth_watching
    )

    if input_analysis_value:
        # This check is specific for querystring because agent-lib doesn't have a way to distinguish
        # url parameter and querystring and TS is expecting it as QUERYSTRING in attack samples
        if is_querystring:
            for input_analysis in input_analysis_value:
                input_analysis.input_type = InputType.QUERYSTRING

        request_ctx.user_input_analysis.extend(input_analysis_value)
        _report_and_block_by_rule_list(
            input_analysis_value, ["reflected-xss", "unsafe-file-upload"], request_ctx
        )


def _report_and_block_by_rule_list(input_analysis, rule_names, context):
    """
    Checks a list of rules and reports if it finds a score(int with value 0-100 indicating percentage
    of certainty of attack) higher than 90 and blocks if the agent is configured in block mode.
    :param input_analysis: list the response from agent_lib
    :param rule_names: list of names of rules that need to be checkd and reported and blocked
    :return: doesn't return anything as it just needs to report and block if needed
    """
    settings = Settings()
    for input_row in input_analysis:
        for rule_name in rule_names:
            rule = settings.protect_rules.get(rule_name)
            # Bot blocker rule is valid only when the input_row.name/header name is "user-agent"
            bot_blocker_header_check = (
                lambda a, rule_name_val: a.lower() == "user-agent"
                if rule_name_val == "bot-blocker"
                else True
            )

            if rule_name == input_row.rule_id:
                attack = rule.build_attack_with_match(input_row.value, input_row, None)
                context.attacks.append(attack)

            if (
                bot_blocker_header_check(input_row.key, rule_name)
                and input_row.score >= 90
                and rule is not None
                and rule_name == input_row.rule_id
            ):
                logger.debug(
                    f"Input analysis found a value '{input_row.value}' that violated {rule_name} rule!"
                )

                if input_row.rule_id == rule.RULE_NAME and rule.is_blocked():
                    rule_message = f"{rule_name} - {ensure_string(input_row.value, errors='replace')}"

                    msg = f"The {input_row.input_type.name} {input_row.value} had a value that successfully exploited {ensure_string(rule_message, errors='replace')}"

                    security_log_msg(msg, Settings().app_name, rule_name, "EXPLOITED")

                    raise SecurityException(
                        rule=None,
                        message=f"Rule {rule_name} threw a security exception",
                    )


def check_url_input_exclusion(exclusions, input_type, param):
    if not exclusions:
        return False

    return exclusions.evaluate_input_exclusions_url(
        exclusions, input_type, param, "defend"
    )


def check_param_input_exclusions(exclusions, input_type, param):
    if not exclusions:
        return False

    return exclusions.evaluate_input_exclusions(exclusions, input_type, param, "defend")
