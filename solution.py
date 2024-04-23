#!/usr/bin/env python3

CHARSET = 'cp850'
CHAIRS = 'WPSC'
WALLS = '|¦\\/-_+*'  # wall characters include * marker

Point = tuple[int, int]

the_map: list[bytearray] = []
room_data: dict[str, tuple[int, int]|dict[str, int]] = {}


def load_map(fh):
    '''
    load map data from file,
    get room names and
    initialize room scan starting points
    '''
    line: str
    for y, line in enumerate(fh):
        st = 0
        while (st := line.find('(', st)) > -1 and (en := line.find(')', st)) > -1:
            # extract room name and keep its position for later
            room_name = line[st + 1:en]
            l = en - st + 1
            # replace room name with whitespace
            line = line[:st] + (' ' * l) + line[en + 1:]

            n = 1
            postfix = ''
            # handle duplicate room names properly
            while room_name + postfix in room_data:
                postfix = ' ' + str(n)
                n += 1
            room_name = room_name + postfix

            # save old name location as starting point
            room_data[room_name] = (st, y)
            st = en

        # strip CR & LF characters
        the_map.append(bytearray(line.rstrip('\r\n'), CHARSET))


def scan_room(st: Point) -> dict[str, int]:
    '''
    scan room using simplified flood fill algorithm,
    starting at provided point
    '''
    next_points: set[Point] = {st}
    counts: dict[str, int] = {k: 0 for k in CHAIRS}

    while next_points:
        x, y = next_points.pop()

        line_above = the_map[y - 1] if y > 0 else b''
        line_current = the_map[y]
        line_below = the_map[y + 1] if y < len(the_map) - 1 else b''
        lla = len(line_above)
        llb = len(line_below)

        prev_above: Point | None = None
        prev_below: Point | None = None

        # go left, then right
        for rng in (range(x, -1, -1), range(x + 1, len(line_current))):
            for i in rng:
                current_char = chr(line_current[i])
                if current_char in WALLS:
                    # hit the wall
                    break

                if current_char in CHAIRS:
                    counts[current_char] += 1

                # fill scanned path with ***
                line_current[i] = ord('*')

                if i < lla:
                    if chr(line_above[i]) not in WALLS:
                        prev_above = (i, y - 1)
                    elif prev_above:
                        next_points.add(prev_above)
                        prev_above = None

                if i < llb:
                    if chr(line_below[i]) not in WALLS:
                        prev_below = (i, y + 1)
                    elif prev_below:
                        next_points.add(prev_below)
                        prev_below = None

            if prev_above:
                next_points.add(prev_above)
                prev_above = None
            if prev_below:
                next_points.add(prev_below)
                prev_below = None

    return counts


def main(fh):
    load_map(fh)

    totals = {k: 0 for k in CHAIRS}
    for rn in room_data:
        result = scan_room(room_data[rn])  # type:ignore
        for k in result:
            totals[k] += result[k]
        room_data[rn] = result

    print('total:')
    print('W: {W}, P: {P}, S: {S}, C: {C}'.format_map(totals))
    for rn in sorted(room_data.keys()):
        print(f'{rn}:')
        print('W: {W}, P: {P}, S: {S}, C: {C}'.format_map(room_data[rn]))  # type:ignore


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('infile', help='Read scheme from this file (`-` for stdin)',
                        type=argparse.FileType('r', encoding=CHARSET))

    args = parser.parse_args()
    main(args.infile)
