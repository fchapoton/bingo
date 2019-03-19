# Ignoring some linting rules in tests
# pylint: disable=redefined-outer-name
# pylint: disable=missing-docstring
import pytest

from bingo.MultipleFloats import MultipleFloatChromosome,\
                                 MultipleFloatChromosomeGenerator

LIST_SIZE = 10
OPT_INDEX_START = 1
OPT_INDEX_STOP = 3

@pytest.fixture
def list_of_floats():
    return [float(i) for i in range(10)]

@pytest.fixture
def opt_individual(list_of_floats):
    opt_list = [i for i in range(OPT_INDEX_START, OPT_INDEX_STOP+1)]
    return MultipleFloatChromosome(list_of_floats, opt_list)

@pytest.fixture
def individual(list_of_floats):
    return MultipleFloatChromosome(list_of_floats)

def return_float_one():
    return 1.0

def test_accpets_valid_indicies(list_of_floats):
    with pytest.raises(ValueError):
        MultipleFloatChromosomeGenerator(return_float_one, LIST_SIZE, [6, 1, 22])
    with pytest.raises(ValueError):
        MultipleFloatChromosomeGenerator(return_float_one, LIST_SIZE, ['a', 2, 3])

def test_removes_duplicates():
    list_of_dupes = [6, 1, 1, 2, 3, 4, 5, 5, 5, 0, 5, 5, 5, 5, 5, 9, 8, 7, 5]
    generator = MultipleFloatChromosomeGenerator(return_float_one,
                                                 LIST_SIZE,
                                                 list_of_dupes)
    assert generator._needs_opt_list == [i for i in range(LIST_SIZE)]

def test_generator_function_produces_floats():
    def bad_function():
        return "This is not good"
    with pytest.raises(ValueError):
        MultipleFloatChromosomeGenerator(bad_function, LIST_SIZE)

def test_needs_local_optimization(opt_individual, individual):
    assert not individual.needs_local_optimization()
    assert opt_individual.needs_local_optimization()

def test_get_local_optimization_params(opt_individual):
    assert opt_individual.get_number_local_optimization_params() == 3

def test_set_local_optimization_params(opt_individual):
    params = [0 for _ in range(OPT_INDEX_START, OPT_INDEX_STOP+1)]
    opt_individual.set_local_optimization_params(params)
    new_values = opt_individual.list_of_values[OPT_INDEX_START:OPT_INDEX_STOP+1]
    assert new_values == params
