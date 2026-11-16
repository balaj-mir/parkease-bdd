"""Custom parameter types for the ParkEase steps (register_type in behave)."""
from collections import namedtuple

import parse
from behave import register_type

Duration = namedtuple("Duration", "minutes seconds")

_UNIT_SECONDS = {"hour": 3600, "minute": 60, "second": 1}


@parse.with_pattern(r"Rs\. [\d,]+")
def parse_amount(text):
    """'Rs. 1,000' -> 1000   (strips the 'Rs. ' prefix and the thousands commas)."""
    return int(text[len("Rs. "):].replace(",", ""))


@parse.with_pattern(r"\d+ (?:hours?|minutes?|seconds?)(?: \d+ (?:hours?|minutes?|seconds?))*")
def parse_duration(text):
    """'3 hours 40 minutes' -> Duration(minutes=220, seconds=0)."""
    tokens = text.split()
    total = sum(int(n) * _UNIT_SECONDS[unit.rstrip("s")]
                for n, unit in zip(tokens[0::2], tokens[1::2]))
    return Duration(minutes=total // 60, seconds=total % 60)


@parse.with_pattern(r"electric|petrol")
def parse_kind(text):
    return text == "electric"            # True when the vehicle is an EV


@parse.with_pattern(r"her|his|their")
def parse_possessive(text):
    return text


@parse.with_pattern(r"she|he|they")
def parse_subject(text):
    return text


register_type(Amount=parse_amount, Duration=parse_duration, Kind=parse_kind,
              Possessive=parse_possessive, Subject=parse_subject)
