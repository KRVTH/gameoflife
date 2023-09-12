import sys

def main():
    try:
        input_name = sys.argv[1]
    except IndexError:
        sys.exit( "Please indicate a Filename." )
    try:
        output_name = sys.argv[2]
    except IndexError:
        sys.exit( "No Output Name Indicated" )
    try:
        n = int(sys.argv[3])
    except IndexError:
        sys.exit("No number of generation")
    except ValueError:
        sys.exit(f"Invalid number of generation: {sys.argv[3]}")

    w, h, array = read_file(input_name)
    board = playboard (w, h,  array)

    print_board(board)
    

def read_file(input_name):
    with open(input_name) as f:
        w, h = [int(x) for x in next(f).split()] # read first line
        array = []
        for line in f: # read rest of lines
            array.append([int(x) for x in line.split()])
    return [w, h, array]

def playboard(w,h, array):
    board = [[0 for _ in range(w)] for _ in range(h)]

    for position in array:
        row, col = position
        if 0 <= row < h and 0 <= col < w:
            board [row][col] = 1

    return board

def print_board(board):
    for row in board:
        print(' '.join(map(str, row)))
        
if __name__ == "__main__":
    main()
    
            