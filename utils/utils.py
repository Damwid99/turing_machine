def render_txt(path: str):
    '''
    Returns:
        - initial word (list)
        - all possible states (list)
        - accepting states (list)
        - initial state (str)
        - relations (list(list))
    '''
    with open(path, 'r') as file:
        lines = file.readlines()
        relation_flag = False
        for idx, line in enumerate(lines):
            if line.strip() == 'slowo wejsciowe:' and idx + 1 < len(lines):
                initial = [x for x in lines[idx + 1].strip()]
            elif line.strip() == 'stany:' and idx + 1 < len(lines):
                states = lines[idx + 1].strip().split()
            elif line.strip() == 'stany akceptujace:' and idx + 1 < len(lines):
                accepting_states = lines[idx + 1].strip().split()
            elif line.strip() == 'stan poczatkowy:' and idx + 1 < len(lines):
                initial_state = lines[idx + 1].strip()
            elif line.strip() == 'relacja przejscia:' and idx + 1 < len(lines):
                relation_flag = True
                # print('relacje')
                relations = []
            elif relation_flag == True:
                relations.append(line.strip().split())
                # print(line.strip())
    return initial, states, accepting_states, initial_state, relations

if __name__ == "__main__":
    init, stats, accepting_stats, initial_stat, rels = render_txt('./in.txt')

    print(init)
    print(stats)
    print(accepting_stats)
    print(initial_stat)
    print(rels)


