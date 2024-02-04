import requests
import pytest


URL= 'https://pokeapi.co/api/v2/type'


#q1

def test_pokemon_type():

    response = requests.get(URL)
    assert response.status_code == 200, f"Failed "

    data = response.json()
    assert isinstance(data, dict), f"Expected JSON response from Pokémon type API, got {type(data)}"
    print(data)
    result = data.get('results', [])
    assert len(result) == 20, f"Expected 20 different Pokémon types{len(result)}"


#q2

def test_fire():

    response = requests.get(URL)
    assert response.status_code == 200, "Failed "
    data = response.json()
    fireType = next((t for t in data['results'] if t['name'] == 'fire'), None)
    assert fireType is not None, "Fire type not found"

    firePokList = fireType['url']
    response = requests.get(firePokList)
    assert response.status_code == 200, "Failed"
    fire_pokemon_list = response.json()['pokemon']
    assert any(pokemon['pokemon']['name'] == 'charmander' for pokemon in fire_pokemon_list), \
        "charmander not found"
    assert all(pokemon['pokemon']['name'] != 'bulbasaur' for pokemon in fire_pokemon_list), \
        "bulbasaur found"



#q3


def fetch_pokemon_by_name(pokemon_name):
    try:
        response = requests.get(f'https://pokeapi.co/api/v2/pokemon/{pokemon_name}')
        response.raise_for_status()
        return response.json()
    except requests.HTTPError as http_err:
        print(f'HTTP error occurred: {http_err}')
    except Exception as err:
        print(f'Other error occurred: {err}')
    return None


@pytest.mark.parametrize("pokemon_name, expected_weight", [
    ('charizard-gmax', 10000),
    ('cinderace-gmax', 10000),
    ('coalossal-gmax', 10000),
    ('centiskorch-gmax', 10000),
    ('groudon-primal', 9997)
])
def test_pokemon_weight(pokemon_name, expected_weight):
    pokemon_details = fetch_pokemon_by_name(pokemon_name)
    assert pokemon_details is not None, f"Details for {pokemon_name} could not be fetched."
    assert pokemon_details[
               'weight'] == expected_weight, f"Weight of {pokemon_name} is {pokemon_details['weight']}, expected {expected_weight}."