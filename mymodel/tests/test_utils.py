from mymodel.utils import generate_probabilities


def test_generate_probabilities():
    N = 10
    probs = generate_probabilities(N)
    assert len(probs) == N
    assert all(0.0 <= p <= 1.0 for p in probs)
