"""Thin step definitions: they only call ParkEase and compare values.

There is NO fee arithmetic here - every expected number comes from the feature file.
"""
from behave import given, when, then

import parameter_types  # noqa: F401  (registers Amount, Duration, Kind, ...)


def assert_equal(what, expected, actual):
    """Fail with a message that names the thing checked, expected and actual values."""
    if isinstance(expected, int) and not isinstance(expected, bool):
        expected, actual = f"Rs. {expected:,}", f"Rs. {actual:,}"
    assert expected == actual, f"{what}: expected {expected!r} but was {actual!r}"


# ---------------------------------------------------------------- Given
@given("{driver} is logged in to ParkEase")
def step_logged_in(context, driver):
    context.app.login(driver)


@given('{pos:Possessive} {electric:Kind} vehicle "{plate}" is linked to {pos2:Possessive} account')
def step_link_vehicle(context, pos, electric, plate, pos2):
    context.plate = plate
    context.app.link_vehicle(plate, electric)


@given("{pos:Possessive} wallet balance is {amount:Amount}")
def step_wallet(context, pos, amount):
    context.app.set_wallet(amount)


@given("{pos:Possessive} vehicle entered the plaza {duration:Duration} ago")
def step_entry_time(context, pos, duration):
    context.parked = duration


# ----------------------------------------------------------------- When
@when("{pos:Possessive} vehicle reaches the exit gate")
def step_exit(context, pos):
    context.result = context.app.exit(context.plate, context.parked.minutes,
                                      context.parked.seconds)


# ----------------------------------------------------------------- Then
@then('{sub:Subject} sees the message "{message}"')
def step_message(context, sub, message):
    assert_equal("message", message, context.result.message)


@then("the parking fee is {amount:Amount}")
def step_parking_fee(context, amount):
    assert_equal("parking fee (R3/R4)", amount, context.result.parking_fee)


@then("the EV discount is {amount:Amount}")
def step_ev_discount(context, amount):
    assert_equal("EV discount (R5)", amount, context.result.ev_discount)


@then("the service charge is {amount:Amount}")
def step_service_charge(context, amount):
    assert_equal("service charge (R6)", amount, context.result.service_charge)


@then("the total paid is {amount:Amount}")
def step_total_paid(context, amount):
    assert_equal("total paid (R5/R6/R7)", amount, context.result.total_paid)


@then("{pos:Possessive} wallet balance is {amount:Amount}")
def step_wallet_balance(context, pos, amount):
    assert_equal("wallet balance (R7/R8)", amount, context.app.wallet_balance())


@then("the gate is open")
def step_gate_open(context):
    assert_equal("gate open", True, context.result.gate_open)


@then("the gate stays closed")
def step_gate_closed(context):
    assert_equal("gate open", False, context.result.gate_open)
