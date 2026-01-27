import time
import sudoku as s
import csv
from multiprocessing import Pool, cpu_count
import argparse


def read_string(puzzle_string):
    current_grid = []
    for i in range(0, 81, 9):
        grid_row = [int(char) for char in puzzle_string[i:i+9]]
        current_grid.append(grid_row)
    return current_grid


def read_grids(filename, num_puzzles):
    grids = []
    with open(filename, 'r') as f:
        reader = csv.reader(f)
        next(reader)
        
        for idx,row in enumerate(reader):
            if idx == num_puzzles:
                break
            else:
                puzzle = read_string(row[0])
                solution = read_string(row[1])
                grids.append((puzzle,solution))
    return grids


def solve_chunk(chunk):
    success_count = 0
    times = []
    for grid_data, solution_data in chunk:
        start = time.time()
        count_zeros = sum(row.count(0) for row in grid_data)
        solution, success = s.solve_sudoku(grid_data, 0, count_zeros)
        end = time.time()
        
        if success:
            assert solution == solution_data
            success_count += 1
            times.append(round(end - start, 5))
    
    return success_count, times


def make_chunks(lst, chunk_size):
    return [lst[i:i + chunk_size] for i in range(0, len(lst), chunk_size)]


def solve_many_sudokus_parallel(grids, num_puzzles, chunk_size, num_workers):
    if num_workers is None:
        num_workers = cpu_count()
    
    chunks = make_chunks(grids, chunk_size)
    print(f"Split {len(grids)} puzzles into {len(chunks)} chunks of {chunk_size} each")
    print(f"Using {num_workers} workers")
    
    with Pool(num_workers) as pool:
        results = pool.map(solve_chunk, chunks)
    
    total_success = sum(r[0] for r in results)
    all_times = [t for r in results for t in r[1]]
    
    return total_success, all_times


def main():
    parser = argparse.ArgumentParser(description="Sudoku Solver Benchmark")
    parser.add_argument('--num_puzzles', type=int, default=1000, help="Number of puzzles to solve (max is 9 million)")
    parser.add_argument('--chunk_size', type=int, default=100, help="Number of puzzles to allocate per process")
    parser.add_argument('--num_workers', type=int, default=2, help="Number of threads to allocate for computing")
    args = parser.parse_args()

    num_puzzles = args.num_puzzles
    chunk_size =  args.chunk_size
    num_workers = args.num_workers

    grids = read_grids('sudoku.csv', num_puzzles)
    start = time.time()
    success_count, times = solve_many_sudokus_parallel(grids, num_puzzles, chunk_size, num_workers)
    total_time = time.time() - start

    print(f"Solved {success_count} puzzles ({round((success_count/num_puzzles)*100,2)}%) in {total_time:.2f}s total")
    print(f"Average {sum(times)/success_count:.5f} seconds per puzzle")


if __name__ == '__main__':
    main()
