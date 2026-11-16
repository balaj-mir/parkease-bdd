"""In-memory ParkEase model that applies business rules R1-R8.

All money is held as whole rupees (int). Time is passed as minutes + seconds.
"""
from dataclasses import dataclass

SUCCESS_MESSAGE = "Payment successful \u2013 gate opening"          # R8
INSUFFICIENT_MESSAGE = "Insufficient wallet balance"                # R7
LOGIN_REQUIRED_MESSAGE = "Please log in to pay by wallet"           # R1 (wording assumed)
NOT_LINKED_MESSAGE = "Vehicle is not linked to your account"        # R1 (wording assumed)


@dataclass
class ExitResult:
    message: str = ""
    parking_fee: int = 0        # fee after the cap, before the EV discount
    ev_discount: int = 0
    service_charge: int = 0
    total_payable: int = 0      # what the rules say the driver owes
    total_paid: int = 0         # what was actually deducted from the wallet
    gate_open: bool = False


class ParkEase:
    GRACE_SECONDS = 15 * 60     # R2: up to and including 15:00 is free
    FIRST_HOUR = 100            # R3
    EXTRA_HOUR = 60             # R3
    FEE_CAP = 800               # R4
    EV_DISCOUNT_PERCENT = 25    # R5
    SERVICE_CHARGE = 20         # R6

    def __init__(self):
        self._driver = None
        self._logged_in = False
        self._vehicles = {}     # plate -> is_electric
        self._wallet = 0

    # ---- account set-up -------------------------------------------------
    def login(self, driver):
        self._driver = driver
        self._logged_in = True

    def logout(self):
        self._logged_in = False

    def link_vehicle(self, plate, electric=False):
        self._vehicles[plate] = electric

    def set_wallet(self, rupees):
        self._wallet = rupees

    def wallet_balance(self):
        return self._wallet

    # ---- the exit gate --------------------------------------------------
    def exit(self, plate, minutes_parked, seconds_parked=0):
        total_seconds = minutes_parked * 60 + seconds_parked

        # R2 + R6: grace-period exits are free, with no service charge.
        if total_seconds <= self.GRACE_SECONDS:
            return ExitResult(message=SUCCESS_MESSAGE, gate_open=True)

        # R1: only logged-in drivers with a linked vehicle can pay by wallet.
        if not self._logged_in:
            return ExitResult(message=LOGIN_REQUIRED_MESSAGE)
        if plate not in self._vehicles:
            return ExitResult(message=NOT_LINKED_MESSAGE)

        parking_fee = self._parking_fee(total_seconds)                  # R3 + R4
        ev_discount = self._ev_discount(parking_fee, self._vehicles[plate])  # R5
        total = parking_fee - ev_discount + self.SERVICE_CHARGE         # R6
        result = ExitResult(parking_fee=parking_fee, ev_discount=ev_discount,
                            service_charge=self.SERVICE_CHARGE, total_payable=total)

        # R7: the wallet must cover the total payable.
        if self._wallet < total:
            result.message = INSUFFICIENT_MESSAGE
            return result

        self._wallet -= total                                           # R8
        result.total_paid = total
        result.message = SUCCESS_MESSAGE
        result.gate_open = True
        return result

    # ---- rule helpers ---------------------------------------------------
    def _parking_fee(self, total_seconds):
        started_hours = -(-total_seconds // 3600)        # ceiling division (R3)
        fee = self.FIRST_HOUR + (started_hours - 1) * self.EXTRA_HOUR
        return min(fee, self.FEE_CAP)                    # R4

    def _ev_discount(self, capped_fee, electric):
        # R5: discount is applied AFTER the cap, to the parking fee only.
        return capped_fee * self.EV_DISCOUNT_PERCENT // 100 if electric else 0
