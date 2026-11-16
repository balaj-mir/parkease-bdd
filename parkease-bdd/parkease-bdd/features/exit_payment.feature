Feature: Automatic parking fee payment on exit
  As a registered ParkEase driver,
  I want my parking fee to be charged automatically from my wallet when I exit,
  so that I can leave the plaza without queuing at a payment booth.

  @smoke
  Scenario: Registered EV driver is charged automatically after 3 hours 40 minutes
    Given Sara is logged in to ParkEase
    And her electric vehicle "LEC-2024" is linked to her account
    And her wallet balance is Rs. 1,000
    And her vehicle entered the plaza 3 hours 40 minutes ago
    When her vehicle reaches the exit gate
    Then she sees the message "Payment successful – gate opening"
    And the parking fee is Rs. 280
    And the EV discount is Rs. 70
    And the service charge is Rs. 20
    And the total paid is Rs. 230
    And the gate is open
    And her wallet balance is Rs. 770

  @boundary
  Scenario Outline: Petrol car fee at the grace, rounding and cap boundaries
    Given Ali is logged in to ParkEase
    And his petrol vehicle "LHR-4521" is linked to his account
    And his wallet balance is Rs. 1,000
    And his vehicle entered the plaza <parked> ago
    When his vehicle reaches the exit gate
    Then he sees the message "Payment successful – gate opening"
    And the parking fee is <parking_fee>
    And the EV discount is Rs. 0
    And the service charge is <service_charge>
    And the total paid is <total_paid>
    And the gate is open
    And his wallet balance is <wallet_after>

    Examples: Free and rounding
      | parked              | parking_fee | service_charge | total_paid | wallet_after |
      | 15 minutes          | Rs. 0       | Rs. 0          | Rs. 0      | Rs. 1,000    |
      | 15 minutes 1 second | Rs. 100     | Rs. 20         | Rs. 120    | Rs. 880      |
      | 60 minutes          | Rs. 100     | Rs. 20         | Rs. 120    | Rs. 880      |
      | 61 minutes          | Rs. 160     | Rs. 20         | Rs. 180    | Rs. 820      |
      | 2 hours 10 minutes  | Rs. 220     | Rs. 20         | Rs. 240    | Rs. 760      |

    Examples: Daily cap
      | parked              | parking_fee | service_charge | total_paid | wallet_after |
      | 12 hours            | Rs. 760     | Rs. 20         | Rs. 780    | Rs. 220      |
      | 12 hours 1 minute   | Rs. 800     | Rs. 20         | Rs. 820    | Rs. 180      |
      | 24 hours            | Rs. 800     | Rs. 20         | Rs. 820    | Rs. 180      |

  @negative
  Scenario: Wallet is Rs. 1 short of the total payable
    Given Ali is logged in to ParkEase
    And his petrol vehicle "LHR-4521" is linked to his account
    And his wallet balance is Rs. 239
    And his vehicle entered the plaza 2 hours 10 minutes ago
    When his vehicle reaches the exit gate
    Then he sees the message "Insufficient wallet balance"
    And the total paid is Rs. 0
    And his wallet balance is Rs. 239
    And the gate stays closed

  @boundary
  Scenario: EV discount is applied after the daily cap
    Given Sara is logged in to ParkEase
    And her electric vehicle "LEC-2024" is linked to her account
    And her wallet balance is Rs. 1,000
    And her vehicle entered the plaza 12 hours 1 minute ago
    When her vehicle reaches the exit gate
    Then she sees the message "Payment successful – gate opening"
    And the parking fee is Rs. 800
    And the EV discount is Rs. 200
    And the service charge is Rs. 20
    And the total paid is Rs. 620
    And her wallet balance is Rs. 380
