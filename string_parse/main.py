def most_common_words(string, N):
    words = string.split()
    occurrences = {}
    for word in words:
        if word not in occurrences:
            occurrences[word] = 0
        occurrences[word] += 1
    occurrences = list(occurrences.items())
    occurrences = sorted(occurrences, key=lambda elem: -elem[1])
    return tuple(occurrences[i][0] for i in range(min(N, len(occurrences))))


def test(string, N, *correct_answers):
    answer = most_common_words(string, N)
    for correct_answer in correct_answers:
        try:
            assert answer == correct_answer
            break
        except AssertionError:
            continue
    else:
        raise AssertionError("incorrect answer: " + str(answer))


test("a a a f d ff fg gg d", 2, ("a", "d"))
test("a a a f b ff fg gg b ff", 2, ("a", "ff"), ("a", "b"))
test("a b", 3, ("b", "a"), ("a", "b"))
