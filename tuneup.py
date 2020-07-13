#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Tuneup assignment

Use the timeit and cProfile libraries to find bad code.
"""

__author__ = "Lori Henderson with some help from Chris Warren for the profile function"

import cProfile
import pstats
import functools
import timeit


def profile(func):
    """A cProfile decorator function that can be used to
    measure performance.
    """
    @functools.wraps(func)
    def profile_wrapper(*args, **kwargs):
        performance_object = cProfile.Profile()
        performance_object.enable()
        result = func(*args, **kwargs)
        performance_object.disable()

        get_stats_obj = pstats.Stats(performance_object)
        get_stats_obj.strip_dirs()
        get_stats_obj.sort_stats("cumulative")
        get_stats_obj.print_stats(10)

        return result

    return profile_wrapper

def read_movies(src):
    """Returns a list of movie titles."""
    print(f'Reading file: {src}')
    with open(src, 'r') as f:
        return f.read().splitlines()


def is_duplicate(title, movies):
    """Returns True if title is within movies list."""
    for movie in movies:
        if movie == title:
            return True
    return False

@profile
def find_duplicate_movies(src):
    """Returns a list of duplicate movies from a src list."""
    movies = read_movies(src)
    duplicates = []
    while movies:
        movie = movies.pop()
        if is_duplicate(movie, movies):
            duplicates.append(movie)
    return duplicates


def timeit_helper():
    """Part A: Obtain some profiling measurements using timeit."""
    t = timeit.Timer(stmt="find_duplicate_movies('movies.txt')", setup="from __main__ import find_duplicate_movies")
    results = min(t.repeat(repeat=7, number=5))

    return "Best time across 7 repeats of 5 runs per repeat:" + str(results) + "sec"


def main():
    """Computes a list of duplicate movie entries."""
    result = find_duplicate_movies('movies.txt')
    print(f'Found {len(result)} duplicate movies:')
    print('\n'.join(result))

    print(f"Best time across 7 repeats of 5 runs per repeat: " + str(timeit_helper()) + "sec")


if __name__ == '__main__':
    main()
