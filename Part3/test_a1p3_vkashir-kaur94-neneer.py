# !/usr/bin/env python3
# YOU SHOULD NOT MODIFY THIS FILE
# 
# autograding code for B551 A1P2, Fall 2021
#
#Stephen Karukas, Zoher Kachwala, Vrinda Mathur

import route
import pytest
import json

GLOBALS = globals()
GREEN = '\033[92m'
ENDC = '\033[0m'
BOLD = '\033[1m'
STATES = {
    'Alabama', 'Arizona', 'Arkansas', 'California','Colorado', 'Connecticut', 
    'Delaware', 'Florida', 'Georgia', 'Idaho', 'Illinois', 'Indiana', 'Iowa', 
    'Kansas', 'Kentucky', 'Louisiana', 'Maine', 'Maryland', 'Massachusetts', 
    'Michigan', 'Minnesota', 'Mississippi','Missouri', 'Montana', 'Nebraska', 
    'Nevada', 'New_Hampshire', 'New_Jersey', 'New_Mexico', 'New_York', 'North_Carolina', 
    'North_Dakota', 'Ohio', 'Oklahoma', 'Oregon', 'Pennsylvania', 'Rhode_Island',
    'South_Carolina', 'South_Dakota', 'Tennessee', 'Texas', 'Utah', 'Vermont', 
    'Virginia', 'Washington', 'West_Virginia', 'Wisconsin', 'Wyoming'
}


def isnumber(obj):
    return isinstance(obj, int) or isinstance(obj, float)

def validate_route(answer, end_city):
    assert isinstance(answer, dict), "get_route() is not returning a dictionary"
    assert len(answer) >= 5, "Too few parts: returned dictionary should have 5 keys"

    segments, miles = answer['total-segments'], answer['total-miles']
    hours, delivery_hours, route_taken = answer['total-hours'], answer['total-delivery-hours'], answer['route-taken']

    assert isnumber(segments), f'{segments} is not a number: total-segments must be a number'
    assert segments > 0, f'{segments} < 0: total-segments must be positive'

    assert isnumber(miles), f'{str(miles)} is not a number: total-miles must be a number'
    assert miles > 0, f'{str(miles)} < 0: total-miles must be positive'

    assert isnumber(hours), f'{str(hours)} is not a number: total-hours must be a number'
    assert hours > 0, f'{str(hours)} < 0: total-hours must be positive'

    assert isnumber(delivery_hours), f'{str(delivery_hours)} is not a number: total-delivery-hours must be a number'
    assert delivery_hours > 0, f'{str(delivery_hours)} < 0: total-delivery-hours must be positive'

    #assert route_taken[segments - 1][0] == end_city, f'{route_taken[segments - 1][0]} is not {end_city}. Not the end-city'
    return {
        "segments": segments, 
        "distance": miles, 
        "time": hours,
        "delivery": delivery_hours
    }


def run_test(filename, cost_function):
    """
Run test case from a JSON file.
- This test checks only if the specified cost function
    is correct (in order to encourage partial credit).
- A test file specifies a start city, end city, 
    and the optimal answer for each cost function.
    """
    assert filename.endswith(".json")

    f = open(filename)
    test_data = json.load(f)
    start = test_data['start']
    end = test_data['end']
    optimal_ans = test_data['solutions'][cost_function]

    # give leeway for slight differences in solutions
    upper = optimal_ans * 1.2
    lower = optimal_ans * 0.8
    start_name = start.split(",")[0]
    end_name = end.split(",")[0]
    description = f"{start_name} -> {end_name} by {cost_function}"

    output = route.get_route(start, end, cost_function)
    calculated = validate_route(output, end)[cost_function]

    assert calculated <= upper, f'Answer is suboptimal [{description}]'
    assert calculated >= lower, f'Answer is too low, probably incorrectly calculated [{description}]'

    f.close()


def get_state(city):
    return city.split(",")[1][1:]


## first test case
@pytest.mark.timeout(120)
def test_p2_1_segments():
    run_test("./test_p2_1.json", "segments")

@pytest.mark.timeout(120)
def test_p2_1_distance():
    run_test("./test_p2_1.json", "distance")

@pytest.mark.timeout(120)
def test_p2_1_time():
    run_test("./test_p2_1.json", "time")

@pytest.mark.timeout(120)
def test_p2_1_delivery():
    run_test("./test_p2_1.json", "delivery")


## second test case
@pytest.mark.timeout(300)
def test_p2_2_segments():
    run_test("./test_p2_2.json", "segments")

@pytest.mark.timeout(300)
def test_p2_2_distance():
    run_test("./test_p2_2.json", "distance")

@pytest.mark.timeout(300)
def test_p2_2_time():
    run_test("./test_p2_2.json", "time")

@pytest.mark.timeout(300)
def test_p2_2_delivery():
    run_test("./test_p2_2.json", "delivery")

## third test case
@pytest.mark.timeout(300)
def test_p2_3_segments():
    run_test("./test_p2_3.json", "segments")

@pytest.mark.timeout(300)
def test_p2_3_distance():
    run_test("./test_p2_3.json", "distance")

@pytest.mark.timeout(300)
def test_p2_3_time():
    run_test("./test_p2_3.json", "time")

@pytest.mark.timeout(300)
def test_p2_3_delivery():
    run_test("./test_p2_3.json", "delivery")


# statetour
@pytest.mark.timeout(600)
def test_statetour():
    print(f"{GREEN+BOLD}This test case is expected to fail unless if you have implemented statetour.{ENDC}")
    start = 'Walla_Walla,_Washington'
    end = 'North_Berwick,_Maine'
    states_c = STATES.copy()
    states_c.remove(get_state(start))
    states_c.remove(get_state(end))
    output = route.get_route(start, end, 'statetour')
    
    for city, road in output['route-taken']:
        st = get_state(city)
        states_c.discard(st)
    
    assert len(states_c) == 0, f'Your path did not visit the following states:\n {", ".join(states_c)}'
    assert output['total-miles'] < 14_000, 'Your path is not short enough.'