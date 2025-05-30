def appearance(intervals: dict[str, list[int]]) -> int:
    lesson = intervals['lesson']
    pupil = intervals['pupil']
    tutor = intervals['tutor']

    # Преобразуем интервалы в список кортежей (начало, конец)
    def prepare_intervals(intervals_list):
        return [(intervals_list[i], intervals_list[i + 1]) for i in range(0, len(intervals_list), 2)]

    pupil_intervals = prepare_intervals(pupil)
    tutor_intervals = prepare_intervals(tutor)
    lesson_start, lesson_end = lesson[0], lesson[1]

    # Находим все пересечения интервалов ученика и учителя
    common_intervals = []
    for p_start, p_end in pupil_intervals:
        p_start = max(p_start, lesson_start)
        p_end = min(p_end, lesson_end)
        if p_start >= p_end:
            continue

        for t_start, t_end in tutor_intervals:
            t_start = max(t_start, lesson_start)
            t_end = min(t_end, lesson_end)
            if t_start >= t_end:
                continue

            # Находим пересечение интервалов
            overlap_start = max(p_start, t_start)
            overlap_end = min(p_end, t_end)
            if overlap_start < overlap_end:
                common_intervals.append((overlap_start, overlap_end))

    # Объединяем пересекающиеся интервалы
    if not common_intervals:
        return 0

    common_intervals.sort()
    merged = [common_intervals[0]]
    for current in common_intervals[1:]:
        last = merged[-1]
        if current[0] <= last[1]:
            merged[-1] = (last[0], max(last[1], current[1]))
        else:
            merged.append(current)

    # Суммируем продолжительность всех интервалов
    total_time = sum(end - start for start, end in merged)
    return total_time


tests = [
    {'intervals': {'lesson': [1594663200, 1594666800],
             'pupil': [1594663340, 1594663389, 1594663390, 1594663395, 1594663396, 1594666472],
             'tutor': [1594663290, 1594663430, 1594663443, 1594666473]},
     'answer': 3117
    },
    {'intervals': {'lesson': [1594702800, 1594706400],
             'pupil': [1594702789, 1594704500, 1594702807, 1594704542, 1594704512, 1594704513, 1594704564, 1594705150, 1594704581, 1594704582, 1594704734, 1594705009, 1594705095, 1594705096, 1594705106, 1594706480, 1594705158, 1594705773, 1594705849, 1594706480, 1594706500, 1594706875, 1594706502, 1594706503, 1594706524, 1594706524, 1594706579, 1594706641],
             'tutor': [1594700035, 1594700364, 1594702749, 1594705148, 1594705149, 1594706463]},
    'answer': 3577
    },
    {'intervals': {'lesson': [1594692000, 1594695600],
             'pupil': [1594692033, 1594696347],
             'tutor': [1594692017, 1594692066, 1594692068, 1594696341]},
    'answer': 3565
    },
]

if __name__ == '__main__':
   for i, test in enumerate(tests):
       test_answer = appearance(test['intervals'])
       # print(test_answer)
       assert test_answer == test['answer'], f'Error on test case {i}, got {test_answer}, expected {test["answer"]}'
