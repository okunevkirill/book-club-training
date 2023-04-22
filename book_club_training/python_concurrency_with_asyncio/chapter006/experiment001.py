import asyncio
import concurrent.futures
import functools
import time
import tracemalloc
from typing import Dict


def get_file_cursors(path: str, chunk_size: int) -> list[tuple[int, int]]:
    chunks = []

    with open(path, mode="rb") as fp:
        chunk_start_cursor = 0
        end_file_cursor = fp.seek(0, 2)

        fp.seek(0)

        while chunk_start_cursor < end_file_cursor:
            current_cursor = fp.seek(chunk_start_cursor + chunk_size)

            if current_cursor > end_file_cursor:
                current_cursor = end_file_cursor
            else:
                while (byte := fp.read(1)) and byte != b"\n":
                    pass
                current_cursor = fp.tell()

            chunk = chunk_start_cursor, current_cursor
            chunks.append(chunk)
            chunk_start_cursor = current_cursor

    return chunks


def map_frequencies(file_path: str, chunk: tuple[int, int]) -> Dict[str, int]:
    with open(file_path, encoding="utf-8") as fp:
        start, end = chunk
        counter = {}

        fp.seek(start)

        while fp.tell() != end:
            word, _, count, _ = fp.readline().split("\t")
            counter[word] = (
                counter[word] + int(count) if counter.get(word) else int(count)
            )
    return counter


def merge_dictionaries(first: Dict[str, int], second: Dict[str, int]) -> Dict[str, int]:
    merged = first
    for key in second:
        merged[key] = merged[key] + second[key] if key in merged else second[key]
    return merged


async def main():
    file_path = "googlebooks-eng-all-1gram-20120701-a"
    chunks = get_file_cursors(file_path, 300000000)

    loop = asyncio.get_running_loop()
    tasks = []
    start = time.perf_counter()

    with concurrent.futures.ProcessPoolExecutor() as pool:
        tasks.extend(
            loop.run_in_executor(
                pool, functools.partial(map_frequencies, file_path, chunk)
            )
            for chunk in chunks
        )
        intermediate_results = await asyncio.gather(*tasks)
        final_result = functools.reduce(merge_dictionaries, intermediate_results)

        print(f"Aardvark has appeared {final_result['Aardvark']} times.")

        end = time.perf_counter()
        print(f"MapReduce took: {(end - start):.4f} seconds")


if __name__ == "__main__":
    tracemalloc.start()
    asyncio.run(main())
    _, peak_memory = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    print(peak_memory / 1024 / 1024, "mb")
